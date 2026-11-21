"""Benchmark CÓ RENDER THẬT (contract v1.3, TICKET-04).

    python3 -m chonoi.bench --seed 42 --duration 30 --out bench.json

Mở cửa sổ tkinter 1280×720 (thư viện chuẩn), vẽ cảnh Gather lõi của ngày 1: nước, nút hái, đàn cá bơi,
Cá Sấu, độ tươi của giỏ và HUD. Út Sen đứng yên tại bến. Mô phỏng chạy đúng 60 tick/s theo đồng hồ thật
(cùng `GatherSim` như headless); mỗi vòng vẽ lại toàn cảnh và đẩy lên màn hình (`update()`), không giới hạn FPS.

Đo: warm-up 3 s rồi đo `--duration` giây. Ghi đúng 5 trường:
  avg_fps     = frames / measured_s
  p1_low_fps  = 1 / (thời gian khung trung bình của max(1, ceil(1% × frames)) khung chậm nhất)
  frames      = số khung trong cửa sổ đo
  measured_s  = thời gian đo thực (giây)
  load_ms     = từ khi khởi chạy lệnh tới khi khung đầu tiên của cảnh được vẽ xong
Đồng hồ chỉ dùng để ĐO và giữ nhịp tick, không đi vào luật. Mã thoát: 0 xong, 2 tham số sai,
1 không mở được cửa sổ (không có màn hình) hoặc lỗi ghi file.
"""

import time

T_LAUNCH = time.perf_counter()  # mốc "khởi chạy" cho load_ms, đặt trước mọi import nặng

import argparse  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402

from .contract import load_contract  # noqa: E402
from .ids import IdAllocator  # noqa: E402
from .inputs import InputState  # noqa: E402
from .rng import Streams  # noqa: E402
from .sim.gather import GatherSim  # noqa: E402

W, H = 1280, 720
WARMUP_S = 3.0
TICK_S = 1 / 60
IDLE = InputState((0.0, 0.0), {}, set())
KIND_COLOR = {"ca_loc": "#7c9a52", "ca_linh": "#d6e6f2", "ca_keo": "#d9a066", "bong_dien_dien": "#f2c230",
              "bong_sung": "#e8799c", "keo_neo": "#8fcf6b"}


def p1_low(frame_times):
    if not frame_times:
        return 0.0
    k = max(1, math.ceil(0.01 * len(frame_times)))
    worst = sorted(frame_times, reverse=True)[:k]
    return 1.0 / (sum(worst) / k)


class Scene:
    """Vẽ cảnh Gather lên tkinter.Canvas từ snapshot của GatherSim (chỉ đọc)."""

    def __init__(self, canvas, tuning):
        self.c = canvas
        g = tuning["gather"]
        (self.x0, self.x1), (self.d0, self.d1) = g["bounds"]["x"], g["bounds"]["d"]
        self.top, self.bottom = 90, H - 70
        self.sx = (W - 40) / (self.x1 - self.x0)
        self.sd = (self.bottom - self.top) / (self.d1 - self.d0)

    def px(self, x, d):
        return 20 + (x - self.x0) * self.sx, self.top + (d - self.d0) * self.sd

    def draw(self, snap, sim):
        c = self.c
        c.delete("all")
        c.create_rectangle(0, 0, W, self.top, fill="#87b9d8", width=0)                     # trời
        for i in range(12):                                                               # nước theo dải sâu
            y0 = self.top + i * (self.bottom - self.top) / 12
            shade = 90 - i * 6
            c.create_rectangle(0, y0, W, y0 + (self.bottom - self.top) / 12 + 1, width=0,
                               fill="#%02x%02x%02x" % (20, 60 + shade // 2, 90 + shade))
        dx, dd = self.px(*sim.t["dock_pos"])
        c.create_rectangle(dx - 30, dd - 12, dx + 30, dd + 4, fill="#8a5a2e", outline="#3e2a14", width=2)  # bến
        for n in snap.get("nodes", []):
            x, y = self.px(*n["pos"])
            ready = n.get("regrow_ticks", 0) == 0
            c.create_oval(x - 9, y - 9, x + 9, y + 9, fill=KIND_COLOR.get(n["kind"], "#ccc") if ready else "#555",
                          outline="#fff" if ready else "#333", width=2)
        for f in snap.get("fish", []):
            x, y = self.px(*f["pos"])
            col = KIND_COLOR.get(f["kind"], "#ccc")
            c.create_oval(x - 14, y - 6, x + 14, y + 6, fill=col, outline="#102030")
            tail = -1 if math.cos(math.radians(f.get("heading_deg", 0))) >= 0 else 1
            c.create_polygon(x + tail * 14, y, x + tail * 22, y - 6, x + tail * 22, y + 6, fill=col)
        for m in snap.get("monsters", []):
            x, y = self.px(*m["pos"])
            col = {"chase": "#c62828", "recoil": "#ef6c00"}.get(m.get("state"), "#2e7d32")
            c.create_oval(x - 34, y - 11, x + 34, y + 11, fill=col, outline="#0b1f0b", width=2)
            c.create_polygon(x + 34, y - 6, x + 54, y, x + 34, y + 6, fill=col)
            c.create_text(x, y - 22, text=f"{m['id']} {m.get('state', '')}", fill="#fff", font=("Arial", 10))
        p = snap["player"]
        x, y = self.px(*p["pos"])
        c.create_oval(x - 11, y - 11, x + 11, y + 11, fill="#ff8a3d", outline="#fff", width=2)
        oxy = p["oxygen_ticks"] / max(1, p["oxygen_max_ticks"])                             # HUD
        c.create_rectangle(16, 14, 216, 30, outline="#fff")
        c.create_rectangle(16, 14, 16 + 200 * oxy, 30, fill="#4fc3f7", width=0)
        c.create_text(226, 22, anchor="w", fill="#fff", font=("Arial", 12),
                      text=f"Oxy {p['oxygen_ticks'] // 60}s · Máu {p['hp']}/{p['hp_max']} · "
                           f"còn {snap['time_left_ticks'] // 60}s · giỏ {len(snap.get('hold', []))}")
        for i, it in enumerate(snap.get("hold", [])):
            fr = float(it["fresh"]) if isinstance(it, dict) else 100.0
            c.create_rectangle(16 + i * 34, self.bottom + 14, 46 + i * 34, self.bottom + 44,
                               fill=KIND_COLOR.get(it["kind"] if isinstance(it, dict) else it, "#ccc"))
            c.create_rectangle(16 + i * 34, self.bottom + 48, 16 + i * 34 + 30 * fr / 100, self.bottom + 52,
                               fill="#66bb6a" if fr >= 30 else "#e53935", width=0)


def run_bench(seed, duration):
    import tkinter as tk

    tuning = load_contract()["tuning"]
    sim = GatherSim(tuning, {"day": 1}, Streams(seed), IdAllocator())
    # giỏ có sẵn vài cá thể để cảnh có độ tươi hao dần (giống lúc vừa lặn hái), Út Sen vẫn ở bến
    from fractions import Fraction
    for kind in ("ca_loc", "ca_linh", "bong_sung", "ca_keo"):
        sim.hold.append({"id": sim.ids.new("I"), "kind": kind, "fresh": Fraction(100)})

    root = tk.Tk()
    root.title("Chợ Nổi — benchmark")
    root.geometry(f"{W}x{H}")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0, bg="#10161c")
    canvas.pack()
    scene = Scene(canvas, tuning)

    def frame():
        scene.draw({**sim.snapshot(), "time_left_ticks": sim.time_left_ticks}, sim)
        root.update()

    frame()
    load_ms = (time.perf_counter() - T_LAUNCH) * 1000

    sim_clock = time.perf_counter()
    times, start, last, t_end = [], None, time.perf_counter(), time.perf_counter() + WARMUP_S + duration
    while True:
        now = time.perf_counter()
        while sim_clock + TICK_S <= now and not sim.done:   # mô phỏng đúng 60 tick/s
            sim.step(IDLE)
            sim_clock += TICK_S
        frame()
        now = time.perf_counter()
        if start is None and now - (t_end - WARMUP_S - duration) >= WARMUP_S:
            start, last = now, now
        elif start is not None:
            times.append(now - last)
            last = now
            if now - start >= duration:
                break
        if now > t_end + 5:  # an toàn
            break
    measured = last - start if start is not None else 0.0
    root.destroy()
    frames = len(times)
    return {"avg_fps": round(frames / measured, 2) if measured else 0.0,
            "p1_low_fps": round(p1_low(times), 2),
            "frames": frames,
            "measured_s": round(measured, 3),
            "load_ms": round(load_ms, 1)}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="chonoi.bench", description="Benchmark có render thật 1280x720.")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--duration", type=float, required=True, help="số giây đo (sau 3 s warm-up)")
    p.add_argument("--out", required=True)
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if not (0 < a.duration <= 600):
        sys.stderr.write("đầu vào sai: --duration phải trong (0, 600]\n")
        return 2
    try:
        result = run_bench(a.seed, a.duration)
    except Exception as e:  # noqa: BLE001 — không có màn hình / tkinter
        sys.stderr.write(f"không chạy được benchmark có render: {e}\n")
        return 1
    d = os.path.dirname(os.path.abspath(a.out))
    try:
        fd, tmp = tempfile.mkstemp(prefix=".bench-", suffix=".tmp", dir=d)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, a.out)
    except OSError as e:
        sys.stderr.write(f"lỗi ghi: {e}\n")
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
