# Quán Ăn Chợ Nổi v1.0.0 — Nhóm 05

Bản phát hành đầu tiên, Test Contract **v1.3**. Gameplay, tuning, kho cá thể và JSONL giữ nguyên v1.2.

## Chạy
```bash
git clone https://github.com/Hphong2305/K5-L3B-LAB-Day12-AI-SDLC-439.git
cd K5-L3B-LAB-Day12-AI-SDLC-439
python3 -m chonoi.live --mode day --days 5      # mở http://127.0.0.1:8000/
```
Hoặc tải `chonoi-v1.0.0.zip` đính kèm, giải nén, vào thư mục rồi chạy lệnh thứ 3. Chỉ cần Python 3 (thư viện chuẩn) và trình duyệt.

## Có gì trong game
- **Buổi sáng:** lặn hái bông điên điển, bông súng, kèo nèo; bắt cá linh, cá lóc, cá kèo; oxy, ngạt, Máu, ngất; Cá Sấu M1 (từ ngày 1) và M2 (từ ngày 3); độ tươi hao trong giỏ, hàng ươn dưới 30; dòng nước lũ.
- **Buổi tối:** 2 bếp, 4 bàn, 6 món theo kế hoạch ngày; giữ chỗ nguyên liệu tươi nhất; giá theo độ tươi; boa, uy tín.
- **Shop:** nâng cấp bình oxy và Máu, có hiệu lực từ ngày sau. 5 ngày D1–D5.
- **Hỗ trợ:** cảnh báo chữ + biểu tượng (🐊 Cá Sấu gần, 🫧 oxy sắp hết, 😠 khách sắp giận), tương phản cao (phím H), tạm dừng (P).

## Mới ở v1.0.0 (Phase 4)
- `bench_cmd` — benchmark có render 1280×720: avg 242.3 FPS, 1% low 72.6 FPS, load 138.5 ms (Windows 11, seed 42, 30 s).
- `soak_cmd` — soak 10 ngày một tiến trình: 10/10 ngày, 0 crash, tất định.
- 3 cảnh báo, chế độ tương phản cao, chơi trọn vòng ngày trên trình duyệt, README 3 lệnh, LICENSE, CREDITS, CHANGELOG.

## Kiểm chứng
115/115 test (`PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`). Ma trận: [docs/verification/phase-4.md](verification/phase-4.md); bằng chứng: [docs/proof/phase-4/](proof/phase-4/README.md).

## Giới hạn đã biết
- Q7: ở headless, khách rời khi món đang nấu có thể làm kẹt món trên tay (bản live có cơ chế cất món thừa).
- Clone sạch mới thử trên Windows; benchmark đo trên một máy Windows.
- Tên một số trường sự kiện/snapshot của Quán và mode day là giả định (Q1–Q9 trong `docs/clarify.md`).

## Nhóm
TV1 `phong` (Lead), TV2 `thangdktd`, TV3 `daohiep2903`, TV4 `NTLam108`, TV5 `vuhieuvh` — xem [TEAM.md](../TEAM.md).
