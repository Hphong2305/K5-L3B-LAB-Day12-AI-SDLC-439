# Bằng chứng Phase 4 — v1.0.0 (contract v1.3)

Chạy trên commit `55cc8b5` (code Phase 4), Windows 11, Python 3.12.10, ngày 2026-11-21. Phần Phase 4 do nhóm trưởng thực hiện cùng Claude Code theo `ACTION_PLAN_NHOM05_DAY12_PHASE4.md`.

| File | Nội dung |
|---|---|
| `p4_full_test.log` | `python3 -m unittest discover -s tests -v`: **115/115 OK** |
| `bench-seed42.json` | Benchmark có render, seed 42, đo 30 s |
| `bench-window.png` | Nội dung cửa sổ benchmark 1280×720 (chụp bằng `PrintWindow` từ một lần chạy ngắn riêng, không phải lần đo) |
| `soak-seed7.json` | Soak 10 ngày, seed 7 |
| `hc-gather-monster-oxygen.png` | Tương phản cao: cảnh báo 🐊 Cá Sấu gần + 🫧 oxy sắp hết |
| `hc-quan-customer.png` | Tương phản cao: cảnh báo 😠 khách sắp giận |
| `warn-gather.json`, `warn-quan.json` | Scenario dựng tình huống cho hai ảnh trên |

## Benchmark có render

```bash
python3 -m chonoi.bench --seed 42 --duration 30 --out bench-seed42.json
```

| Trường | Giá trị | Mốc báo cáo | Đạt |
|---|---|---|---|
| `avg_fps` | 242.31 | ≥ 60 | ✔ |
| `p1_low_fps` | 72.57 | ≥ 30 | ✔ |
| `frames` | 7270 | — | — |
| `measured_s` | 30.002 | 30 | ✔ |
| `load_ms` | 138.5 | ≤ 10 000 | ✔ |

- Cảnh: Gather ngày 1, seed 42, đủ nút hái, đàn cá bơi, Cá Sấu M1 tuần tra, giỏ có độ tươi hao dần; Út Sen đứng ở bến; cửa sổ tkinter 1280×720; mô phỏng 60 tick/s theo đồng hồ thật, vẽ không giới hạn FPS.
- Một lần chạy trước đó bị nhiễu vì chụp màn hình trong lúc đo (`avg_fps` 230.46, `p1_low_fps` 39.35) nên bị bỏ; số trên là lần chạy sạch, không có thao tác song song.
- Giới hạn: `load_ms` tính từ lúc module `chonoi.bench` được nạp (không gồm thời gian khởi động trình thông dịch Python); đo trên một máy Windows, chưa đo trên macOS/Linux.

## Soak 10 ngày

```bash
python3 -m chonoi.soak --seed 7 --days 10 --out soak-seed7.json
```

- `days_completed = 10`, `crashes = 0`, `duration_s` 3.403 s (lần 2: 3.559 s).
- Chạy lần hai cùng seed: toàn bộ dữ liệu trừ `duration_s` trùng khớp.
- Soak không có input người chơi (đứng yên): Gather hết giờ với giỏ rỗng, Quán không có nguyên liệu nên `earned = 0`, uy tín giữ 3.0. Lệnh kiểm độ bền và giữ trạng thái xuyên ngày; phần giữ tiền/nâng cấp/ID qua ngày được kiểm bằng `tests/test_soak.py` (`test_plans_cycle_after_day_5_and_state_carries`).

## Cảnh báo và tương phản cao

```bash
python3 -m chonoi.live --mode gather --scenario docs/proof/phase-4/warn-gather.json   # mở /?contrast=high
python3 -m chonoi.live --mode quan --scenario docs/proof/phase-4/warn-quan.json
```

Chụp bằng Chrome headless 1280×720 ngay sau khi bật server. Cả ba cảnh báo hiện dạng băng chữ + biểu tượng (nền đen, viền vàng, chữ đậm) và nhãn tại chỗ (trên Cá Sấu, trên khách). Lần chụp đầu phát hiện băng cảnh báo còn hiện sau khi buổi đã kết thúc (ngất); đã sửa để ẩn khi `finished` hoặc tạm dừng rồi chụp lại.

## Clone sạch

Clone commit `55cc8b5` vào thư mục mới, chạy đúng 3 lệnh README (`git clone`, `cd`, `python3 -m chonoi.live --mode day --days 5`):
server in địa chỉ, `/state` trả `mode: day`, ngày 1, `gather`, không lỗi; `unittest` trong bản clone: OK; `git status` sạch.
Giới hạn: thử trên Windows (Git Bash, `python3` trỏ tới Python 3.12), **chưa thử trên macOS/Linux thật**; code chỉ dùng thư viện chuẩn, không phụ thuộc gói ngoài.
