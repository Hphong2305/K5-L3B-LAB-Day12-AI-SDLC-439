# Phase 3 — Giá theo độ tươi và `cook_started.items` (TV4)

Nhánh `feat/p3-tv4-quan-price`, tách từ `feat/p3-tv3-quan-inventory` (TV3, `41cfd1a`). Ngày 2026-11-21, Windows, Python 3.12. Theo ADR-0003, dòng "Quán & Day".

## Đã làm

- `chonoi/sim/quan.py`
  - Bếp nhận đơn: lấy các cá thể từ `_consume_reserved` (TV3), tính `base_price = floor(listed_price × avg_fresh / 100)`. `fresh` dạng `Fraction` lấy đúng lúc tiêu nên phép `floor` chính xác.
  - `cook_started.data.items` = các cá thể đã tiêu `{id, kind, fresh}`, sắp theo `kind` rồi `id`.
  - `base_price` đi theo món: bếp → `hand` → bàn. Món thừa dùng lại (chỉ live) giữ giá chốt lúc nấu. Món dựng sẵn từ fixture, không có cá thể, dùng giá niêm yết (`TODO(TV4, TICKET-03)`).
  - Boa = `floor(base_price × tip_rate)`, tính bằng `Fraction`. Giá trên `served`/`paid` là `base_price`.
- `tests/test_quan_leftovers.py`: `reserved` và `stock` rỗng theo v1.2 là `[]`.
- `tests/test_quan_price.py` (mới, 7 test).
- `tests/test_day_mode.py`: bàn giao giỏ v1.2 sang Quán, ngất ra kho `[]`, ID `I` tăng xuyên Ngày. Test bàn giao của TV2 so `sim.sub.stock` với `99.992`, đổi sang so qua `format_item` vì Quán (TV3) giữ `fresh` dạng `Fraction` bên trong; giá trị không đổi.

## Lệnh và kết quả

```powershell
$env:PYTHONPATH='tests;.'; $env:PYTHONIOENCODING='utf-8'
python3 -m unittest test_quan_price test_quan_leftovers test_quan_customers test_quan_day_menu test_day_mode -v
python3 -m unittest discover -s tests
```

| Kiểm | Kết quả |
|---|---|
| Quán + Day (5 file) | `Ran 32 tests ... OK` |
| Toàn bộ (sau khi gộp `main` có test v1.2 của TV2, `5252728`) | `Ran 99 tests ... OK`, gồm smoke `test_inv_01` Gather → file kho → Quán |
| `base_price` | fresh 50: 60 → 30, boa 6. Trung bình 4 cá thể (100, 90, 80, 70) cho lẩu 120 → 102. fresh 99.992 (lưới 1/240): 59, không làm tròn lên 60 |
| `cook_started.items` | sắp `bong_dien_dien I1`, `ca_linh I2, I3, I10` |
| Headless | `cook_started.items[0].fresh` = 99.996 (hao 1 tick ở kho Quán trước lượt bấm). Hai lần chạy trùng từng byte |
| Day 2 ngày (giỏ v1.2 dựng sẵn) | ngày 2 cấp ID từ `I10`. Giá thu theo độ tươi (cá lóc 59, gỏi 38). Kết thúc `days_complete` |

## Còn mở

- Chưa có TICKET-03 bản đầy đủ: có thêm `base_price` vào `cook_started`/`served` không, và món không có cá thể tính giá thế nào.
