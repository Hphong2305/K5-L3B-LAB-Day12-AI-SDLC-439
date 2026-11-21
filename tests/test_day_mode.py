"""Mode `day` (v1.1, bản tạm TV4): vòng ngày, chuyển pha cùng tick, Shop/nâng cấp, pause, CLI."""

import os
import time
import unittest
from unittest import mock
from fractions import Fraction

from helpers import read_jsonl, run_headless, write_json

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator
from chonoi.inventory import format_item, fresh_to_num
from chonoi.inputs import InputState
from chonoi.rng import Streams
from chonoi.sim.day import DaySim


class Workdir:
    def __enter__(self):
        import tempfile
        self._d = tempfile.TemporaryDirectory()
        return self

    def path(self, name):
        return os.path.join(self._d.name, name)

    def __exit__(self, *a):
        self._d.cleanup()


IDLE = InputState((0.0, 0.0), {}, set())


def press(*buttons):
    return InputState((0.0, 0.0), {b: True for b in buttons}, set(buttons))


class DayMode(unittest.TestCase):
    def setUp(self):
        self.t = load_contract()["tuning"]
        self.gather_ticks = int(self.t["gather"]["duration_s"] * self.t["tick_hz"])
        self.quan_ticks = int(self.t["quan"]["duration_s"] * self.t["tick_hz"])
        self.shop_ticks = self.t["shop"]["max_ticks"]

    def sim(self, days=1):
        return DaySim(self.t, {}, Streams(1), IdAllocator(), days=days)

    def run_until(self, sim, phase, limit=50000):
        evs = []
        for _ in range(limit):
            if sim.phase == phase:
                return evs
            evs += sim.step(IDLE)
        self.fail(f"không tới pha {phase}")

    # --- vòng đời ------------------------------------------------------------
    def test_cli_one_day_lifecycle_and_same_tick_transitions(self):
        with Workdir() as w:
            out = w.path("d.jsonl")
            code, err = run_headless("--mode", "day", "--days", "1", "--seed", "1", "--ticks", "100000",
                                     "--snapshot-every", "600", "--out", out)
            self.assertEqual(code, 0, err)
            rows = read_jsonl(out)
            ev = [(r["tick"], r["name"], r["data"]) for r in rows if r["type"] == "event"]
            names = [n for _, n, _ in ev if n in ("day_start", "day_plan", "phase_start", "gather_end",
                                                    "quan_end", "shop_end", "day_end")]
            self.assertEqual(names, ["day_start", "day_plan", "phase_start", "gather_end", "phase_start",
                                     "quan_end", "phase_start", "shop_end", "day_end"])
            tick_of = {}
            for t, n, d in ev:
                tick_of.setdefault((n, d.get("phase")), t)
            self.assertEqual(tick_of[("day_start", None)], 1)
            self.assertEqual(tick_of[("gather_end", None)], tick_of[("phase_start", "quan")])
            self.assertEqual(tick_of[("quan_end", None)], tick_of[("phase_start", "shop")])
            end = rows[-1]
            self.assertEqual((end["type"], end["mode"], end["reason"]), ("end", "day", "days_complete"))
            self.assertEqual(end["ticks"], self.gather_ticks + self.quan_ticks + self.shop_ticks)

    def test_cli_deterministic_bytes_two_days(self):
        with Workdir() as w:
            outs = [w.path("a.jsonl"), w.path("b.jsonl")]
            for o in outs:
                self.assertEqual(run_headless("--mode", "day", "--days", "2", "--seed", "7", "--ticks", "60000",
                                              "--out", o)[0], 0)
            with open(outs[0], "rb") as a, open(outs[1], "rb") as b:
                self.assertEqual(a.read(), b.read())

    def test_cli_bad_days_and_flags_exit_2(self):
        with Workdir() as w:
            out = w.path("o.jsonl")
            for args in (("--mode", "day", "--days", "0"), ("--mode", "day", "--days", "6"),
                         ("--mode", "gather", "--days", "1"), ("--mode", "day", "--inventory-out", w.path("k.json"))):
                self.assertEqual(run_headless(*args, "--seed", "1", "--ticks", "0", "--out", out)[0], 2, args)
            sc = write_json(w.path("sc.json"), {"gather": {}})
            self.assertEqual(run_headless("--mode", "day", "--scenario", sc, "--seed", "1", "--ticks", "0",
                                          "--out", out)[0], 2)
            self.assertFalse(os.path.exists(out))

    def test_one_day_headless_under_20s(self):
        with Workdir() as w:
            t0 = time.perf_counter()
            run_headless("--mode", "day", "--days", "1", "--seed", "1", "--ticks", "100000", "--out", w.path("p.jsonl"))
            self.assertLess(time.perf_counter() - t0, 20)

    # --- bàn giao giữa các pha --------------------------------------------------
    def test_gather_hold_becomes_quan_stock_with_day_menu(self):
        sim = self.sim()
        sim.sub.hold = [
            {"id": "I1", "kind": "ca_loc", "fresh": 100},
            {"id": "I2", "kind": "bong_sung", "fresh": 100},
            {"id": "I3", "kind": "bong_sung", "fresh": 100},
        ]
        sim.step(press("interact"))  # đứng ở bến -> docked
        self.assertEqual(sim.phase, "quan")
        # Quán giữ fresh dạng Fraction bên trong (TV3); so ở dạng xuất ra (snapshot / file kho), làm tròn 3 chữ số.
        self.assertEqual([format_item(it) for it in sim.sub.stock], [
            {"id": "I1", "kind": "ca_loc", "fresh": 99.992},
            {"id": "I2", "kind": "bong_sung", "fresh": 99.992},
            {"id": "I3", "kind": "bong_sung", "fresh": 99.992},
        ])
        self.assertEqual(sim.sub.orderable_dishes, sorted(self.t["day_plan"][0]["dishes"]))

    def _item(self, sim, kind, fresh=100):
        return {"id": sim.ids.new("I"), "kind": kind, "fresh": Fraction(fresh)}

    def test_gather_hold_handed_to_quan_as_v12_items_with_day_menu(self):
        """v1.2 (ADR-0003): Quán nhận đúng mảng cá thể {id, kind, fresh} như gather_end.inventory.items.

        QuanSim được thay bằng bản ghi lại tham số: phần đọc kho cá thể ở Quán là của TV3 (chưa xong),
        test này chỉ kiểm phần bàn giao của Day.
        """
        sim = self.sim()
        sim.sub.hold = [self._item(sim, "ca_loc"), self._item(sim, "bong_sung"), self._item(sim, "bong_sung")]
        with mock.patch("chonoi.sim.day.QuanSim") as quan:
            evs = sim.step(press("interact"))  # đứng ở bến -> docked
        self.assertEqual(sim.phase, "quan")
        end = dict(evs)["gather_end"]
        # bước cập bến vẫn hao tươi 1 tick ở giỏ: 100 - gather_decay_per_s / tick_hz
        fr = self.t["freshness"]
        f1 = fresh_to_num(Fraction(100) - Fraction(str(fr["gather_decay_per_s"])) / self.t["tick_hz"])
        expected = [{"id": "I1", "kind": "ca_loc", "fresh": f1}, {"id": "I2", "kind": "bong_sung", "fresh": f1},
                    {"id": "I3", "kind": "bong_sung", "fresh": f1}]
        self.assertEqual(end["inventory"], {"items": expected})
        kwargs = quan.call_args.kwargs
        self.assertEqual(kwargs["inventory"], expected)
        self.assertEqual(sorted(kwargs["day_dishes"]), sorted(self.t["day_plan"][0]["dishes"]))

    def test_faint_hands_empty_v12_inventory_and_quan_still_opens(self):
        sim = self.sim()
        sim.sub.hold = [self._item(sim, "ca_loc")]
        with mock.patch("chonoi.sim.day.QuanSim") as quan:
            sim.sub._finish("fainted", [])  # ngất: giỏ bị bỏ
            sim._open_quan([])
        self.assertEqual(sim.phase, "quan")
        self.assertEqual(quan.call_args.kwargs["inventory"], [])

    def test_item_ids_keep_increasing_across_days(self):
        sim = self.sim(days=2)
        first = self._item(sim, "ca_loc")
        self.assertEqual(first["id"], "I1")
        with mock.patch("chonoi.sim.day.QuanSim") as quan:
            quan.return_value.done, quan.return_value.money = True, 0
            quan.return_value.earned, quan.return_value.reputation = 0, 3.0
            sim.step(press("interact"))   # ngày 1: cập bến -> Quán (giả, kết thúc ngay)
            sim.step(IDLE)                # Quán xong -> Shop
            sim.step(IDLE)                # thả nút
            sim.step(press("interact"))   # rời Shop -> ngày 2
        self.assertEqual((sim.day, sim.phase), (2, "gather"))
        self.assertIs(sim.sub.ids, sim.ids)  # cùng IdAllocator qua các ngày
        self.assertEqual(sim.ids.new("I"), "I2")

    def test_money_and_reputation_carry_over_quan_starts_from_day_reputation(self):
        sim = self.sim(days=2)
        self.run_until(sim, "quan")
        sim.sub.money, sim.sub.earned, sim.sub.reputation = 100, 100, 3.5
        self.run_until(sim, "shop")
        self.assertEqual((sim.money, sim.earned, sim.reputation), (100, 100, 3.5))
        self.run_until(sim, "quan")
        self.assertEqual(sim.day, 2)
        self.assertEqual(sim.sub.reputation, 3.5)
        self.assertEqual(sim.money, 100)

    # --- Shop / nâng cấp --------------------------------------------------------
    def test_upgrade_takes_effect_next_day_only(self):
        sim = self.sim(days=2)
        self.run_until(sim, "shop")
        sim.wallet = 1000
        ev = sim.step(press("buy_oxygen"))
        price = self.t["shop"]["upgrades"]["oxygen"][0]["price"]
        self.assertIn(("upgrade_bought", {"upgrade": "oxygen", "level": 1, "price": price, "money": 1000 - price}), ev)
        self.assertEqual(sim.active_upgrades["oxygen"], 0)
        sim.step(press("interact"))  # rời Shop -> ngày 2
        self.assertEqual((sim.day, sim.phase), (2, "gather"))
        self.assertEqual(sim.active_upgrades["oxygen"], 1)
        level1 = self.t["shop"]["upgrades"]["oxygen"][0]["oxygen_max_s"]
        self.assertEqual(sim.sub.oxygen_max, int(round(level1 * 60)))
        self.assertEqual(self.t["gather"]["oxygen_max_s"], 30)  # tuning gốc không bị đổi

    def test_buy_without_money_or_past_max_level_fails(self):
        sim = self.sim()
        self.run_until(sim, "shop")
        self.assertIn(("buy_failed", {"upgrade": "hp", "reason": "money"}), sim.step(press("buy_hp")))
        sim.wallet = 10000
        sim.step(press("buy_hp"))
        sim.step(IDLE)
        sim.step(press("buy_hp"))
        sim.step(IDLE)
        self.assertEqual(sim.upgrades["hp"], 2)
        self.assertIn(("buy_failed", {"upgrade": "hp", "reason": "max_level"}), sim.step(press("buy_hp")))

    def test_shop_closes_after_max_ticks(self):
        sim = self.sim()
        self.run_until(sim, "shop")
        for _ in range(self.shop_ticks - 1):
            sim.step(IDLE)
        self.assertFalse(sim.done)
        ev = sim.step(IDLE)
        self.assertIn("shop_end", [n for n, _ in ev])
        self.assertTrue(sim.done)

    # --- pause -----------------------------------------------------------------
    def test_pause_freezes_sim_and_timers_resume_runs_same_step(self):
        sim = self.sim()
        sim.step(IDLE)
        sim_tick, left = sim.sim_tick, sim.time_left_ticks
        self.assertIn(("paused", {"day": 1, "phase": "gather"}), sim.step(press("pause")))
        for _ in range(30):
            sim.step(IDLE)
        self.assertEqual((sim.sim_tick, sim.time_left_ticks), (sim_tick, left))
        ev = sim.step(press("pause"))
        self.assertIn(("resumed", {"day": 1, "phase": "gather"}), ev)
        self.assertEqual((sim.sim_tick, sim.time_left_ticks), (sim_tick + 1, left - 1))


if __name__ == "__main__":
    unittest.main()
