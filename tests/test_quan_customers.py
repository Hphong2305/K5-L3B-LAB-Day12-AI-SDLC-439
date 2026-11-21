import unittest

from chonoi.contract import load_contract
from chonoi.errors import BadInput
from chonoi.inputs import LiveInputs
from chonoi.runner import Session


def ingredient(item_id, kind="bong_sung", fresh=100):
    return {"id": item_id, "kind": kind, "fresh": fresh}


class QuanCustomers(unittest.TestCase):
    def setUp(self):
        self.tuning = load_contract()["tuning"]
        self.tuning["quan"]["first_customer_tick"] = 1

    def test_arrival_reserves_recipe_without_consuming_stock(self):
        stock = [ingredient("I10", fresh=80), ingredient("I3", fresh=90),
                 ingredient("I2", fresh=80), ingredient("I1", fresh=70)]
        session = Session("quan", self.tuning, {"stock": stock}, 42)
        inp = LiveInputs().advance()
        event, = session.step(inp)
        customer, = session.sim.customers
        self.assertEqual(event["name"], "customer_arrived")
        self.assertEqual(event["tick"], 1)
        self.assertEqual(event["data"]["order_id"], customer["order_id"])
        self.assertEqual(customer["dish_id"], "goi_bong_sung")
        self.assertEqual(customer["patience_ticks_left"], session.sim.patience_ticks)
        self.assertEqual(customer["reserved"], ["I2", "I3"])
        self.assertEqual([item["id"] for item in session.snapshot()["stock"]], ["I1", "I2", "I3", "I10"])
        self.assertEqual([item["id"] for item in session.sim.available_stock()], ["I1", "I10"])
        self.assertEqual(session.step(inp), [])
        self.assertEqual(customer["patience_ticks_left"], session.sim.patience_ticks - 1)

    def test_insufficient_stock_produces_no_dish(self):
        session = Session("quan", self.tuning, {"stock": [ingredient("I1")]}, 42)
        event, = session.step(LiveInputs().advance())
        self.assertEqual(event["name"], "no_dish")
        self.assertEqual(session.sim.customers, [])

    def test_fixture_leaves_at_deadline_and_releases_stock(self):
        scenario = {
            "stock": [ingredient("I1"), ingredient("I2")],
            "random_customers": False,
            "customers": [{"id": "C7", "table_id": "T1", "order_id": "O7",
                           "dish_id": "goi_bong_sung", "patience_ticks_left": 2}],
        }
        session = Session("quan", self.tuning, scenario, 42)
        inp = LiveInputs().advance()
        self.assertEqual(session.sim.available_stock(), [])
        self.assertEqual(session.step(inp), [])
        self.assertEqual(session.sim.customers[0]["patience_ticks_left"], 1)
        event, = session.step(inp)
        self.assertEqual(event["name"], "customer_left")
        self.assertEqual([item["id"] for item in session.sim.available_stock()], ["I1", "I2"])
        self.assertEqual(len(session.snapshot()["stock"]), 2)
        self.assertIsNone(session.snapshot()["tables"][0]["customer_id"])

    def test_fixture_reservation_cannot_exceed_stock(self):
        scenario = {"customers": [{"id": "C1", "table_id": "T1", "dish_id": "goi_bong_sung"}]}
        with self.assertRaises(BadInput):
            Session("quan", self.tuning, scenario, 42)

    def test_invalid_items_and_duplicate_reservations(self):
        item = ingredient("I1", "ca_loc")
        for stock in ({"ca_loc": 1}, [item, item], [dict(item, fresh=True)],
                      [dict(item, fresh=101)], [dict(item, fresh=float("nan"))]):
            with self.subTest(stock=stock), self.assertRaises(BadInput):
                Session("quan", self.tuning, {"stock": stock}, 42)
        customer = {"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                    "reserved": ["I1"]}
        scenario = {"stock": [item], "customers": [customer, dict(customer, id="C2", table_id="T2")]}
        with self.assertRaises(BadInput):
            Session("quan", self.tuning, scenario, 42)

    def test_spoilage_releases_whole_reservation_and_uses_freshest_replacements(self):
        scenario = {
            "stock": [ingredient("I1", fresh=30), ingredient("I2", fresh=70),
                      ingredient("I3", fresh=80), ingredient("I4", fresh=90)],
            "random_customers": False,
            "customers": [{"id": "C1", "table_id": "T1", "order_id": "O1",
                           "dish_id": "goi_bong_sung", "reserved": ["I1", "I2"]}],
        }
        session = Session("quan", self.tuning, scenario, 42)
        self.assertEqual(session.snapshot()["stock"][0]["fresh"], 30)
        event, = session.step(LiveInputs().advance())
        self.assertEqual(event["name"], "spoiled")
        self.assertEqual(event["data"]["item_id"], "I1")
        self.assertEqual(session.snapshot()["customers"][0]["reserved"], ["I3", "I4"])
        sim = session.sim
        sim._stove_interact(sim.stoves[0], [])
        self.assertEqual([item["id"] for item in sim.stock], ["I1", "I2"])
        self.assertEqual(sim.customers[0]["reserved"], [])

    def test_one_retry_per_order_and_spoiled_items_cannot_be_cooked(self):
        scenario = {
            "stock": [ingredient("I1", "ca_loc", 30), ingredient("I2", "ca_loc", 30.004),
                      ingredient("I3", "ca_loc")],
            "random_customers": False,
            "customers": [
                {"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui", "reserved": ["I1"]},
                {"id": "C2", "table_id": "T2", "dish_id": "ca_loc_nuong_trui",
                 "reserved": ["I3"], "patience_ticks_left": 2},
            ],
        }
        session = Session("quan", self.tuning, scenario, 42)
        inp = LiveInputs().advance()
        session.step(inp)
        self.assertEqual(session.snapshot()["stock"][1]["fresh"], 30)
        self.assertEqual(session.sim.customers[0]["reserved"], ["I2"])
        session.step(inp)
        self.assertEqual(session.sim.customers[0]["state"], "unfulfillable")
        self.assertEqual(session.sim.customers[0]["reserved"], [])
        self.assertEqual([item["id"] for item in session.sim.available_stock()], ["I3"])
        self.assertIsNone(session.sim._next_order())

    def test_retry_with_insufficient_stock_marks_order_unfulfillable(self):
        scenario = {
            "stock": [ingredient("I1", fresh=30), ingredient("I2")],
            "random_customers": False,
            "customers": [{"id": "C1", "table_id": "T1", "dish_id": "goi_bong_sung"}],
        }
        session = Session("quan", self.tuning, scenario, 42)
        session.step(LiveInputs().advance())
        customer, = session.sim.customers
        self.assertEqual((customer["state"], customer["reserved"]), ("unfulfillable", []))
        self.assertEqual([item["id"] for item in session.sim.available_stock()], ["I2"])
