# TẦNG 4: APPLICATION / DASHBOARD, RBAC & TELEGRAM BOT
**Phụ trách chính:** Lục Xuân Thịnh (MSSV: 2001230931 - SV3 - Trưởng nhóm)

## Tính năng chính:
1. **Node-RED Dashboard Light Theme (`http://localhost:1880/ui`):**
   - **Cột 1 – Khí khói (MQ-2):** Đồng hồ Gauge 3 vùng màu (Xanh <300, Vàng 300–600, Đỏ >600), Thẻ trạng thái dung hợp đa cảm biến (bắt cả khói > 600 PPM và nhiệt > 55°C), Huy hiệu trạng thái thiết bị **`ONLINE` / `OFFLINE TIMEOUT > 20s`**.
   - **Cột 2 – Nhiệt ẩm & Lịch sử:** Biểu đồ biến thiên DHT22 theo thời gian thực, Thẻ số đo nhanh, **Bảng Lịch sử sự kiện Middleware** đồng bộ từ `logs/event_history.csv`.
   - **Cột 3 – Điều khiển 2 chiều & Phân quyền (RBAC):** Bộ chọn vai trò **`Operator` (Toàn quyền)** vs **`Viewer` (Chỉ xem - khóa nút bấm)**, 4 nút thao tác (`FAN_ON`, `FAN_OFF`, `AUTO`, `TEST 750 PPM`), Bảng phản hồi chế độ và Nhật ký Telegram gần nhất.
2. **Tích hợp Telegram Bot `@BaoKhoiCanhBao_bot`:**
   - Gửi cảnh báo cháy khẩn cấp (<1s) và cảnh báo thiết bị `OFFLINE > 20s`.
   - Bộ chống spam **Rate-limit 60 giây** tránh lỗi API 429.
   - Token & Chat ID thật nằm trong file `flows_dashboard_telegram.local.json` (được `.gitignore` bảo vệ).

## Khởi chạy Portable đa máy:
Chạy file **`CHAY_DASHBOARD.bat`** tại thư mục gốc repository (tự kiểm tra thư viện, tự tạo bản `.local.json` và dùng `nodered_settings.js`).
