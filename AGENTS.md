# AGENTS.md — hướng dẫn chung cho mọi agent AI của nhóm

> Cập nhật file này qua các phase (lịch sử git phải cho thấy điều đó). Ngắn gọn, có lệnh chạy thật.

## Lệnh
- Test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`
- Headless: `python3 -m chonoi.headless --mode gather|quan|day --seed 1 --ticks 600 --out out.jsonl` (`day`: thêm `--days 1..5`)
- Chơi thử trên trình duyệt: `python3 -m chonoi.live --mode day --days 5` (hoặc `--mode gather|quan`; WASD, E, Space, R, P, 1/2, H)
- Benchmark có render (v1.3): `python3 -m chonoi.bench --seed 42 --duration 30 --out bench.json` (cần màn hình)
- Soak (v1.3): `python3 -m chonoi.soak --seed 7 --days 10 --out soak.json` (một tiến trình; `--mode day` vẫn giới hạn 1..5)
- Trước khi đẩy client: `node --check` phần `<script>` của `chonoi/web/index.html` (hành động retro P2).

## Cấu trúc & quy ước
- (Starter Python là TÙY CHỌN; nhóm có thể dùng ngôn ngữ khác nếu giữ Test Contract.) Khung do giảng viên cấp: `chonoi/{headless,inputs,scenario,contract,rng,ids,jsonl,inventory,runner,live}.py` và `chonoi/web/`. Hạn chế sửa; nếu phải sửa thì báo cả nhóm và ghi lại lý do.
- Luật chơi của nhóm: `chonoi/sim/gather.py`, `chonoi/sim/quan.py`, `chonoi/sim/day.py` (vòng ngày/Shop); công cụ v1.3: `chonoi/bench.py`, `chonoi/soak.py`.
- Kho v1.2: cá thể `{id, kind, fresh}`, `fresh` dạng `Fraction` bên trong — test so qua `format_item`/snapshot (ADR-0003).
- **Số liệu chỉ đọc từ `game.contract.json` / dữ liệu**, không hard-code trong luật.
- Mọi số ngẫu nhiên đi qua `Streams` (`chonoi/rng.py`); không dùng `random` toàn cục, không dùng đồng hồ hệ thống.
- Sắp danh sách thực thể bằng `ids.sort_by_id`; cấp id bằng `IdAllocator`.

## Nên tránh
- Không sửa `docs/contracts/`, `game.contract.json` (khóa contract) hoặc schema kho khi chưa báo cả nhóm (đổi hợp đồng ảnh hưởng mọi module).
- Không làm hỏng nhánh chính: trước khi đẩy, chạy test.
- Không bịa yêu cầu: chỗ mơ hồ thì ghi `docs/clarify.md` và hỏi PO.
- Không sửa test cho xanh khi luật sai; phải sửa luật hoặc ghi lý do đổi test trong commit.

## Quy tắc làm việc với agent
- Mỗi agent một việc rõ ràng (một lát). Cho agent đọc PRD/ticket đúng phase và hợp đồng kho trước.
- Agent làm xong phải chạy test và ghi kết quả vào mô tả commit hoặc `docs/proof/`; người đọc lại thay đổi trước khi đẩy.
- Sáng tạo thêm được khuyến khích nhưng phải tắt ở headless (xem README, mục "Tự do sáng tạo").

## Skills / hooks của nhóm
- `verify-contract` (.agents/skills/verify-contract/SKILL.md): Chạy kiểm tra contract, danh sách thành viên và tính tất định byte-identical trước khi merge/commit.
- `gen-scenario` (.agents/skills/gen-scenario/SKILL.md): Tạo các file fixture scenario chuẩn contract cho các ca biên (oxy, ngạt thở, đầy giỏ, khách kiên nhẫn).
