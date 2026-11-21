"""Phase 4 (contract v1.3, TICKET-04): manifest, công thức benchmark, cảnh báo + tương phản cao trong client."""

import json
import math
import os
import unittest

from chonoi.bench import p1_low
from chonoi.contract import load_contract

ROOT = os.path.join(os.path.dirname(__file__), "..")


class Manifest(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, "game.contract.json"), encoding="utf-8") as f:
            self.c = json.load(f)

    def test_v13_declares_bench_and_soak(self):
        self.assertEqual(self.c["contract_version"], "1.3")
        self.assertEqual(self.c["bench_cmd"], "python3 -m chonoi.bench")
        self.assertEqual(self.c["soak_cmd"], "python3 -m chonoi.soak")
        load_contract()  # tuning v1.2 vẫn hợp lệ

    def test_gameplay_tuning_unchanged_from_v12(self):
        t = self.c["tuning"]
        self.assertEqual(t["freshness"], {"initial": 100, "gather_decay_per_s": 0.5, "quan_decay_per_s": 0.25,
                                          "spoiled_below": 30})
        self.assertEqual(len(t["menu"]), 6)
        self.assertEqual(len(t["day_plan"]), 5)
        self.assertEqual(self.c["extensions"], ["current"])


class BenchFormula(unittest.TestCase):
    def test_p1_low_uses_ceil_1_percent_slowest_frames(self):
        times = [1 / 100] * 199 + [1 / 20]          # 200 khung -> k = 2 khung chậm nhất
        k = max(1, math.ceil(0.01 * 200))
        worst = sorted(times, reverse=True)[:k]
        self.assertAlmostEqual(p1_low(times), 1 / (sum(worst) / k))
        self.assertAlmostEqual(p1_low([1 / 50] * 10), 50)  # k = 1 khi ít khung

    def test_p1_low_empty(self):
        self.assertEqual(p1_low([]), 0.0)


class ClientWarnings(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, "chonoi", "web", "index.html"), encoding="utf-8") as f:
            self.html = f.read()

    def test_three_warnings_have_text_and_icon(self):
        for icon, words in (("🐊", "CÁ SẤU GẦN"), ("🫧", "OXY SẮP HẾT"), ("😠", "KHÁCH SẮP GIẬN")):
            self.assertIn(icon, self.html)
            self.assertIn(words, self.html)
        for fn in ("monsterNear", "oxygenLow", "customerAngry", "drawWarnings"):
            self.assertIn(f"function {fn}", self.html)

    def test_high_contrast_toggle(self):
        self.assertIn('k === "h"', self.html)
        self.assertIn('get("contrast") === "high"', self.html)
        self.assertIn("body.hc canvas", self.html)


if __name__ == "__main__":
    unittest.main()
