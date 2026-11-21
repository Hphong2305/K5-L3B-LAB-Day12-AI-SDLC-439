# Phase 3 — Kho và giữ chỗ Quán

Chạy từ thư mục `ccc/` trên Windows, Python 3.12:

```powershell
$env:PYTHONPATH='tests;.'
$env:PYTHONUTF8='1'
python -m unittest test_quan_customers test_quan_day_menu -v
```

- **Test TV3:** 10/10 đạt. Kiểm tra kho cá thể, ID trùng, độ tươi ngoài miền, giữ trùng giữa hai đơn, ưu tiên tươi nhất, biên 30, nhả cả phần giữ, thử lại một lần, tiêu kho theo ID và menu ngày.
- **Smoke Gather → file kho → Quán:** Hai tiến trình trả mã 0. Gather xuất I2 (`ca_loc`, fresh 89.992). Quán nhận cùng ID và độ tươi ở tick 0. Tick 120, độ tươi là 89.492 và đơn giữ `["I2"]`. File mẫu cũ dạng đếm trả mã 2 theo schema v1.2.
- **Suite đầy đủ:** 87 test, 73 đạt, 9 fail và 5 error. Các ca chưa đạt dùng fixture hoặc kỳ vọng schema v1.1 trong `test_day_mode.py`, `test_gather_actions.py`, `test_gather_fish.py`, `test_python_starter_units.py`, `test_quan_leftovers.py` và `test_smoke_p1.py`. Các file ngoài phạm vi TV3 được giữ để người phụ trách chuyển đổi theo ADR-0003.

## Điểm nối cho TV4

`_consume_reserved(customer)` xóa và trả về đúng các nguyên liệu đã giữ, với `fresh` dạng `Fraction` tại thời điểm bếp lấy. TV4 có thể dùng giá trị trả về để chốt giá.

Bản triển khai xử lý hao tươi sau bước giảm kiên nhẫn và trước tương tác bếp. Khi độ tươi bằng nhau, chọn ID nhỏ hơn theo `sort_by_id`. Mỗi đơn có tối đa một lần giữ lại trong vòng đời của đơn. Đơn `unfulfillable` tiếp tục đếm kiên nhẫn và bếp bỏ qua. Cần đối chiếu các lựa chọn này với bản đầy đủ TICKET-03/Test Contract v1.2.

## Kiểm tra sau khi ghép `origin/main` tại c146914

Day handoff dùng snapshot để kiểm độ tươi dạng JSON; test món thừa kiểm `reserved` và `stock` là mảng. Ba test đích cho Day, smoke Gather → Quán và món thừa đều đạt. Chạy lại `python -m unittest discover -s tests` với Python UTF-8 và Windows launcher `python3.exe` trong PATH tạm cho kết quả **89/89 đạt**.
