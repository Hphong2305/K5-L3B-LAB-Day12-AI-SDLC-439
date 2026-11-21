"""Buổi sáng — Lặn & Hái (`gather`). KHUNG: bơi, chặn mép, đồng hồ, cập bến, xuất kho.

Mặt cắt dòng sông nhìn NGANG: vị trí `[x, d]` (x sang phải, `d` độ sâu hướng xuống, d = 0 là mặt nước).
`move = [x, d]`: thành phần thứ hai DƯƠNG = bơi xuống. Hướng mặt là góc từ +x, dương = xuống.

Đã làm sẵn để smoke test chạy được: bơi + tăng/giảm tốc, chặn mép (d không âm), đồng hồ và hết giờ,
cập bến (`interact` trong vùng bến -> `gather_end` reason `docked`), xuất kho, snapshot đầy đủ trường gather.

Nhóm viết tiếp (đúng thứ tự một bước trong PRD mục 13.8, "Gather"):
  TODO(nhóm, lát 1): bơi + oxy + biên + giỏ
      - oxy: dưới nước (d > surface_depth) trừ 1 tick/tick, mặt nước hồi oxygen_refill_per_tick, kẹp [0, max]
      - ngạt: oxy = 0 và đang dưới nước -> đếm zero_oxy_ticks, đủ choke_interval_ticks thì -1 Máu (choke)
      - Máu về 0 -> ngất (faint, gather_end reason `fainted`, mất toàn bộ giỏ, kho rỗng)
      - sự kiện dive / surface / oxygen_empty / choke / faint
      - giỏ: thứ tự nhặt (LIFO), sức chứa hold_capacity
  Lát 2: hái nút ở mặt nước, bắt cá dưới nước, ưu tiên cập bến và xuất kho.
      - hành động chọn mục tiêu gần nhất trong bán kính, hòa theo ID
      - đủ chỗ mới nhận trọn yield; nút regrow và cá có hồi chiêu theo tuning
      - runner ghi kho nguyên tử đúng một lần sau gather_end
Các tính năng của phase sau chưa nằm trong khung này.
"""

import math

from ..ids import id_key, sort_by_id
from ..inventory import hold_to_items
from .ramp import ramp_velocity

TICK = 60.0
AXES = ("x", "d")


class GatherSim:
    mode = "gather"
    phase = "gather"

    def __init__(self, tuning, scenario, streams, ids):
        t = tuning["gather"]
        self.t = t
        self.rng = streams
        self.ids = ids
        p = scenario.get("player", {})
        self.pos = [float(c) for c in p.get("pos", t["start_pos"])]
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        self.heading = float(p.get("heading_deg", t["start_heading_deg"]))
        self.oxygen_max = int(round(t["oxygen_max_s"] * TICK))
        self.oxygen_ticks = p.get("oxygen_ticks", self.oxygen_max)
        self.hp = p.get("hp", t["hp_max"])
        self.zero_oxy_ticks = p.get("zero_oxy_ticks", 0)
        self.invuln_ticks = p.get("invuln_ticks", 0)
        self.catch_cd_ticks = p.get("catch_cd_ticks", 0)
        self.hold = list(scenario.get("hold", []))  # thứ tự nhặt, cuối mảng là mới nhất
        self.time_left_ticks = scenario.get("time_left_ticks", int(round(t["duration_s"] * TICK)))
        # nút và đàn cá: scenario THAY THẾ danh sách mặc định; random_fish=false tắt cá mặc định
        src_nodes = scenario["nodes"] if "nodes" in scenario else t["nodes"]
        self.nodes = [{"id": n["id"], "kind": n["kind"], "pos": [float(c) for c in n["pos"]],
                       "regrow_ticks": n.get("regrow_ticks", 0)} for n in src_nodes]
        if "fish" in scenario:
            src_fish = scenario["fish"]
        elif scenario.get("random_fish", True):
            src_fish = t.get("fish_initial", [])
            if isinstance(src_fish, int):
                src_fish = [
                    {"id": f"F{i+1}", "kind": ("ca_linh", "ca_loc", "ca_keo")[i % 3],
                     "pos": [15.0 + (i % 6) * 15.0, 5.0 + (i // 3) * 5.0], "heading_deg": 0}
                    for i in range(src_fish)
                ]
        else:
            src_fish = []
        # Đàn cá đứng yên ở phase này. Cá bơi / sinh thêm do TV2 triển khai.
        self.fish = [{"id": f["id"], "kind": f["kind"], "pos": [float(c) for c in f["pos"]],
                      "heading_deg": f.get("heading_deg", 0)} for f in src_fish]

        # Thủy quái (Cá Sấu) — TV1 phụ trách
        self.day = scenario.get("day", 1)
        m_cfg = t.get("monsters", {})
        self.monsters_cfg = m_cfg
        self.monsters = []
        if "monsters" in scenario:
            for m in scenario["monsters"]:
                wps = [[float(c) for c in wp] for wp in m.get("waypoints", [[float(c) for c in m["pos"]], [float(c) for c in m["pos"]]])]
                self.monsters.append({
                    "id": m["id"],
                    "kind": m.get("kind", "ca_sau"),
                    "pos": [float(c) for c in m["pos"]],
                    "waypoints": wps,
                    "target_idx": m.get("target_idx", 1),
                    "state": m.get("state", "patrol"),
                    "state_ticks_left": m.get("state_ticks_left", 0),
                    "recoil_dir": [float(c) for c in m["recoil_dir"]] if m.get("recoil_dir") else None,
                })
        else:
            spawns = m_cfg.get("spawns", [])
            for s in spawns:
                if s.get("from_day", 1) <= self.day:
                    wps = [[float(c) for c in wp] for wp in s["waypoints"]]
                    self.monsters.append({
                        "id": s["id"],
                        "kind": s["kind"],
                        "pos": [float(c) for c in s["pos"]],
                        "waypoints": wps,
                        "target_idx": 1,
                        "state": "patrol",
                        "state_ticks_left": 0,
                        "recoil_dir": None,
                    })

        for coll in (self.nodes, self.fish, self.monsters):
            for e in coll:
                ids.reserve(e["id"])
        self.money = 0
        self.earned = 0
        self.reputation = tuning["quan"]["reputation_initial"]
        self.done = False
        self.reason = None

    # --- giao diện cho runner -------------------------------------------------
    def inventory_items(self) -> dict:
        return hold_to_items(self.hold)

    def snapshot(self) -> dict:
        return {
            "player": {"pos": self.pos, "vel": self.vel, "heading_deg": self.heading,
                       "oxygen_ticks": self.oxygen_ticks, "oxygen_max_ticks": self.oxygen_max,
                       "hp": self.hp, "hp_max": self.t["hp_max"], "zero_oxy_ticks": self.zero_oxy_ticks,
                       "invuln_ticks": self.invuln_ticks, "catch_cd_ticks": self.catch_cd_ticks,
                       "at_surface": self._at_surface()},
            "hold": self.hold, "hold_count": len(self.hold),
            "hold_capacity": self.t["hold_capacity"],
            "nodes": [{"id": n["id"], "pos": n["pos"], "kind": n["kind"],
                       "ready": n["regrow_ticks"] == 0, "regrow_ticks": n["regrow_ticks"]}
                      for n in sort_by_id(self.nodes)],
            "fish": [{"id": f["id"], "pos": f["pos"], "kind": f["kind"], "heading_deg": f.get("heading_deg", 0)}
                     for f in sort_by_id(self.fish)],
            "monsters": [{"id": m["id"], "kind": m["kind"], "pos": m["pos"],
                          "waypoints": m["waypoints"], "target_idx": m["target_idx"],
                          "state": m["state"], "state_ticks_left": m["state_ticks_left"],
                          "recoil_dir": m["recoil_dir"]}
                         for m in sort_by_id(self.monsters)],
        }

    # --- một bước ---------------------------------------------------------------
    def step(self, inp):
        events = []
        # 1. đồng hồ và hàng có sẵn: giảm bộ đếm, nút mọc lại
        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        self.invuln_ticks = max(0, self.invuln_ticks - 1)
        self.catch_cd_ticks = max(0, self.catch_cd_ticks - 1)
        for n in sort_by_id(self.nodes):
            if n["regrow_ticks"] > 0:
                n["regrow_ticks"] -= 1
                if n["regrow_ticks"] == 0:
                    events.append(("node_regrown", {"node_id": n["id"]}))
        # 2. bơi + chặn mép
        was_surface = self._at_surface()
        self._move(inp)
        now_surface = self._at_surface()

        # so phân vùng đầu/cuối bước -> dive / surface (data: pos)
        if was_surface and not now_surface:
            events.append(("dive", {"pos": list(self.pos)}))
        elif not was_surface and now_surface:
            events.append(("surface", {"pos": list(self.pos)}))

        # oxy theo d CUỐI bước (mặt nước hồi, dưới nước trừ), oxygen_empty khi từ dương xuống 0
        if now_surface:
            self.oxygen_ticks = min(self.oxygen_max, self.oxygen_ticks + self.t["oxygen_refill_per_tick"])
            self.zero_oxy_ticks = 0
        else:
            if self.oxygen_ticks > 0:
                self.oxygen_ticks -= 1
                if self.oxygen_ticks == 0:
                    events.append(("oxygen_empty", {}))
            else:
                self.zero_oxy_ticks += 1
                if self.zero_oxy_ticks >= self.t["choke_interval_ticks"]:
                    self.zero_oxy_ticks = 0
                    self.hp -= 1
                    events.append(("choke", {"hp": self.hp}))
                    if self.hp <= 0:
                        lost = list(reversed(self.hold))
                        self.hold = []
                        events.append(("faint", {"cause": "choke", "hp": 0, "lost": lost}))
                        self._finish("fainted", events)
                        return events
        # 3. Quái update theo ID, xét tối đa một hit (TV1)
        self._update_monsters()
        if self._check_monster_hit(events):
            return events

        # 4. interact: bến trước, rồi hái (TV2)
        if inp.pressed("interact"):
            if self._in_dock():
                self._finish("docked", events)
                return events
            if self._at_surface():
                self._try_gather(events)
        # 5. bắt cá (TV2)
        if inp.pressed("catch"):
            self._try_catch(events)
        # 6. hết giờ
        if self.time_left_ticks <= 0:
            self._finish("time", events)
            return events

        # 7. Khi còn giờ: cá bơi, cá sinh (TV2)
        self._move_fish()
        self._spawn_fish(events)
        return events

    # --- tiện ích ---------------------------------------------------------------
    def _at_surface(self) -> bool:
        return self.pos[1] <= self.t["surface_depth"]

    def _in_dock(self) -> bool:
        return math.dist(self.pos, self.t["dock_pos"]) <= self.t["dock_radius"]

    def _finish(self, reason, events):
        if reason == "fainted":
            self.hold.clear()
        self.done = True
        self.reason = reason
        events.append(("gather_end", {"reason": reason, "inventory": {"items": self.inventory_items()}}))

    def _try_gather(self, events):
        radius = self.t["interact_radius"]
        nearby = [n for n in self.nodes
                  if n["regrow_ticks"] == 0 and math.dist(self.pos, n["pos"]) <= radius]
        if not nearby:
            return
        node = min(nearby, key=lambda n: (math.dist(self.pos, n["pos"]), id_key(n["id"])))
        amount = self.t["node_yield"]
        if len(self.hold) + amount > self.t["hold_capacity"]:
            events.append(("hold_full", {"source": "node", "source_id": node["id"]}))
            return
        self.hold.extend([node["kind"]] * amount)
        node["regrow_ticks"] = int(round(self.t["regrow_s"] * TICK))
        events.append(("gather", {"node_id": node["id"], "kind": node["kind"], "yield": amount}))

    def _try_catch(self, events):
        if self._at_surface() or self.catch_cd_ticks > 0:
            return
        radius = self.t["catch_radius"]
        nearby = [f for f in self.fish if math.dist(self.pos, f["pos"]) <= radius]
        if not nearby:
            return
        fish = min(nearby, key=lambda f: (math.dist(self.pos, f["pos"]), id_key(f["id"])))
        amount = self.t["fish_yield"][fish["kind"]]
        if len(self.hold) + amount > self.t["hold_capacity"]:
            events.append(("hold_full", {"source": "fish", "source_id": fish["id"]}))
            return
        self.hold.extend([fish["kind"]] * amount)
        self.catch_cd_ticks = int(round(self.t["catch_cooldown_s"] * TICK))
        events.append(("fish_caught", {"fish_id": fish["id"], "kind": fish["kind"], "yield": amount}))

    def _move(self, inp):
        speed = self.t["swim_speed"]
        mx, md = inp.move
        self.vel = ramp_velocity(self, (mx * speed, md * speed), int(self.t["ramp_max_ticks"]))
        if (mx, md) != (0.0, 0.0):
            self.heading = math.degrees(math.atan2(md, mx)) % 360
        b = self.t["bounds"]
        for i, axis in enumerate(AXES):
            self.pos[i] += self.vel[i] / TICK
            lo, hi = b[axis]
            if self.pos[i] <= lo:
                self.pos[i] = lo
                self.vel[i] = max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i] = hi
                self.vel[i] = min(0.0, self.vel[i])

    # --- Thủy quái (Cá Sấu) — TV1 ----------------------------------------------
    def _update_monsters(self):
        species_cfg = self.monsters_cfg.get("species", {}).get("ca_sau", {})
        patrol_speed = species_cfg.get("patrol_speed", 1.0)
        chase_speed = species_cfg.get("chase_speed", 3.0)
        detect_radius = species_cfg.get("detect_radius", 10.0)
        exit_radius = species_cfg.get("exit_radius", 16.0)
        depths = species_cfg.get("depths", [10, 30])
        bounds_x = self.t["bounds"]["x"]

        for m in sort_by_id(self.monsters):
            state = m["state"]
            if state == "recoil":
                m["state_ticks_left"] -= 1
                recoil_speed = 2.0  # mỗi bước 2/60 m
                rdir = m.get("recoil_dir") or [1.0, 0.0]
                m["pos"][0] += rdir[0] * (recoil_speed / TICK)
                m["pos"][1] += rdir[1] * (recoil_speed / TICK)
                m["pos"][0] = max(bounds_x[0], min(bounds_x[1], m["pos"][0]))
                m["pos"][1] = max(depths[0], min(depths[1], m["pos"][1]))
                if m["state_ticks_left"] <= 0:
                    m["state"] = "patrol"
                    m["recoil_dir"] = None

            elif state == "chase":
                dist_to_p = math.dist(m["pos"], self.pos)
                if dist_to_p > exit_radius or self.pos[1] < depths[0]:
                    m["state"] = "patrol"
                else:
                    dx = self.pos[0] - m["pos"][0]
                    dd = self.pos[1] - m["pos"][1]
                    dist_to_p = math.hypot(dx, dd)
                    if dist_to_p > 0:
                        step_d = min(dist_to_p, chase_speed / TICK)
                        m["pos"][0] += (dx / dist_to_p) * step_d
                        m["pos"][1] += (dd / dist_to_p) * step_d
                    m["pos"][0] = max(bounds_x[0], min(bounds_x[1], m["pos"][0]))
                    m["pos"][1] = max(depths[0], min(depths[1], m["pos"][1]))

            if m["state"] == "patrol":
                dist_to_p = math.dist(m["pos"], self.pos)
                if self.pos[1] >= depths[0] and dist_to_p <= detect_radius:
                    m["state"] = "chase"
                    dx = self.pos[0] - m["pos"][0]
                    dd = self.pos[1] - m["pos"][1]
                    dist_to_p = math.hypot(dx, dd)
                    if dist_to_p > 0:
                        step_d = min(dist_to_p, chase_speed / TICK)
                        m["pos"][0] += (dx / dist_to_p) * step_d
                        m["pos"][1] += (dd / dist_to_p) * step_d
                    m["pos"][0] = max(bounds_x[0], min(bounds_x[1], m["pos"][0]))
                    m["pos"][1] = max(depths[0], min(depths[1], m["pos"][1]))
                else:
                    target = m["waypoints"][m["target_idx"]]
                    dx = target[0] - m["pos"][0]
                    dd = target[1] - m["pos"][1]
                    dist_tgt = math.hypot(dx, dd)
                    step_d = patrol_speed / TICK
                    if dist_tgt <= step_d:
                        m["pos"][0] = target[0]
                        m["pos"][1] = target[1]
                        m["target_idx"] = 1 - m["target_idx"]
                    else:
                        m["pos"][0] += (dx / dist_tgt) * step_d
                        m["pos"][1] += (dd / dist_tgt) * step_d
                    m["pos"][0] = max(bounds_x[0], min(bounds_x[1], m["pos"][0]))
                    m["pos"][1] = max(depths[0], min(depths[1], m["pos"][1]))

    def _check_monster_hit(self, events) -> bool:
        if self.invuln_ticks > 0 or self.pos[1] < 10.0:
            return False

        species_cfg = self.monsters_cfg.get("species", {}).get("ca_sau", {})
        hit_radius = species_cfg.get("hit_radius", 1.5)

        candidates = [m for m in self.monsters
                      if m["state"] != "recoil" and math.dist(self.pos, m["pos"]) <= hit_radius]
        if not candidates:
            return False

        m = min(candidates, key=lambda mon: (math.dist(self.pos, mon["pos"]), id_key(mon["id"])))

        self.hp -= 1
        lost_count = len(self.hold) // 2
        lost = []
        for _ in range(lost_count):
            lost.append(self.hold.pop())

        self.invuln_ticks = self.monsters_cfg.get("invuln_ticks", 90)

        events.append(("monster_hit", {
            "monster_id": m["id"],
            "hp": self.hp,
            "lost": lost,
            "pos": list(self.pos),
        }))

        dx = m["pos"][0] - self.pos[0]
        dd = m["pos"][1] - self.pos[1]
        dist_mp = math.hypot(dx, dd)
        if dist_mp == 0:
            recoil_dir = [1.0, 0.0]
        else:
            recoil_dir = [dx / dist_mp, dd / dist_mp]

        m["state"] = "recoil"
        m["state_ticks_left"] = species_cfg.get("recoil_ticks", 60)
        m["recoil_dir"] = recoil_dir

        if self.hp <= 0:
            remaining_lost = list(reversed(self.hold))
            self.hold = []
            events.append(("faint", {"cause": "monster", "hp": 0, "lost": remaining_lost}))
            self._finish("fainted", events)
            return True

        return False

    # Điểm nối cho TV2 triển khai cá bơi và cá sinh
    def _move_fish(self):
        pass

    def _spawn_fish(self, events):
        pass
