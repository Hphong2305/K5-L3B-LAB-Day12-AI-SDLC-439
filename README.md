# Quán Ăn Chợ Nổi — Nhóm 05 (v1.0.0)

Game 2D: buổi sáng Út Sen lặn bắt cá, hái rau trên mặt nước (tránh Cá Sấu, canh oxy, giữ độ tươi), buổi tối mở quán nấu và phục vụ khách, cuối ngày ghé Shop mua nâng cấp. Chơi 5 ngày theo kế hoạch thực đơn. Test Contract **v1.3**.

## Chạy game từ clone sạch (macOS / Linux, 3 lệnh)

Cần **Python 3** (thư viện chuẩn, không cài thêm gói; đã thử với 3.12) và một trình duyệt.

```bash
git clone https://github.com/Hphong2305/K5-L3B-LAB-Day12-AI-SDLC-439.git
cd K5-L3B-LAB-Day12-AI-SDLC-439
python3 -m chonoi.live --mode day --days 5
```

Mở địa chỉ lệnh in ra (mặc định `http://127.0.0.1:8000/`). Bản đóng gói `.zip` ở trang Release `v1.0.0` chạy bằng lệnh thứ 3 sau khi giải nén.

## Điều khiển

| Phím | Tác dụng |
|---|---|
| WASD / mũi tên | Bơi (sáng) / đi (tối) |
| E | Hái nút, cập bến · nấu, bưng, phục vụ · rời Shop |
| Space | Bắt cá (dưới nước) |
| 1 / 2 | Mua bình oxy / Máu ở Shop (hiệu lực từ ngày sau) |
| P | Tạm dừng |
| H | Bật/tắt **tương phản cao** (hoặc mở `?contrast=high`) |
| R | Chơi lại |

Cảnh báo bằng chữ và biểu tượng: 🐊 **Cá Sấu gần**, 🫧 **oxy sắp hết**, 😠 **khách sắp giận**.

**Điểm:** `score = earned + 100 × floor(reputation)`. Giá món = `floor(giá niêm yết × độ tươi trung bình / 100)`; boa khi khách còn ≥ 50% kiên nhẫn.

## Lệnh cho kiểm thử (theo `game.contract.json`)

```bash
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v                         # toàn bộ test
python3 -m chonoi.headless --mode gather|quan|day --seed 1 --ticks 600 --out out.jsonl   # headless (day: --days 1..5)
python3 -m chonoi.bench --seed 42 --duration 30 --out bench.json                    # benchmark có render 1280×720 (cần màn hình)
python3 -m chonoi.soak --seed 7 --days 10 --out soak.json                           # soak 10 ngày, một tiến trình
python3 -m chonoi.live --mode gather|quan                                           # chơi riêng một buổi
```

Trên Windows: `$env:PYTHONPATH='tests;.'` và dùng `python3` thật trong `PATH` (test gọi `headless_cmd` của manifest).

## Sáng tạo của nhóm

Tất cả **tắt ở headless**; bằng chứng lõi vẫn đúng: test headless và tất định trùng từng byte vẫn qua.

| Tính năng | Bật ở đâu | Số liệu | Chi tiết |
|---|---|---|---|
| Dòng nước lũ (`current`) đẩy người chơi khi lặn sâu | `extensions: ["current"]` trong manifest | `tuning.gather.current` | [CHANGELOG v1.2](CHANGELOG.md), ADR-0003 |
| Chơi trọn vòng ngày trên trình duyệt: Sáng → Tối → Shop, tạm dừng | `python3 -m chonoi.live --mode day` | `day_plan`, `shop` | `chonoi/live.py`, `chonoi/web/index.html` |
| Bảo quản món thừa: món của khách đã rời mang về bếp cất, dùng lại, tự hủy sau 30 phút game (ca 180 s = 3 giờ game → 1800 tick) | Chỉ `chonoi.live --mode quan` | `tuning.live` | [ADR-0001](docs/adr/0001-live-leftover-storage.md) |
| Chế độ sáng tạo: 3 Cá Sấu, vùng tuần tra rộng, thêm đàn cá kèo sâu | `chonoi.live --mode gather --creative` | trong code live | [ADR-0002](docs/adr/0002-live-creative-gather.md) |
| HUD độ tươi, cảnh báo hàng ươn, Cá Sấu vẽ chi tiết | Giao diện trình duyệt | — | `chonoi/web/index.html` |

## Tài liệu

[TEAM.md](TEAM.md) · [AGENTS.md](AGENTS.md) · [CHANGELOG.md](CHANGELOG.md) · [CREDITS.md](CREDITS.md) · [LICENSE](LICENSE) · [Release notes v1.0.0](docs/release-notes-v1.0.0.md) · `docs/verification/phase-1..4.md` · `docs/proof/` · `docs/adr/` · [docs/clarify.md](docs/clarify.md) · [docs/retro.md](docs/retro.md) · [docs/ai-usage-log.md](docs/ai-usage-log.md) · `docs/members/` · [docs/STARTER.md](docs/STARTER.md) (khung kỹ thuật của giảng viên)

## Về bài lab

Day 12 — AI SDLC, làm theo nhóm qua 4 phase trong 3 giờ; yêu cầu từng phase ở lab board [Chợ Nổi Lab](https://claude.ai/artifact/E35v787wSx2wDgPTNhMVDg). Quy định: dùng AI thoải mái, không sao chép repo nhóm khác, bằng chứng phải thật; asset ngoài chỉ CC0/CC-BY/MIT hoặc tự tạo và ghi nguồn ở `CREDITS.md`; không commit API key, token, `.env`.
