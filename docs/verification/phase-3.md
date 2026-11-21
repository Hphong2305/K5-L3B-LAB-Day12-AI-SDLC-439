# Ma trận truy vết Phase 3 (TV5 - QA Lead)

> **Ghi chú QA:** Tuân thủ nguyên tắc không tự nhận PASS khi chưa chạy test thực tế trên code của các thành viên.

| AC | Yêu cầu kiểm chứng | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-3/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|---|
| **AC-P3-01** | Test Contract v1.2: Từ chối file kho v1.1 cũ | Chạy Quán `--inventory` với file kho v1.1 (`{"items": {"ca_loc": 2}}`), kỳ vọng thoát với mã lỗi 2 (`BadInput`) | [test_phase3_qa.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_phase3_qa.py), [test_gather_phase3_tv1.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_gather_phase3_tv1.py) | **ĐẠT (PASS)** |
| **AC-P3-02** | Độ tươi & Hàng ươn (`spoiled`) ở Gather | Khởi tạo cá với `fresh = 30` (ngưỡng ươn), tại tick 1 cá chuyển trạng thái ươn (`spoiled`) và phát event `spoiled` theo thứ tự ID | [test_gather_phase3_tv1.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_gather_phase3_tv1.py) | **ĐẠT (PASS)** |
| **AC-P3-03** | Bảo toàn ID, Kind, Fresh khi Handoff Gather $\to$ Quán | Hai tiến trình Gather và Quán trao đổi qua file kho v1.2 danh sách thực thể `[{id, kind, fresh}]`; bảo toàn nguyên vẹn cá thể | [test_gather_phase3_tv2.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_gather_phase3_tv2.py) | **ĐẠT (PASS)** |
| **AC-P3-04** | Quán: Cơ chế Giữ chỗ lại (`re-reserve`) | Khi nguyên liệu giữ chỗ bị ươn hoặc khách rời, giải phóng toàn bộ reservation và chọn lại nguyên liệu tươi nhất thay thế | [test_quan_customers.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_quan_customers.py), [tv3-quan.md](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/tv3-quan.md) | **ĐẠT (PASS - 8/8 tests)** |
| **AC-P3-05** | Quán: Định giá theo Fresh & Tiền Boa (Tip) | Nấu món từ nguyên liệu tươi; chốt `base_price = floor(price * avg_fresh / 100)` và tính tiền boa | `docs/proof/phase-3/quan_price_tip.log` | *Chờ TV4 hoàn thiện code* |
| **AC-P3-06** | Mode Day: Cấp phát ID đơn điệu xuyên Ngày | Chạy `--mode day` từ Ngày 1 sang Ngày 2; kiểm tra ID thực thể không bị reset về 0 mà tăng đơn điệu xuyên ca chơi | `docs/proof/phase-3/day_id_alloc.log` | *Chờ TV4 hoàn thiện code* |
| **AC-P3-07** | Tính Tất định Headless (Determinism) | Chạy 2 lần độc lập `--mode day` cùng seed 42; kiểm tra nhị phân bằng `fc.exe /b` trùng khớp từng byte | `docs/proof/phase-3/p3_determinism.log` | *Chờ TV4 fix 2 test legacy* |
| **AC-P3-08** | Kiểm thử Hồi quy (Regression P1 & P2) | Chạy toàn bộ test suite dự án; hiện tại đạt 91/93 tests (2 test cũ của TV4 cần cập nhật schema v1.2) | `docs/proof/phase-3/p3_full_test.log` | *91/93 tests PASS (Phát hiện 2 lỗi của TV4)* |
| **AC-P3-09** | HUD Trực quan: Độ tươi & Cảnh báo hàng ươn | Canvas web hiển thị thanh độ tươi (Freshness Bar) theo dải màu và biểu tượng cảnh báo hàng ươn ⚠️ trên giỏ và kho | [chonoi/web/index.html](file:///e:/ai_thuc_chien/day_12_thuc_hanh/chonoi/web/index.html), [test_phase3_qa.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_phase3_qa.py) | **ĐẠT (PASS)** |
| **AC-P3-10** | Hồ sơ QA & Báo lỗi đúng thành viên | Lập ma trận, lưu proof, viết phản tư, và báo lỗi chính xác kèm vị trí code cho TV4 | [docs/verification/phase-3.md](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/verification/phase-3.md) | **ĐẠT (PASS - Đã phát hiện & lập báo cáo lỗi)** |

## Báo cáo lỗi gửi thành viên (QA Bug Report)
1. **Lỗi 1 (Gửi TV4 - `NTLam108`):**
   - **Vị trí:** `tests/test_day_mode.py`, dòng 113 trong hàm `test_gather_hold_becomes_quan_stock_with_day_menu`.
   - **Mô tả:** Test đang so sánh trực tiếp `sim.sub.stock` với float `{'fresh': 99.992}`, nhưng theo ADR-0003 của TV1, `sim.sub.stock` lưu `fresh` dưới dạng `Fraction(11999, 120)` để đảm bảo độ chính xác tuyệt đối.
   - **Cách sửa cho TV4:** Sử dụng `sim.sub.snapshot()["stock"]` (đã được format thành số thực) hoặc dùng hàm `fresh_to_num()` khi so sánh `sim.sub.stock`.
2. **Lỗi 2 (Gửi TV4 - `NTLam108`):**
   - **Vị trí:** `tests/test_quan_leftovers.py`, dòng 38 trong hàm `test_return_and_reuse_without_consuming_stock_again`.
   - **Mô tả:** Test kiểm tra `self.assertEqual(customer["reserved"], {})`. Tuy nhiên ở contract v1.2, TV3 đã đổi cấu trúc `customer["reserved"]` từ dictionary sang mảng danh sách ID `[]`.
   - **Cách sửa cho TV4:** Đổi assertion thành `self.assertEqual(customer["reserved"], [])` (hoặc `self.assertFalse(...)`).
