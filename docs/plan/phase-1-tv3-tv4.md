# Phối hợp TV3 và TV4 trong Phase 1

Đề xuất để TV3 và TV4 xác nhận trước khi sửa `chonoi/sim/quan.py`.

## Dữ liệu dùng chung

Starter lưu khách trong `self.customers` và nguyên liệu giữ chỗ trong `customer["reserved"]`. Hai phần dùng chung `order_id`, `order_tick`, mã món, trạng thái đơn và `patience_ticks_left`. Khi xác nhận giao diện, đối chiếu tên trường và giá trị trạng thái với mục F phần Quán của Test Contract.

## Giữ, trừ và nhả nguyên liệu

- Khi khách gọi, TV3 ghi số lượng cần vào `reserved` của khách. Kho khả dụng bằng `self.stock` trừ tổng lượng đang giữ cho các đơn.
- Khi bếp bắt đầu nấu, TV4 chọn đơn đủ điều kiện theo Test Contract, trừ đúng lượng đã giữ khỏi `self.stock`, xóa phần giữ và cập nhật trạng thái đơn trong cùng bước.
- Khi khách rời mà đơn còn nguyên liệu đang giữ, TV3 giải phóng phần giữ. `self.stock` chỉ thay đổi ở thời điểm bếp tiêu nguyên liệu.

## Phân vùng trong `quan.py`

- **TV3** phụ trách khởi tạo khách từ fixture, lịch khách đến, chọn món, giữ nguyên liệu và xử lý hết kiên nhẫn.
- **TV4** phụ trách bếp, tương tác tại bếp hoặc bàn, bưng món, phục vụ, ăn, thanh toán và kết ca.
- Mỗi người viết logic trong các hàm riêng. Hai người thống nhất thứ tự gọi trong `step()` theo mục F và cử một người ghép các lời gọi. Cần xác nhận cách xử lý khi khách hết kiên nhẫn đúng tick người chơi tương tác.

## Kiểm tra khi tích hợp

1. Khách gọi món, bếp nhận đơn và trừ đúng nguyên liệu một lần.
2. Khách rời trước khi bếp nhận đơn, giải phóng phần giữ để nguyên liệu khả dụng trở lại.
