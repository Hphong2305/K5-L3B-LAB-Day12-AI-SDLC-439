"""Soak headless (contract v1.3, TICKET-04): chạy N ngày liên tục trong MỘT tiến trình.

    python3 -m chonoi.soak --seed 7 --days 10 --out soak.json

Mỗi ngày đủ gather -> quan -> shop qua `DaySim` (cùng lớp với `--mode day`), giữ tiền, earned, uy tín,
nâng cấp và bộ cấp ID cá thể xuyên ngày; ngày 6..N lặp lại kế hoạch D1..D5. Không có input người chơi
(đứng yên), nên kết quả chỉ phụ thuộc seed: chạy lại cùng seed cho cùng dữ liệu, trừ `duration_s`.

Đầu ra (đúng 5 khóa): days, days_completed, crashes, results[{day, earned, reputation, score}], duration_s.
`results[]` chụp lúc Shop của ngày đó đóng. Không ghi leaderboard. Mã thoát: 0 chạy xong (kể cả có crash,
xem `crashes`), 2 tham số sai, 1 lỗi ghi file.
"""

import argparse
import json
import math
import os
import sys
import tempfile
import time
import traceback

from .contract import load_contract
from .errors import BadInput
from .ids import IdAllocator
from .inputs import InputState
from .rng import Streams
from .sim.day import DaySim

IDLE = InputState((0.0, 0.0), {}, set())
MAX_DAYS = 100


def run_soak(tuning, seed, days):
    """Chạy soak, trả dict kết quả (chưa có duration_s)."""
    sim = DaySim(tuning, {}, Streams(seed), IdAllocator(), days=days, cycle_plans=True)
    mult = tuning["score"]["reputation_multiplier"]
    results, crashes = [], 0
    # chặn trên số bước: mỗi ngày tối đa gather + quan + shop (cộng dư an toàn)
    per_day = (int(tuning["gather"]["duration_s"] * tuning["tick_hz"]) + int(tuning["quan"]["duration_s"] * tuning["tick_hz"])
               + int(tuning["shop"]["max_ticks"]) + 10)
    try:
        for _ in range(per_day * days):
            if sim.done:
                break
            for name, data in sim.step(IDLE):
                if name == "day_end":
                    rep = data["reputation"]
                    results.append({"day": data["day"], "earned": data["earned"], "reputation": rep,
                                    "score": data["earned"] + mult * math.floor(rep)})
    except Exception:  # noqa: BLE001 — soak đếm crash thay vì chết
        crashes += 1
        sys.stderr.write(traceback.format_exc())
    return {"days": days, "days_completed": len(results), "crashes": crashes, "results": results}


def _write_json(path, obj):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".soak-", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="chonoi.soak", description="Soak headless nhiều ngày trong một tiến trình.")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--days", type=int, required=True)
    p.add_argument("--out", required=True)
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    t0 = time.perf_counter()
    try:
        if not (1 <= a.days <= MAX_DAYS):
            raise BadInput(f"--days phải trong [1, {MAX_DAYS}]")
        tuning = load_contract()["tuning"]
    except BadInput as e:
        sys.stderr.write(f"đầu vào sai: {e}\n")
        return 2
    out = run_soak(tuning, a.seed, a.days)
    out["duration_s"] = round(time.perf_counter() - t0, 3)
    try:
        _write_json(a.out, out)
    except OSError as e:
        sys.stderr.write(f"lỗi ghi: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
