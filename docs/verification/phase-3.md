# Ma trận truy vết Phase 3 (TV5 - QA Lead)

> **Ghi chú QA:** Toàn bộ 10 tiêu chí đã được kiểm thử thực tế và đạt 100% với 103/103 tests PASS.

| AC | Yêu cầu kiểm chứng | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-3/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|---|
| **AC-P3-01** | Test Contract v1.2: Từ chối file kho v1.1 cũ | Chạy Quán `--inventory` với file kho v1.1 (`{"items": {"ca_loc": 2}}`), kỳ vọng thoát với mã lỗi 2 (`BadInput`) | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log), [test_phase3_qa.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_phase3_qa.py) | **ĐẠT (PASS)** |
| **AC-P3-02** | Độ tươi & Hàng ươn (`spoiled`) ở Gather | Khởi tạo cá với `fresh = 30` (ngưỡng ươn), tại tick 1 cá chuyển trạng thái ươn (`spoiled`) và phát event `spoiled` theo thứ tự ID | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log), [test_gather_phase3_tv1.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_gather_phase3_tv1.py) | **ĐẠT (PASS)** |
| **AC-P3-03** | Bảo toàn ID, Kind, Fresh khi Handoff Gather $\to$ Quán | Hai tiến trình Gather và Quán trao đổi qua file kho v1.2 danh sách thực thể `[{id, kind, fresh}]`; bảo toàn nguyên vẹn cá thể | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log), [test_gather_phase3_tv2.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_gather_phase3_tv2.py) | **ĐẠT (PASS)** |
| **AC-P3-04** | Quán: Cơ chế Giữ chỗ lại (`re-reserve`) | Khi nguyên liệu giữ chỗ bị ươn hoặc khách rời, giải phóng toàn bộ reservation và chọn lại nguyên liệu tươi nhất thay thế | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log), [test_quan_customers.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_quan_customers.py) | **ĐẠT (PASS - 8/8 tests)** |
| **AC-P3-05** | Quán: Định giá theo Fresh & Tiền Boa (Tip) | Nấu món từ nguyên liệu tươi; chốt `base_price = floor(price * avg_fresh / 100)` và tính tiền boa trên giá chốt | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log), [test_quan_price.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_quan_price.py) | **ĐẠT (PASS - 7/7 tests)** |
| **AC-P3-06** | Mode Day: Cấp phát ID đơn điệu xuyên Ngày | Chạy `--mode day` từ Ngày 1 sang Ngày 2; kiểm tra ID thực thể không bị reset về 0 mà tăng đơn điệu xuyên ca chơi | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log), [test_day_mode.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_day_mode.py) | **ĐẠT (PASS)** |
| **AC-P3-07** | Tính Tất định Headless (Determinism) | Chạy 2 lần độc lập `--mode day --days 2` cùng seed 42; kiểm tra nhị phân bằng `fc.exe /b` trùng khớp từng byte | [day_smoke.jsonl](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/day_smoke.jsonl) | **ĐẠT (PASS - FC: no differences)** |
| **AC-P3-08** | Kiểm thử Hồi quy (Regression P1 & P2) | Chạy toàn bộ test suite dự án; toàn bộ 103/103 tests đều PASS | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log) | **ĐẠT (PASS - 103/103 tests)** |
| **AC-P3-09** | HUD Trực quan: Độ tươi & Cảnh báo hàng ươn | Canvas web hiển thị thanh độ tươi (Freshness Bar) theo dải màu và biểu tượng cảnh báo hàng ươn ⚠️ trên giỏ và kho | [chonoi/web/index.html](file:///e:/ai_thuc_chien/day_12_thuc_hanh/chonoi/web/index.html), [test_phase3_qa.py](file:///e:/ai_thuc_chien/day_12_thuc_hanh/tests/test_phase3_qa.py) | **ĐẠT (PASS)** |
| **AC-P3-10** | Hồ sơ QA & Báo lỗi đúng thành viên | Lập ma trận, lưu proof, viết phản tư, và báo lỗi chính xác kèm vị trí code cho TV3, TV4 fix thành công | [p3_full_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-3/p3_full_test.log) | **ĐẠT (PASS)** |

## Đánh giá ngắn Phase 3
- **Yêu cầu đã đạt:**
  - Hoàn tất 100% tích hợp Phase 3 từ cả 5 thành viên (TV1, TV2, TV3, TV4, TV5).
  - Khắc phục hoàn toàn 2 lỗi hồi quy trong `test_day_mode.py` và `test_quan_leftovers.py`.
  - Toàn bộ 103 unit và integration test đều PASS.
  - Tính tất định byte-identical của chế độ Ngày (`--mode day --days 2`) được khẳng định tuyệt đối.
  - HUD web hỗ trợ hiển thị dải màu độ tươi và cảnh báo hàng ươn sinh động.
