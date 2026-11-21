# Retro nhóm

## Phase 2 (nhanh)
- Điều tốt:
  - Tất cả 5 thành viên chia việc rõ ràng theo PRD v1.1 và hoàn thành đúng hạn (TV1: quái vật Cá Sấu; TV2: đàn cá bơi & sinh; TV3: quán mở rộng & lọc thực đơn; TV4: vòng lặp ngày & shop & pause; TV5: QA Lead & HUD cá sấu).
  - Tích hợp không bị xung đột logic lõi; toàn bộ 78/78 tests đều PASS ngay lần đầu chạy tích hợp đầy đủ.
  - Chế độ headless duy trì tính tất định 100% byte-identical across runs.
- Điều tệ:
  - Nhánh `feat/p2-day` tích hợp song song cả TV3 và TV4 nên cần cẩn trọng khi merge kiểm chứng.
  - Trình duyệt web có lúc bị đen màn hình do lỗi cú pháp JS khi sửa code canvas nếu không kiểm tra kỹ biến trùng.
- 1 hành động cho Phase 3:
  - Viết script tự động chạy cú pháp JS (`node -c`) và kiểm tra test tổng hợp trước mỗi lần commit giao diện và tính năng.

## Phase 3 (nhanh)
- Điều tốt:
  - Cả nhóm nâng cấp thành công Contract v1.2 sang kho cá thể có ID và độ tươi (`fresh`) theo ADR-0003.
  - QA Lead phát hiện sớm 2 lỗi hồi quy ở `test_day_mode` và `test_quan_leftovers`; TV3 và TV4 đã tiếp thu và sửa ngay lập tức, đưa kết quả lên 103/103 test PASS.
  - Tính tất định nhị phân byte-identical được bảo toàn 100% qua lệnh so sánh `fc.exe /b`.
- Điều tệ:
  - Việc biểu diễn độ tươi nội bộ bằng `Fraction` khiến một số test cũ so sánh số thực bị lệch nếu không qua hàm format.
- 1 hành động cho Phase 4:
  - Đảm bảo các test case luôn gọi qua hàm adapter `format_item` hoặc `snapshot` để chuẩn hóa dữ liệu đầu ra trước khi assert.

## Phase 4 (cuối)
- **Rà hành động Phase 2** ("chạy `node --check` cú pháp JS và test tổng hợp trước mỗi commit giao diện"): đã làm thủ công ở P3–P4 (mỗi lần sửa `index.html` đều chạy `node --check` trước khi commit) và ghi thành quy tắc trong `AGENTS.md` ở P4; **chưa** tự động hóa thành hook/skill vì thiếu thời gian. Hành động P3 ("assert qua `format_item`/snapshot") đã áp dụng trong test P4.
- **Điều tốt:**
  - Tích hợp P3 từ nhánh QA `vuhieuvh-phase3` vào `main` bằng fast-forward, không xung đột; 103/103 → 115/115 test sau P4.
  - Bench có render đạt cả ba mốc (avg 242 FPS, 1% low 72.6, load 138 ms); soak 10 ngày 0 crash, tất định.
  - Phát hiện bẫy: lên contract 1.3 làm các test P3 (`version == "1.2"`) **lặng lẽ skip** — đã đổi sang `>= 1.2`.
- **Điều tệ:**
  - Tag `phase-3` không được gắn đúng hạn; code P3 nằm trên nhánh tới đầu P4.
  - Phản tư cá nhân thiếu 3 người (TV1, TV2, TV3) và `vuhieuvh.md` vượt 200 từ tại thời điểm chốt.
  - Máy tích hợp không có `gh`, Release phải tạo trên GitHub web.
- **Số liệu** (`git log main`, tại commit P4; tổng / không tính merge): htphong23 11/7, Hphong2305 2/0, thangdktd 5/5, daohiep2903 10/7, NTLam108 11/8, vuhieuvh 18/10 (9 commit "Hai Duong" là starter của giảng viên). Đọc code của nhau: nhánh riêng + merge do TV1/TV5 rà; TV3–TV4 phối hợp qua `docs/plan/phase-1-tv3-tv4.md` và review diff. Token theo người: xem `docs/ai-usage-log.md` (ước tính, không đo chính xác).
- **Một lần AI sai và cách phát hiện:** khi lấy ảnh làm bằng chứng benchmark, AI chụp theo tọa độ màn hình trong lúc đang đo — ảnh ra là cửa sổ ứng dụng khác che lên (lộ dữ liệu riêng) và số đo bị nhiễu (1% low 39 FPS). Phát hiện khi **mở xem ảnh trước khi commit**; đã xóa ảnh, chạy lại bench sạch (1% low 72.6) và chụp nội dung cửa sổ bằng `PrintWindow` ở một lần chạy riêng.
- **Nếu làm lại, đổi gì:** gắn tag ngay khi hết giờ mỗi phase dù còn dở; chốt sớm TICKET/Test Contract vào repo (`docs/contracts/`) để agent không phải đoán tên trường (Q1–Q9); viết phản tư cá nhân cuối mỗi phase thay vì dồn cuối buổi.
- **Hành động có người nhận:** TV1 tạo Release `v1.0.0` + đính gói; TV1/TV2/TV3 viết `docs/members/<handle>.md`; TV5 rút `vuhieuvh.md` ≤ 200 từ; TV5 đổi link `file:///` trong `docs/verification/phase-2.md`, `phase-3.md` sang link tương đối.
