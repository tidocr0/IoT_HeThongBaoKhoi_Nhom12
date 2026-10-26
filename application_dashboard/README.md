# TẦNG 4: APPLICATION / DASHBOARD & TELEGRAM BOT
**Phụ trách chính:** Lục Xuân Thịnh (Lead)

## Nhiệm vụ:
1. Giao diện Giám sát thời gian thực (Node-RED Dashboard):
   - Đồng hồ Gauge hiển thị nồng độ `smoke_ppm` với 3 dải màu: Xanh (0-300), Vàng (300-600), Đỏ (600-1000).
   - Biểu đồ Chart đường nhiệt độ & độ ẩm.
   - Các nút Switch điều khiển thủ công: Bật/Tắt Quạt hút, Bật/Tắt Còi, Chế độ Tự động (AUTO).
2. Tích hợp Telegram Bot cảnh báo từ xa:
   - Khi có sự cố cháy (nhận từ `nhom12/baokhoi/alert` hoặc khi `smoke_ppm > 600`), bot tự động bắn tin nhắn về nhóm chat / điện thoại.
   - Nội dung tin nhắn:
     ```text
     🚨 [CẢNH BÁO CHÁY KHẨN CẤP]
     Vị trí: Buồng cảm biến khói Nhóm 12
     Nồng độ khói: 750 PPM
     Nhiệt độ hiện tại: 58.5 °C
     Trạng thái quạt hút: ĐANG BẬT TỐI ĐA
     Thời gian ghi nhận: 10:30:15 - 26/10/2026
     ```
