# TẦNG 3: MIDDLEWARE / AUTOMATION ENGINE (NODE-RED)
**Phụ trách chính:** Châu Phát Lộc

## Nhiệm vụ:
1. Tiếp nhận dữ liệu định kỳ từ topic `nhom12/baokhoi/telemetry` và cảnh báo khẩn cấp từ `nhom12/baokhoi/alert`.
2. Viết hàm phân tích nồng độ khói `smoke_ppm`:
   - Nếu `smoke_ppm > 600`: Tự động xuất lệnh `{"cmd": "FAN_ON"}` và `{"buzzer": 1}` gửi vào topic `nhom12/baokhoi/cmd`.
   - Nếu `smoke_ppm < 300`: Tự động xuất lệnh `{"cmd": "AUTO"}`.
3. Ghi nhận log sự kiện (Event Logging) vào file hoặc context storage.
4. Đẩy dữ liệu ra giao diện Dashboard Tầng 4.

## Hướng dẫn sử dụng:
1. Copy nội dung file `flows_template.json`.
2. Trên Node-RED: Chọn `Menu` -> `Import` -> Paste JSON -> Bấm `Import`.
3. Cấu hình MQTT Node với thông tin HiveMQ SSL cổng 8883 (đã cấu hình sẵn trong flow).
4. Bấm `Deploy`.
