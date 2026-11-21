# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| Phase 1 | phong (TV1) | Copilot / Claude | Lập trình Lát 1 Gather (bơi, oxy, ngạt, ngất, giỏ LIFO), bổ sung test unit `test_gather_lat1.py` | ~25k tokens | AI đôi khi nhầm lẫn tọa độ trục $d$ hướng xuống với trục y chuẩn |
| Phase 1 | thangdktd (TV2) | GitHub Copilot | Triển khai Lát 2 Gather (hái rau, bắt cá, hồi chiêu, cập bến xuất kho) | ~20k tokens | Cần bổ sung prompt rõ về quy tắc hòa ID nhỏ hơn khi khoảng cách bằng nhau |
| Phase 1 | daohiep2903 (TV3) | Codex / Copilot | Triển khai Lát 3 Quán (khách đến theo chu kỳ, kiểm tra kho, đặt chỗ `reserved`, độ kiên nhẫn) | ~22k tokens | AI ban đầu trừ kho trực tiếp thay vì giữ chỗ trong `reserved` |
| Phase 1 | nguyentronglam (TV4) | Codex / Claude | Triển khai Lát 4 Quán (bếp nấu, bưng bê, phục vụ, tính tiền, boa, uy tín, script tự lái E2E) | ~30k tokens | AI giả định khách hết kiên nhẫn vẫn giữ món trên tay người chơi |
| Phase 1 | vuhieuvh (TV5) | Antigravity (Gemini 3.8 Flash) | Khởi tạo ma trận truy vết AC-P1, kiểm thử độc lập 4 lát cắt, xác thực tính tất định và handoff file kho | ~20k tokens | AI ban đầu chưa nhận diện được môi trường Windows thiếu binary python3, cần thêm shim |
| Phase 2 | phong (TV1) | Copilot / Claude | Triển khai Quái Cá Sấu M1/M2 (tuần tra, đuổi theo, cắn trừ máu, rớt đồ LIFO, recoil) | ~28k tokens | AI quên giới hạn độ sâu $d \ge 10$ khiến cá sấu đuổi người chơi lên mặt nước |
| Phase 2 | thangdktd (TV2) | GitHub Copilot | Triển khai Đàn cá bơi phản xạ biên, đổi hướng và spawn chu kỳ 360 tick | ~24k tokens | AI tính sai góc phản xạ khi cá chạm góc 2 biên |
| Phase 2 | daohiep2903 (TV3) | Codex / Copilot | Triển khai lọc thực đơn Quán theo kế hoạch ngày (`day_dishes`) | ~18k tokens | AI cần được nhắc lọc thực đơn trước khi thực hiện giữ chỗ nguyên liệu |
| Phase 2 | nguyentronglam (TV4) | Codex / Claude | Triển khai vòng đời `--mode day` (DayIntro, gather, quan, shop, pause) | ~35k tokens | AI ban đầu kích hoạt nâng cấp ngay trong ngày thay vì dời sang ngày tiếp theo |
| Phase 2 | vuhieuvh (TV5) | Antigravity (Gemini 3.8 Flash) | QA Lead, tích hợp 5 lát cắt, kiểm thử hồi quy 78/78 tests, thiết kế giải phẫu Cá Sấu Web | ~25k tokens | AI khai báo trùng biến `const p` trong canvas gây lỗi màn hình đen |
| Phase 3 | phong (TV1) | Copilot / Claude | Cập nhật Contract v1.2, Adapter kho cá thể, độ tươi & dòng nước lũ trong Gather, viết ADR-0003 | ~30k tokens | AI tính hao tươi dạng float gây sai số lũy kế, sau đó chuyển sang dùng `Fraction` |
| Phase 3 | thangdktd (TV2) | GitHub Copilot | Cấp ID `I1..In` khi bắt/hái cá, bảo toàn danh sách cá thể khi rớt đồ LIFO | ~22k tokens | AI ban đầu tái sử dụng ID cá thể đã rớt thay vì tiếp tục tăng |
| Phase 3 | daohiep2903 (TV3) | Codex / Copilot | Quán theo dõi độ tươi kho, giữ chỗ `reserved` theo ID, cơ chế `re-reserve` khi ươn | ~28k tokens | AI ban đầu giữ cấu trúc `customer["reserved"]` dạng dict thay vì danh sách ID |
| Phase 3 | NTLam108 (TV4) | Codex / Claude | Định giá món ăn `base_price` theo độ tươi, tiền tip, mode day browser & sửa test | ~32k tokens | AI so sánh trực tiếp float với `Fraction` trong `test_day_mode` dẫn đến test fail |
| Phase 3 | vuhieuvh (TV5) | Antigravity (Gemini 3.8 Flash) | QA Lead, lập ma trận AC-P3, phát hiện 2 ca lỗi hồi quy, HUD thanh độ tươi và cảnh báo ươn | ~26k tokens | AI khi gộp nhánh có xung đột nhỏ ở hàm tóm tắt kho, đã giải quyết bằng `node -c` |
