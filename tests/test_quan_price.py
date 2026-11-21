"""v1.2 (ADR-0003, phần TV4): cook_started.items, base_price theo độ tươi, boa tính trên base_price."""

import math
import os
import tempfile
import unittest
from fractions import Fraction

from helpers import read_jsonl, run_headless, write_json

from chonoi.contract import load_contract
from chonoi.inputs import InputState
from chonoi.runner import Session

IDLE = InputState((0.0, 0.0), {}, set())


def item(item_id, kind, fresh=100):
    return {"id": item_id, "kind": kind, "fresh": fresh}


def waiting(dish, order="O1", table="T1", patience=None):
    c = {"id": "C1", "table_id": table, "order_id": order, "order_tick": 0, "dish_id": dish}
    if patience is not None:
        c["patience_ticks_left"] = patience
    return c


class QuanPrice(unittest.TestCase):
    def setUp(self):
        self.t = load_contract()["tuning"]
        self.menu = self.t["menu"]

    def sim(self, stock, customer):
        sc = {"stock": stock, "customers": [customer], "random_customers": False}
        return Session("quan", self.t, sc, 1).sim

    def cook_and_serve(self, sim):
        stove, table = sim.stoves[0], sim.tables[0]
        cook = []
        sim._stove_interact(stove, cook)
        stove.update(state="ready", cook_ticks_left=0)  # bỏ qua thời gian nấu
        sim._stove_interact(stove, [])
        served = []
        sim._table_interact(table, served)
        return dict(cook)["cook_started"], sim.customers[0]

    def test_base_price_floor_of_avg_fresh_and_tip_on_base_price(self):
        sim = self.sim([item("I1", "ca_loc", 50)], waiting("ca_loc_nuong_trui"))
        cook, c = self.cook_and_serve(sim)
        listed = self.menu["ca_loc_nuong_trui"]["price"]
        base = math.floor(Fraction(listed) * 50 / 100)
        self.assertEqual(cook["items"], [{"id": "I1", "kind": "ca_loc", "fresh": 50}])
        self.assertEqual(c["price"], base)
        self.assertEqual(c["tip"], math.floor(Fraction(base) * Fraction(str(self.t["quan"]["tip_rate"]))))
        self.assertLess(c["price"], listed)

    def test_items_sorted_by_kind_then_id_and_average_over_all_items(self):
        stock = [item("I10", "ca_linh", 100), item("I2", "ca_linh", 90), item("I3", "ca_linh", 80),
                 item("I1", "bong_dien_dien", 70)]
        sim = self.sim(stock, waiting("lau_ca_linh_dien_dien"))
        cook, c = self.cook_and_serve(sim)
        self.assertEqual([i["id"] for i in cook["items"]], ["I1", "I2", "I3", "I10"])
        self.assertEqual([i["kind"] for i in cook["items"]], ["bong_dien_dien"] + ["ca_linh"] * 3)
        avg = Fraction(100 + 90 + 80 + 70, 4)
        self.assertEqual(c["price"], math.floor(self.menu["lau_ca_linh_dien_dien"]["price"] * avg / 100))
        self.assertEqual(sim.stock, [])

    def test_floor_is_exact_on_freshness_grid(self):
        # 99.992 = 23998/240 (lưới độ tươi): 60 * 99.991666.../100 = 59.995 -> 59, không làm tròn lên 60
        sim = self.sim([item("I1", "ca_loc", 99.992)], waiting("ca_loc_nuong_trui"))
        _, c = self.cook_and_serve(sim)
        self.assertEqual(c["price"], 59)

    def test_fresh_items_keep_listed_price(self):
        sim = self.sim([item("I1", "ca_loc", 100)], waiting("ca_loc_nuong_trui"))
        _, c = self.cook_and_serve(sim)
        self.assertEqual(c["price"], self.menu["ca_loc_nuong_trui"]["price"])

    def test_no_tip_when_patience_low_even_with_base_price(self):
        full = int(self.t["quan"]["patience_s"] * self.t["tick_hz"])
        sim = self.sim([item("I1", "ca_loc", 80)], waiting("ca_loc_nuong_trui", patience=full // 4))
        _, c = self.cook_and_serve(sim)
        self.assertEqual(c["price"], math.floor(Fraction(60 * 80, 100)))
        self.assertEqual(c["tip"], 0)

    def test_paid_uses_base_price(self):
        sim = self.sim([item("I1", "ca_loc", 50)], waiting("ca_loc_nuong_trui"))
        _, c = self.cook_and_serve(sim)
        c["eat_ticks_left"] = 1
        evs = sim.step(IDLE)
        paid = dict(evs)["paid"]
        self.assertEqual((paid["price"], paid["tip"]), (c["price"], c["tip"]))
        self.assertEqual(sim.money, c["price"] + c["tip"])

    def test_headless_cook_started_items_use_fresh_at_consume_time(self):
        """Hộp đen: kho hao 1 tick ở Quán trước lượt bấm bếp, items mang độ tươi lúc tiêu."""
        sc = {"quan": {"stock": [item("I1", "ca_loc", 100)], "random_customers": False,
                       "player": {"pos": self.t["quan"]["stoves"][0]["pos"]},
                       "customers": [waiting("ca_loc_nuong_trui")]}}
        with tempfile.TemporaryDirectory() as d:
            scp = write_json(os.path.join(d, "sc.json"), sc)
            inp = write_json(os.path.join(d, "in.json"), {"frames": [{"tick": 0, "interact": True}]})
            outs = [os.path.join(d, f"{n}.jsonl") for n in "ab"]
            for o in outs:
                code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "5", "--scenario", scp,
                                         "--inputs", inp, "--out", o)
                self.assertEqual(code, 0, err)
            rows = read_jsonl(outs[0])
            with open(outs[0], "rb") as a, open(outs[1], "rb") as b:
                self.assertEqual(a.read(), b.read())
        cook, = [r for r in rows if r.get("name") == "cook_started"]
        decay = Fraction(str(self.t["freshness"]["quan_decay_per_s"])) / self.t["tick_hz"]
        f1 = 100 - decay
        self.assertEqual(cook["data"]["items"], [{"id": "I1", "kind": "ca_loc", "fresh": round(float(f1), 3)}])


if __name__ == "__main__":
    unittest.main()
