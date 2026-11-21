# Ma trận truy vết Phase 4 — v1.0.0 (contract v1.3)

Commit kiểm chứng: `55cc8b5` (code). Bằng chứng: [`docs/proof/phase-4/`](../proof/phase-4/README.md). AC lấy theo `ACTION_PLAN_NHOM05_DAY12_PHASE4.md`; TICKET-04 bản gốc không có trong repo.

| AC | Yêu cầu | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|---|
| AC-P4-01 | Manifest v1.3, khai `bench_cmd`, `soak_cmd`; không đổi gameplay/tuning/kho/JSONL v1.2 | `tests/test_phase4.py` (`test_v13_declares_bench_and_soak`, `test_gameplay_tuning_unchanged_from_v12`); khi sửa manifest, script so `tuning` trước/sau | [game.contract.json](../../game.contract.json), [p4_full_test.log](../proof/phase-4/p4_full_test.log) | **ĐẠT** |
| AC-P4-02 | Benchmark có render thật 1280×720, seed 42, warm-up 3 s, đo 30 s; `bench.json` đúng 5 trường | Chạy `bench_cmd --seed 42 --duration 30`; ảnh cửa sổ; test công thức `p1_low` | [bench-seed42.json](../proof/phase-4/bench-seed42.json), [bench-window.png](../proof/phase-4/bench-window.png) | **ĐẠT** — avg 242.31, 1% low 72.57, load 138.5 ms (Windows) |
| AC-P4-03 | Soak 10 ngày một tiến trình, gather → quan → shop mỗi ngày, `days_completed = 10`, `crashes = 0`, tất định trừ `duration_s` | Chạy `soak_cmd --seed 7 --days 10` hai lần; `tests/test_soak.py` (1/5/10 ngày, tất định, tham số sai, lặp D1–D5, giữ nâng cấp/tiền/ID xuyên ngày, `--mode day` vẫn 1..5) | [soak-seed7.json](../proof/phase-4/soak-seed7.json), [test_soak.py](../../tests/test_soak.py) | **ĐẠT** |
| AC-P4-04 | 3 cảnh báo chữ + biểu tượng (Cá Sấu gần, oxy sắp hết, khách sắp giận) | Scenario dựng tình huống, chụp client; `tests/test_phase4.py` | [hc-gather-monster-oxygen.png](../proof/phase-4/hc-gather-monster-oxygen.png), [hc-quan-customer.png](../proof/phase-4/hc-quan-customer.png) | **ĐẠT** |
| AC-P4-05 | Chế độ tương phản cao, cả ba cảnh báo hiện trong chế độ này | `?contrast=high` / phím H; hai ảnh trên chụp ở chế độ này | như AC-P4-04 | **ĐẠT** (chụp bằng Chrome headless; chưa có người chơi thử bằng tay) |
| AC-P4-06 | Từ clone sạch macOS/Linux chạy GUI ≤ 3 lệnh theo README | Clone commit vào thư mục mới, chạy 3 lệnh README, gọi `/state`, chạy unittest trong clone | [proof README](../proof/phase-4/README.md#clone-sạch) | **ĐẠT MỘT PHẦN** — chạy được trên Windows; chưa thử macOS/Linux thật |
| AC-P4-07 | Gói chạy được, đính kèm Release `v1.0.0` | `git archive` commit bàn giao thành `.zip`, giải nén, chạy lệnh 3 | release notes | **CHỜ** — gói tạo ở commit bàn giao; Release phải tạo trên GitHub web (máy không có `gh`) |
| AC-P4-08 | Regression P1–P3 còn hiệu lực | Toàn bộ unittest; test P3 không bị skip ở v1.3 (đổi điều kiện `>= 1.2`) | [p4_full_test.log](../proof/phase-4/p4_full_test.log) | **ĐẠT** — 115/115 |
| AC-P4-09 | README, CHANGELOG, CREDITS, LICENSE, release notes | Rà file | [README](../../README.md), [CHANGELOG](../../CHANGELOG.md), [CREDITS](../../CREDITS.md), [LICENSE](../../LICENSE), [release notes](../release-notes-v1.0.0.md) | **ĐẠT** |
| AC-P4-10 | Đủ 5 `docs/members/<handle>.md`, mỗi file ≤ 200 từ | Đếm file và số từ | `docs/members/` | **CHƯA ĐẠT** — còn thiếu bản phản tư của TV1 (`phong`); bốn bản hiện có đều ≤ 200 từ |
| AC-P4-11 | Tag `phase-4` và Release `v1.0.0` cùng SHA trên `main`, đúng hạn | `git ls-remote --tags` | — | **CHỜ** nhóm trưởng xác nhận đẩy |

## Đánh giá ngắn
- Đạt: manifest v1.3, bench có render, soak 10 ngày, 3 cảnh báo + tương phản cao, regression 115/115, tài liệu phát hành.
- Chưa đạt / chờ: phản tư của TV1; thử clone sạch trên macOS/Linux; Release + gói đính kèm phải tạo trên GitHub web.
- Ghi chú: tag `phase-3` chưa từng được gắn; code Phase 3 (nhánh `vuhieuvh-phase3`) được tích hợp vào `main` ở đầu Phase 4.
