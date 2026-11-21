# CHANGELOG

## [v1.0.0 — Contract v1.3 — Phase 4: Phát hành] — 2026-11-21

Không đổi gameplay, tuning, schema kho hay JSONL của v1.2.

### Thêm
- Manifest `contract_version: "1.3"`, `bench_cmd: python3 -m chonoi.bench`, `soak_cmd: python3 -m chonoi.soak`;
  `run_cmd` chơi trọn vòng ngày `python3 -m chonoi.live --mode day --days 5`.
- **Benchmark có render thật** (`chonoi/bench.py`): cửa sổ tkinter 1280×720, cảnh Gather lõi ngày 1, warm-up 3 s,
  đo `--duration` giây; `bench.json` đúng 5 trường `avg_fps`, `p1_low_fps`, `frames`, `measured_s`, `load_ms`.
- **Soak** (`chonoi/soak.py`): N ngày trong một tiến trình, ngày 6..N lặp kế hoạch D1..D5, giữ tiền/uy tín/nâng cấp/ID
  xuyên ngày; `soak.json` gồm `days`, `days_completed`, `crashes`, `results[{day, earned, reputation, score}]`, `duration_s`.
- **Cảnh báo chữ + biểu tượng** trong client: 🐊 Cá Sấu gần, 🫧 oxy sắp hết, 😠 khách sắp giận; **tương phản cao**
  (phím H / `?contrast=high`). Chơi mode `day` trên trình duyệt (Sáng → Tối → Shop, tạm dừng, mua nâng cấp).
- `LICENSE` (MIT cho phần nhóm viết), `CREDITS.md`, README chạy từ clone sạch bằng 3 lệnh, release notes.

### Đổi
- `DaySim(..., cycle_plans=True)` chỉ dùng cho soak; `--mode day --days` vẫn 1..5.
- `tests/test_phase3_qa.py`: điều kiện chạy đổi từ `version == "1.2"` sang `version >= 1.2` để test P3 không bị bỏ qua ở v1.3.

## [Contract v1.2 — Phase 3: Mùa Nước Nổi] — 2026-11-21

### ⚠️ Breaking Changes (Thay đổi không tương thích ngược so với v1.0 / v1.1)
1. **Schema File Kho (`--inventory-out` / `--inventory`) & `gather_end.data.inventory`:**
   - **Trước (v1.0–v1.1):** Kho đếm theo loại `{"items": {"ca_linh": 3, "ca_loc": 1}}`, kho rỗng `{"items": {}}`.
   - **Mới (v1.2):** Kho cá thể `{"items": [{"id": "I1", "kind": "ca_linh", "fresh": 100}, {"id": "I2", "kind": "ca_loc", "fresh": 97.5}]}`, kho rỗng `{"items": []}`.
   - File kho đếm hoặc sai schema / `id` trùng / `kind` lạ / `fresh` ngoài `[0, 100]` bị từ chối với mã thoát `2` (`BadInput`).
2. **Schema Scenario & Snapshot (`gather.hold`, `quan.stock`, `customers[].reserved`):**
   - `gather.hold`: Từ mảng chuỗi mã nguyên liệu `["ca_loc", "bong_sung"]` chuyển sang mảng cá thể `[{"id": "I1", "kind": "ca_loc", "fresh": 100}, ...]`.
   - `quan.stock`: Từ object đếm `{"bong_sung": 2}` chuyển sang mảng cá thể `[{"id": "I1", "kind": "bong_sung", "fresh": 100}, ...]`.
   - `customers[].reserved`: Từ object đếm `{"bong_sung": 2}` chuyển sang mảng ID cá thể `["I1", "I2"]`.
3. **Payload sự kiện `monster_hit`, `faint`, `cook_started`:**
   - `lost` trong `monster_hit` và `faint`: Mảng các cá thể `{id, kind, fresh}` theo thứ tự bỏ LIFO.
   - `cook_started.data.items`: Mảng các cá thể `{id, kind, fresh}` tiêu dùng cho món ăn, sắp theo `kind` rồi `id`.

### Hướng dẫn cập nhật Fixture & Test cũ
- Thay mọi `"hold": ["ca_loc", "bong_sung"]` trong fixture gather bằng:
  ```json
  "hold": [
    {"id": "I1", "kind": "ca_loc", "fresh": 100},
    {"id": "I2", "kind": "bong_sung", "fresh": 100}
  ]
  ```
- Thay mọi `"stock": {"bong_sung": 2}` trong fixture quán bằng:
  ```json
  "stock": [
    {"id": "I1", "kind": "bong_sung", "fresh": 100},
    {"id": "I2", "kind": "bong_sung", "fresh": 100}
  ]
  ```
- Thay kiểm tra kho rỗng `{"items": {}}` bằng `{"items": []}`.

### Tính năng mới (Phase 3)
- **Độ tươi (`freshness`):** Khởi tạo `fresh = 100`, hao `0.5/s` ở giỏ Gather và `0.25/s` ở kho Quán. Phát sự kiện `spoiled` (`{item_id, kind, location}`) đúng một lần theo thứ tự `id` khi độ tươi đi từ $\ge 30$ xuống $< 30$.
- **Giữ chỗ theo ID & Chốt giá theo độ tươi (`base_price`):** Chọn cá thể khả dụng chưa ươn tươi nhất (hòa theo `id`); tự động nhả và thử giữ lại 1 lần khi cá thể đang giữ bị ươn; chốt `base_price = floor(listed_price * avg_fresh / 100)`.
- **Mở rộng — Dòng nước lũ (`current`):** Khai báo `"extensions": ["current"]` và `tuning.gather.current`. Phát `current_warning` ở $t - 120$, `current_start` ở $t = 1800k$ kéo dài $480$ tick, đẩy người chơi $\pm 1.5\text{ m/s}$ khi $d_{\text{đầu bước}} \ge 10$, phát `current_end(elapsed|phase_end)`.

## [Contract v1.1 — Phase 2: Một ngày ở chợ nổi] — 2026-11-21
- Cá Sấu M1/M2 (tuần tra, đuổi, cắn, lùi, rơi nửa giỏ LIFO), cá bơi và sinh thêm, cá kèo / kèo nèo.
- Quán 2 bếp, 4 bàn, 6 món, lọc thực đơn theo `day_plan`; mode `day` (D1–D5), Shop nâng cấp oxy/Máu hiệu lực ngày sau, tạm dừng.

## [Contract v1.0 — Phase 1: PRD-0] — 2026-11-21
- Gather: bơi, oxy/ngạt, Máu/ngất, hái, bắt cá, giỏ LIFO, cập bến, file kho.
- Quán: khách theo lịch, giữ chỗ nguyên liệu, kiên nhẫn, bếp, bưng, phục vụ, boa, uy tín, hết ca.

