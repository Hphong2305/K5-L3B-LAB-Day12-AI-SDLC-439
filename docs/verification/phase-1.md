# Ma trận truy vết Phase 1 (TV5 - QA Lead)

| AC | Yêu cầu kiểm chứng | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-1/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|---|
| **AC-P1-01** | Test Contract & Determinism | Chạy unit tests và kiểm tra đầu ra byte-identical với cùng seed | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ chạy baseline* |
| **AC-P1-02** | Lát 1: Bơi, ramp, hướng, chặn mép | Chạy unit tests kiểm tra tốc độ, đổi hướng, không bay khỏi mặt nước ($d \ge 0$) | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV1 code Lát 1* |
| **AC-P1-03** | Lát 1: Tiêu thụ & hồi oxy, ngạt, ngất | Test oxy giảm dưới nước, hồi ở mặt nước; hết oxy trừ HP; ngất mất giỏ | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV1 code Lát 1* |
| **AC-P1-04** | Lát 2: Hái rau & bắt cá | Test hái hoa súng/điên điển ở mặt nước, bắt cá có hồi chiêu dưới nước | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV2 code Lát 2* |
| **AC-P1-05** | Lát 2: Cập bến & xuất file kho | Test sự kiện `docked`, tạo file `inventory-out` đúng chuẩn `{"items": {...}}` | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV2 code Lát 2* |
| **AC-P1-06** | Handoff: Quán nạp file kho Gather | Chạy smoke test hai tiến trình Gather $\rightarrow$ file kho $\rightarrow$ Quán đọc stock | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ test handoff (T+25)* |
| **AC-P1-07** | Lát 3: Khách đến, giữ chỗ nguyên liệu | Test sinh khách theo chu kỳ, kiểm tra `reserved` món đủ nguyên liệu | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV3 code Lát 3* |
| **AC-P1-08** | Lát 3: Độ kiên nhẫn & khách rời quán | Test giảm `patience_ticks_left`, khách bỏ đi nhả `reserved` | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV3 code Lát 3* |
| **AC-P1-09** | Lát 4: Bếp nấu, bưng bê & phục vụ | Test bếp nấu đúng thời gian, bưng món lên tay, phục vụ đúng bàn | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV4 code Lát 4* |
| **AC-P1-10** | Lát 4: Thanh toán, boa & uy tín | Test khách trả tiền, tính boa theo thời hạn, cập nhật uy tín quán | Sẽ lưu vào `docs/proof/phase-1/` | *Đang chờ TV4 code Lát 4* |
| **AC-P1-11** | HUD tối thiểu hiển thị trực quan | Chơi thử trên trình duyệt qua `chonoi.live`, xác nhận đầy đủ HUD | Sẽ lưu snapshot giao diện | *Đang chờ kiểm tra* |

## Đánh giá ngắn
- **Yêu cầu nào đạt / chưa đạt:** Đang ở giai đoạn chuẩn bị khung kiểm thử trước T+20.
- **Điều cần chỉnh cho phase sau:** Sẽ cập nhật sau khi tích hợp toàn bộ các lát ở T+45.
