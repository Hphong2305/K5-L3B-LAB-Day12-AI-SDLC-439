"""Buổi tối — Mở Quán. KHUNG: đi lại, chặn biên, đồng hồ, kho nạp từ file/scenario.

Nhóm viết tiếp (PRD-0 mục F, Quán):
  TODO(nhóm, lát 4): interact tại bếp/bàn (cook_started, dish_ready, dish_picked, served),
                     ăn xong trả tiền (paid), boa, uy tín, hết ca (quan_end).
"""

from ..errors import BadInput
from ..ids import sort_by_id
from ..inventory import validate_items
from .ramp import ramp_velocity

TICK = 60.0


class QuanSim:
    mode = "quan"
    phase = "quan"

    def __init__(self, tuning, scenario, streams, ids, inventory=None):
        t = tuning["quan"]
        self.t = t
        self.menu = tuning["menu"]
        self.rng = streams
        self.ids = ids
        self.tick = 0
        tick_hz = tuning["tick_hz"]
        self.patience_ticks = round(t["patience_s"] * tick_hz)
        self.customer_interval_ticks = round(t["customer_interval_s"] * tick_hz)
        self.random_customers = scenario.get("random_customers", True)
        if not isinstance(self.random_customers, bool):
            raise BadInput("random_customers phải là boolean")
        p = scenario.get("player", {})
        self.pos = list(p.get("pos", t["start_pos"]))
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        # kho: --inventory HOẶC scenario.stock (cả hai -> cli đã báo mã 2)
        self.stock = dict(inventory if inventory is not None else scenario.get("stock", {}))
        self.hand = scenario.get("hand")
        self.time_left_ticks = scenario.get("time_left_ticks", int(round(t["duration_s"] * 60)))
        self.reputation = scenario.get("reputation", t["reputation_initial"])
        self.stoves = [dict(s, state=s.get("state", "idle"), dish=s.get("dish"),
                            cook_ticks_left=s.get("cook_ticks_left", 0), ready_ticks=s.get("ready_ticks", 0))
                       for s in self._merge(t["stoves"], scenario.get("stoves", []))]
        self.tables = self._merge(t["tables"], scenario.get("tables", []))
        self.customers = self._load_customers(scenario.get("customers", []))
        if any(amount < 0 for amount in self.available_stock().values()):
            raise BadInput("nguyên liệu giữ chỗ vượt quá kho")
        self.money = 0
        self.earned = 0
        self.shift_earned = 0
        self.done = False
        self.reason = None

    @staticmethod
    def _merge(defaults, updates):
        by_id = {d["id"]: dict(d) for d in defaults}
        for u in updates:
            if u["id"] not in by_id:
                raise BadInput(f"id bếp/bàn không tồn tại: {u['id']}")
            by_id[u["id"]].update(u)
        return sort_by_id(list(by_id.values()))

    def _load_customers(self, fixtures):
        customers = []
        for fixture in sort_by_id(fixtures):
            customer = dict(fixture)
            customer.setdefault("state", "waiting")
            customer.setdefault("patience_ticks_left", self.patience_ticks)
            patience = customer["patience_ticks_left"]
            if type(patience) is not int or patience < 0:
                raise BadInput("patience_ticks_left phải là số nguyên không âm")
            dish_id = customer.get("dish_id")
            recipe = {}
            if dish_id is not None:
                if not isinstance(dish_id, str) or dish_id not in self.menu:
                    raise BadInput(f"mã món không hợp lệ: {dish_id!r}")
                if customer["state"] == "waiting":
                    recipe = self.menu[dish_id]["recipe"]
            customer["reserved"] = validate_items(customer.get("reserved", recipe))
            if dish_id is not None and customer["reserved"] != recipe:
                raise BadInput(f"giữ chỗ không khớp đơn của khách {customer['id']}")
            self.ids.reserve(customer["id"])
            order_id = customer.get("order_id")
            if order_id is not None:
                if not isinstance(order_id, str) or not order_id:
                    raise BadInput("order_id phải là chuỗi khác rỗng")
                self.ids.reserve(order_id)
            customers.append(customer)
        return customers

    def available_stock(self):
        available = dict(self.stock)
        for customer in self.customers:
            for kind, amount in customer["reserved"].items():
                available[kind] = available.get(kind, 0) - amount
        return available

    def snapshot(self) -> dict:
        occupied = {c["table_id"]: c["id"] for c in self.customers}
        return {
            "player": {"pos": self.pos},
            "stock": {k: self.stock[k] for k in sorted(self.stock) if self.stock[k] > 0},
            "hand": self.hand,
            "stoves": [{k: s.get(k) for k in ("id", "pos", "state", "dish", "cook_ticks_left", "ready_ticks")}
                       for s in self.stoves],
            "tables": [{"id": tb["id"], "pos": tb["pos"], "customer_id": occupied.get(tb["id"])} for tb in self.tables],
            "customers": sort_by_id(self.customers),
        }

    def step(self, inp):
        events = []
        self.tick += 1
        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        self._update_customer_patience(events)
        # TODO(nhóm, lát 4): cập nhật bếp, thời gian ăn và thanh toán.
        self._move(inp)
        # TODO(nhóm): tối đa MỘT interact, chọn đối tượng theo (khoảng cách, bếp trước bàn, id).
        self._spawn_customer(events)
        if self.time_left_ticks <= 0:
            self.done = True
            self.reason = "time"
            events.append(("quan_end", {"reason": "time", "money": self.money, "earned": self.earned,
                                        "shift_earned": self.shift_earned, "reputation": self.reputation}))
        return events

    def _update_customer_patience(self, events):
        for customer in sort_by_id(self.customers):
            if customer["state"] not in ("waiting", "assigned"):
                continue
            customer["patience_ticks_left"] = max(0, customer["patience_ticks_left"] - 1)
            if customer["patience_ticks_left"]:
                continue
            customer["reserved"].clear()
            self.customers.remove(customer)
            self.reputation = max(self.t["reputation_min"],
                                  self.reputation + self.t["left_reputation_delta"])
            events.append(("customer_left", {"customer_id": customer["id"],
                                             "order_id": customer.get("order_id"),
                                             "table_id": customer["table_id"]}))

    def _spawn_customer(self, events):
        elapsed = self.tick - self.t["first_customer_tick"]
        if not self.random_customers or elapsed < 0 or elapsed % self.customer_interval_ticks:
            return
        occupied = {customer["table_id"] for customer in self.customers}
        table = next((table for table in self.tables if table["id"] not in occupied), None)
        if table is None:
            return
        available = self.available_stock()
        dishes = [dish_id for dish_id, dish in sorted(self.menu.items())
                  if all(available.get(kind, 0) >= amount for kind, amount in dish["recipe"].items())]
        if not dishes:
            events.append(("no_dish", {"table_id": table["id"]}))
            return
        dish_id = self.rng.get("customer_menu").choice(dishes)
        customer = {
            "id": self.ids.new("C"),
            "table_id": table["id"],
            "dish_id": dish_id,
            "order_id": self.ids.new("O"),
            "order_tick": self.tick,
            "state": "waiting",
            "patience_ticks_left": self.patience_ticks,
            "reserved": dict(self.menu[dish_id]["recipe"]),
        }
        self.customers.append(customer)
        events.append(("customer_arrived", {"customer_id": customer["id"],
                                            "table_id": customer["table_id"],
                                            "order_id": customer["order_id"],
                                            "dish_id": dish_id}))

    def _move(self, inp):
        speed = self.t["walk_speed"]
        mx, mz = inp.move
        self.vel = ramp_velocity(self, (mx * speed, mz * speed), int(self.t.get("ramp_max_ticks", 6)))
        b = self.t["bounds"]
        for i, axis in enumerate(("x", "z")):
            self.pos[i] += self.vel[i] / TICK
            lo, hi = b[axis]
            if self.pos[i] <= lo:
                self.pos[i], self.vel[i] = lo, max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i], self.vel[i] = hi, min(0.0, self.vel[i])
