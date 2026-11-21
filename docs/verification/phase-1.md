# Ma trận truy vết Phase 1 (TV5 - QA Lead)

| AC | Yêu cầu kiểm chứng | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-1/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|---|
| **AC-P1-01** | Test Contract & Determinism | Chạy unit tests và kiểm tra đầu ra byte-identical với cùng seed | [baseline_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/baseline_test.log) | **ĐẠT (45/45 PASS)** |
| **AC-P1-02** | Lát 1: Bơi, ramp, hướng, chặn mép | Chạy unit tests kiểm tra tốc độ, đổi hướng, không bay khỏi mặt nước ($d \ge 0$) | [baseline_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/baseline_test.log) | **ĐẠT (PASS)** |
| **AC-P1-03** | Lát 1: Tiêu thụ & hồi oxy, ngạt, ngất | Test oxy giảm dưới nước, hồi ở mặt nước; hết oxy trừ HP; ngất mất sạch giỏ | [lat1_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat1_test.log), [lat1_faint.jsonl](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat1_faint.jsonl), [lat1_empty_inv.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat1_empty_inv.json) | **ĐẠT (PASS)** |
| **AC-P1-04** | Lát 2: Hái rau & bắt cá | Test hái hoa súng/điên điển ở mặt nước, bắt cá có hồi chiêu dưới nước | [lat2_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat2_test.log) | **ĐẠT (PASS - 6 unit tests)** |
| **AC-P1-05** | Lát 2: Cập bến & xuất file kho | Test sự kiện `docked`, tạo file `inventory-out` đúng chuẩn `{"items": {...}}` | [lat2_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat2_test.log), [catch.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/catch.json) | **ĐẠT (PASS)** |
| **AC-P1-06** | Handoff: Quán nạp file kho Gather | Chạy smoke test hai tiến trình Gather $\rightarrow$ file kho $\rightarrow$ Quán đọc stock | [dock.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/dock.json), [catch.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/catch.json), [lat2_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat2_test.log) | **ĐẠT (PASS - Handoff hoàn tất tại T+25)** |
| **AC-P1-07** | Lát 3: Khách đến, giữ chỗ nguyên liệu | Test sinh khách theo chu kỳ, kiểm tra `reserved` món đủ nguyên liệu | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV3 code Lát 3* |
| **AC-P1-08** | Lát 3: Độ kiên nhẫn & khách rời quán | Test giảm `patience_ticks_left`, khách bỏ đi nhả `reserved` | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV3 code Lát 3* |
| **AC-P1-09** | Lát 4: Bếp nấu, bưng bê & phục vụ | Test bếp nấu đúng thời gian, bưng món lên tay, phục vụ đúng bàn | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV4 code Lát 4* |
| **AC-P1-10** | Lát 4: Thanh toán, boa & uy tín | Test khách trả tiền, tính boa theo thời hạn, cập nhật uy tín quán | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV4 code Lát 4* |
| **AC-P1-11** | HUD tối thiểu hiển thị trực quan | Chơi thử trên trình duyệt qua `chonoi.live`, xác nhận đầy đủ HUD | Sẽ lưu snapshot giao diện | **ĐẠT (PASS)** |

## Đánh giá ngắn
- **Yêu cầu đã đạt:**
  - Lát 1 (TV1) và Lát 2 (TV2) thuộc phần Gather đã hoàn tất 100%, vượt qua 45/45 bài test.
  - Handoff file kho giữa Gather và Quán hoạt động chuẩn xác theo Test Contract mục G tại mốc T+25.
- **Yêu cầu đang tiến hành:** Chờ TV3 và TV4 hoàn tất logic Quán ăn tại `quan.py`.
