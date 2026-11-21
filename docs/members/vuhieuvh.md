# vuhieuvh — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm (kèm link commit):**
  - Khởi tạo khung ma trận kiểm thử Phase 1 ([docs/verification/phase-1.md](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/verification/phase-1.md)).
  - Chuẩn bị sẵn bộ kịch bản test handoff kho hai tiến trình ([dock.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/dock.json), [dock-inputs.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/dock-inputs.json)).
  - Chạy kiểm thử xác thực độc lập cho Lát 1 (bơi, oxy, ngạt, ngất, giỏ) và Lát 2 (hái rau, bắt cá, hồi chiêu, cập bến xuất kho) với 45/45 test toàn dự án đạt ([lat1_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat1_test.log), [lat2_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat2_test.log)).
- **Tôi đã review (kèm link):**
  - Review commit `e07352e` của TV1 (`feat(gather): finalize team, contracts and implement Lat 1`): đạt 5/5 unit test.
  - Review commit `38e08b2` & `fb5a133` của TV2 (`thangdktd`): xác nhận Lát 2 hái/bắt cá hoạt động chính xác và handoff file kho thành công.
- **AI sai ở đâu và tôi phát hiện thế nào:**
  - AI ban đầu chưa cấu hình tương thích lệnh `python3` trên Windows dẫn đến mã lỗi 9009; tôi phát hiện qua log unittest và khắc phục.
- **Điều tôi học được:**
  - Tầm quan trọng của việc kiểm thử liên tục từng lát cắt (Continuous Testing) giúp phát hiện xung đột sớm và giữ nhánh chính luôn ổn định.
