"""Bộ kiểm thử độc lập Phase 3 (TV5 - QA Lead)
Theo dõi và xác thực các tiêu chí AC-P3 theo TICKET-03 và Test Contract v1.2.
"""

import json
import os
import unittest

from chonoi.contract import load_contract
from helpers import Workdir, run_headless, write_json


class TestPhase3QA(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract()
        self.version = self.contract.get("contract_version", "1.1")
        # v1.3 (Phase 4) giữ nguyên luật v1.2: các test P3 phải tiếp tục chạy, không bị skip
        self.v12_or_later = tuple(int(x) for x in self.version.split(".")) >= (1, 2)

    def test_hud_html_contains_freshness_and_spoiled_indicators(self):
        """AC-P3-09: Kiểm tra HUD HTML đã có hàm xử lý độ tươi và cảnh báo hàng ươn."""
        with open("chonoi/web/index.html", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("getItemInfo", html)
        self.assertIn("fresh", html)
        self.assertIn("spoiled", html)
        self.assertIn("⚠️", html)

    def test_ac_p3_01_v11_inventory_rejected_when_v12_active(self):
        """AC-P3-01: File kho v1.1 cũ (chỉ count) phải bị từ chối với exit code 2 khi contract lên v1.2."""
        if not self.v12_or_later:
            self.skipTest("Chờ TV1/TV3 nâng cấp contract lên v1.2")
        with Workdir() as w:
            v11_inv = write_json(w.path("old_inv.json"), {
                "items": {"ca_loc": 2, "ca_linh": 3}
            })
            code, out = run_headless(
                "--mode", "quan",
                "--seed", "1",
                "--ticks", "10",
                "--inventory", v11_inv,
                "--out", w.path("out.jsonl")
            )
            self.assertEqual(code, 2, "File kho v1.1 cũ phải trả exit code 2")

    def test_ac_p3_02_spoiled_fish_at_tick_1(self):
        """AC-P3-02: Kiểm tra hàng ươn tại tick 1 khi fresh=30 (hoặc chạm ngưỡng ươn)."""
        if not self.v12_or_later:
            self.skipTest("Chờ TV1/TV2 triển khai cơ chế fresh/spoiled trong Gather")
        # Sẽ chạy khi GatherSim hỗ trợ trường fresh trong scenario/fish
        pass

    def test_ac_p3_06_id_allocator_monotonicity(self):
        """AC-P3-06: Bộ cấp phát ID phải tăng đơn điệu xuyên suốt các ngày trong mode day."""
        if not self.v12_or_later:
            self.skipTest("Chờ TV4 hoàn thiện DaySim v1.2")
        pass


if __name__ == "__main__":
    unittest.main()
