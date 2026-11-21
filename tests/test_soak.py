"""Soak v1.3 (TICKET-04): N ngày trong một tiến trình, kết quả tất định, giữ trạng thái xuyên ngày."""

import json
import os
import tempfile
import unittest
from fractions import Fraction

from helpers import run_headless

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator, id_key
from chonoi.inputs import InputState
from chonoi.rng import Streams
from chonoi.sim.day import DaySim
from chonoi.soak import main as soak_main, run_soak

IDLE = InputState((0.0, 0.0), {}, set())
KEYS = {"days", "days_completed", "crashes", "results", "duration_s"}


class Soak(unittest.TestCase):
    def setUp(self):
        self.t = load_contract()["tuning"]

    def cli(self, *args):
        d = tempfile.mkdtemp()
        out = os.path.join(d, "soak.json")
        code = soak_main([*args, "--out", out])
        data = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else None
        return code, data

    def test_1_5_10_days_complete_without_crash(self):
        for days in (1, 5, 10):
            code, data = self.cli("--seed", "7", "--days", str(days))
            self.assertEqual(code, 0)
            self.assertEqual(set(data), KEYS)
            self.assertEqual((data["days"], data["days_completed"], data["crashes"]), (days, days, 0))
            self.assertEqual([r["day"] for r in data["results"]], list(range(1, days + 1)))
            for r in data["results"]:
                self.assertEqual(set(r), {"day", "earned", "reputation", "score"})

    def test_same_seed_same_gameplay_data(self):
        a, b = run_soak(self.t, 7, 10), run_soak(self.t, 7, 10)
        self.assertEqual(a, b)
        self.assertNotIn("duration_s", a)  # chỉ duration_s được phép khác giữa hai lần chạy

    def test_bad_args_exit_2_without_output(self):
        for args in (("--seed", "7", "--days", "0"), ("--seed", "7", "--days", "-1"), ("--seed", "x", "--days", "3"),
                     ("--days", "3",)):
            code, data = self.cli(*args)
            self.assertEqual(code, 2, args)
            self.assertIsNone(data)

    def test_runs_in_one_process_via_manifest_soak_cmd(self):
        contract = json.load(open(os.path.join(os.path.dirname(__file__), "..", "game.contract.json"), encoding="utf-8"))
        self.assertEqual(contract["soak_cmd"], "python3 -m chonoi.soak")
        d = tempfile.mkdtemp()
        out = os.path.join(d, "s.json")
        import subprocess, sys  # noqa: E401
        p = subprocess.run([sys.executable, "-m", "chonoi.soak", "--seed", "7", "--days", "10", "--out", out],
                           cwd=os.path.join(os.path.dirname(__file__), ".."), capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.load(open(out, encoding="utf-8"))["days_completed"], 10)

    # --- trạng thái xuyên ngày --------------------------------------------------
    def test_plans_cycle_after_day_5_and_state_carries(self):
        sim = DaySim(self.t, {}, Streams(7), IdAllocator(), days=7, cycle_plans=True)
        plans = {p["day"]: p for p in self.t["day_plan"]}
        seen_plan, last_id = {}, 0
        while not sim.done:
            if sim.phase == "gather" and sim.day not in seen_plan:
                it = {"id": sim.ids.new("I"), "kind": "ca_loc", "fresh": Fraction(100)}
                self.assertGreater(id_key(it["id"])[1], last_id)  # ID không reset sang ngày mới
                last_id = id_key(it["id"])[1]
                seen_plan[sim.day] = None
            if sim.phase == "shop" and sim.day == 1 and sim.upgrades["oxygen"] == 0:
                sim.wallet = 500
                sim.step(InputState((0.0, 0.0), {}, {"buy_oxygen"}))
                continue
            for name, data in sim.step(IDLE):
                if name == "day_plan":
                    seen_plan[data["day"]] = data["dishes"]
        self.assertEqual(seen_plan[6], plans[1]["dishes"])
        self.assertEqual(seen_plan[7], plans[2]["dishes"])
        self.assertEqual(sim.upgrades["oxygen"], 1)       # nâng cấp giữ tới ngày 7
        self.assertEqual(sim.money, 500 - self.t["shop"]["upgrades"]["oxygen"][0]["price"])

    def test_mode_day_still_limited_to_5_days(self):
        d = tempfile.mkdtemp()
        code, _ = run_headless("--mode", "day", "--days", "6", "--seed", "1", "--ticks", "0",
                               "--out", os.path.join(d, "o.jsonl"))
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
