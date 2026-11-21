# Ma trận truy vết Phase 2 (TV5 - QA Lead)

| AC | Yêu cầu kiểm chứng | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-2/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|---|
| **AC-P2-01** | Manifest v1.1 & Cấu hình | Kiểm tra `contract_version: "1.1"`, 6 nguyên liệu, 6 món, cấu hình Shop, `day_plan` D1–D5 | [game.contract.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/game.contract.json) | **ĐẠT (PASS)** |
| **AC-P2-02** | Lát 1: Cá Sấu M1/M2 tuần tra & rượt đuổi | Quái M1 (từ D1), M2 (từ D3). Patrol 1.0 m/s; phát hiện người chơi khi $d \ge 10$ và khoảng cách $\le 10$m $\rightarrow$ chase 3.0 m/s; thoát khi cách $>16$m hoặc $d < 10$ | [p2_monsters_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-2/p2_monsters_test.log) | **ĐẠT (PASS - 5/5 tests)** |
| **AC-P2-03** | Lát 1: Cá Sấu tấn công, recoil & rớt đồ | Hit khi cách $\le 1.5$m, người chơi $d \ge 10$, hết bất tử: giảm 1 HP, rớt `floor(hold/2)` theo LIFO, bất tử 90 tick, quái recoil 60 tick (lùi 2.0 m/s) | [p2_monsters_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-2/p2_monsters_test.log) | **ĐẠT (PASS)** |
| **AC-P2-04** | Lát 2: Đàn cá bơi, đổi hướng & sinh thêm | Cá bơi 1.5 m/s, turn 120 tick, spawn mỗi 360 tick (8 đàn đầu, max 12 đàn, tỉ lệ 40% linh / 30% lóc / 30% kèo) | Sẽ lưu vào `docs/proof/phase-2/` | *Đang chờ TV2 code Cá bơi* |
| **AC-P2-05** | Lát 2: Nội dung mới (cá kèo, kèo nèo N5/N6) | Bắt cá kèo (`ca_keo`), hái kèo nèo (`keo_neo`) tại các điểm nút N5, N6 | Sẽ lưu vào `docs/proof/phase-2/` | *Đang chờ TV2 code Lát 2* |
| **AC-P2-06** | Lát 3: Quán mở rộng 2 bếp B1/B2 & 4 bàn T1–T4 | Mô phỏng Quán với 2 bếp độc lập, 4 bàn nhận khách; kiểm tra điều phối đơn chờ | Sẽ lưu vào `docs/proof/phase-2/` | *Đang chờ TV3 code Quán* |
| **AC-P2-07** | Lát 3: Thực đơn 6 món & lọc theo `day_plan` | 6 món đúng công thức, khách chỉ gọi các món nằm trong kế hoạch ngày (`dishes` của D1–D5) | Sẽ lưu vào `docs/proof/phase-2/` | *Đang chờ TV3 code Quán* |
| **AC-P2-08** | Lát 4: Vòng đời chế độ Ngày (`--mode day`) | Luồng pha: `DayIntro → gather → EveningIntro → quan → DayResult → Shop` qua các ngày D1–D5 | Sẽ lưu vào `docs/proof/phase-2/` | *Đang chờ TV4 code Day* |
| **AC-P2-09** | Lát 4: Shop & Nâng cấp sang ngày hôm sau | Shop 600 tick, mua nâng cấp oxy/máu; xác nhận chỉ có hiệu lực từ Ngày tiếp theo | Sẽ lưu vào `docs/proof/phase-2/` | *Đang chờ TV4 code Shop* |
| **AC-P2-10** | Lát 4: Cơ chế Tạm dừng (`pause`) | Khi pause: tick ngoài tăng nhưng `sim_tick`, `phase_tick` và các bộ đếm không chạy | Sẽ lưu vào `docs/proof/phase-2/` | *Đang chờ TV4 code Pause* |
| **AC-P2-11** | Kiểm tra hồi quy (Regression Phase 1) | Chạy lại toàn bộ test suite Phase 1 dưới cấu hình và số liệu chuẩn mới v1.1 | [p2_monsters_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-2/p2_monsters_test.log) | **ĐẠT (PASS - 54/54 tests)** |
| **AC-P2-12** | HUD trực quan v1.1 | Hiển thị quái cá sấu, 2 bếp, 4 bàn, pause UI và cửa hàng Shop trên trình duyệt | Sẽ lưu snapshot giao diện | *Đang chuẩn bị* |

## Đánh giá ngắn Phase 2
- **Yêu cầu đã đạt:**
  - Manifest v1.1 đã cập nhật đầy đủ thông số cho cả 5 ngày và 6 món ăn.
  - Lát Cá Sấu (TV1) đã kiểm thử độc lập thành công 5/5 tests: tuần tra, đuổi theo, cắn trừ máu, rớt đồ LIFO, quái recoil và ngất xả kho.
  - Kiểm tra hồi quy toàn dự án: 54/54 tests đều PASS, không phá vỡ logic cũ.
- **Yêu cầu đang tiến hành:** Đang theo dõi TV2 (cá bơi/sinh) và TV3-TV4 (quán mở rộng & chế độ Day).
