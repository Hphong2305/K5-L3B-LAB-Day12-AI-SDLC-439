# Ma trận truy vết Phase 3 (TV5 - QA Lead)

> **Ghi chú QA:** Tuân thủ nguyên tắc không tự nhận PASS khi chưa chạy test thực tế trên code của các thành viên.

| AC | Yêu cầu kiểm chứng | Cách kiểm chứng | Bằng chứng (dự kiến link `docs/proof/phase-3/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|---|
| **AC-P3-01** | Test Contract v1.2: Từ chối file kho v1.1 cũ | Chạy Quán `--inventory` với file kho định dạng v1.0/v1.1 (`{"items": {"ca_loc": 2}}`), kỳ vọng thoát với mã lỗi 2 | `docs/proof/phase-3/inv_v11_rejected.log` | *Chờ TV3 cập nhật Quán v1.2* |
| **AC-P3-02** | Độ tươi & Hàng ươn (`spoiled`) ở Gather | Khởi tạo cá với `fresh = 30` (ngưỡng ươn), tại tick 1 kiểm tra xem cá có chuyển sang trạng thái ươn (`spoiled`) và phát event `spoiled` hay không | `docs/proof/phase-3/gather_spoiled.log` | *Chờ TV1/TV2 code độ tươi Gather* |
| **AC-P3-03** | Bảo toàn ID, Kind, Fresh khi Handoff Gather $\to$ Quán | Hai tiến trình Gather và Quán trao đổi qua file kho v1.2 danh sách thực thể `[{id, kind, fresh}]`; kiểm tra kho Quán nạp đúng từng cá thể | `docs/proof/phase-3/smoke_handoff_v12.json` | *Chờ TV2 xuất kho & TV3 nạp kho v1.2* |
| **AC-P3-04** | Quán: Cơ chế Giữ chỗ lại (`re-reserve`) | Khách nhận đơn giữ chỗ nguyên liệu (`reserved`), khi khách rời đi do hết kiên nhẫn thì nguyên liệu được hoàn trả an toàn về kho để khách sau dùng tiếp | `docs/proof/phase-3/quan_re_reserve.log` | *Chờ TV3 code Quán* |
| **AC-P3-05** | Quán: Định giá theo Fresh & Tiền Boa (Tip) | Nấu món từ nguyên liệu tươi so với nguyên liệu giảm độ tươi; kiểm tra doanh thu cộng ví và tiền boa thay đổi theo bảng tính của contract v1.2 | `docs/proof/phase-3/quan_price_tip.log` | *Chờ TV3 code Quán* |
| **AC-P3-06** | Mode Day: Cấp phát ID đơn điệu xuyên Ngày | Chạy `--mode day` từ Ngày 1 sang Ngày 2; kiểm tra ID thực thể không bị reset về 0 mà tăng đơn điệu xuyên suốt ca chơi | `docs/proof/phase-3/day_id_alloc.log` | *Chờ TV4 cập nhật DaySim* |
| **AC-P3-07** | Tính Tất định Headless (Determinism) | Chạy 2 lần độc lập `--mode day` cùng seed 42; kiểm tra nhị phân bằng `fc.exe /b` trùng khớp từng byte | `docs/proof/phase-3/p3_determinism.log` | *Chờ tích hợp cả nhóm* |
| **AC-P3-08** | Kiểm thử Hồi quy (Regression P1 & P2) | Chạy toàn bộ test suite từ Phase 1 và Phase 2 (78+ tests), đảm bảo không hồi quy tính năng cũ | `docs/proof/phase-3/p3_full_test.log` | *Chờ tích hợp cả nhóm* |
| **AC-P3-09** | HUD Trực quan: Độ tươi & Cảnh báo hàng ươn | Canvas web hiển thị thanh độ tươi (Freshness Bar) theo dải màu và biểu tượng cảnh báo hàng ươn ⚠️ trên giỏ và kho | [chonoi/web/index.html](file:///e:/ai_thuc_chien/day_12_thuc_hanh/chonoi/web/index.html) | **Đang hoàn thiện HUD (TV5)** |
| **AC-P3-10** | Hồ sơ QA & Nhật ký AI | Hoàn tất proof, verification matrix, retro Phase 3 và nhật ký AI cho cả nhóm | [docs/ai-usage-log.md](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/ai-usage-log.md) | *Đang cập nhật* |

## Đánh giá ngắn Phase 3
- **Hiện trạng:** Đang ở giai đoạn khởi tạo Phase 3. TV5 đã lập ma trận kiểm chứng, chuẩn bị test fixture và triển khai nâng cấp giao diện HUD.
- **Kế hoạch tiếp theo:** Hoàn thành HUD trực quan, theo dõi các thành viên TV1-TV4 đẩy code và thực hiện kiểm thử độc lập cho từng lát cắt ngay khi có commit.
