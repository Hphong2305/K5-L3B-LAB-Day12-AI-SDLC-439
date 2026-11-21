# vuhieuvh — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm (kèm link commit):**
  - Khởi tạo khung ma trận kiểm thử Phase 1 ([docs/verification/phase-1.md](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/verification/phase-1.md)).
  - Chuẩn bị sẵn bộ kịch bản test handoff kho hai tiến trình ([dock.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/dock.json), [dock-inputs.json](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/dock-inputs.json)).
  - Chạy kiểm thử xác thực độc lập cho Lát 1 (bơi, oxy, ngạt, ngất, giỏ) và sinh bằng chứng mô phỏng ngất xả kho ([lat1_test.log](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat1_test.log), [lat1_faint.jsonl](file:///e:/ai_thuc_chien/day_12_thuc_hanh/docs/proof/phase-1/lat1_faint.jsonl)).
- **Tôi đã review (kèm link):**
  - Review commit `e07352e` của TV1 (`feat(gather): finalize team, contracts and implement Lat 1`): Chạy bộ test `tests/test_gather_lat1.py` đạt 5/5 test nghiệp vụ, xác nhận không gây hồi quy (37/37 test toàn dự án đều pass).
- **AI sai ở đâu và tôi phát hiện thế nào:**
  - AI ban đầu chưa cấu hình tương thích lệnh `python3` trên Windows dẫn đến mã lỗi 9009; tôi phát hiện qua log unittest và khắc phục.
- **Điều tôi học được:**
  - Việc kiểm thử chéo ngay khi một thành viên vừa hoàn thành lát giúp phát hiện lỗi sớm và tạo sự tự tin cao cho người kế tiếp (TV2) tiếp tục phát triển.
