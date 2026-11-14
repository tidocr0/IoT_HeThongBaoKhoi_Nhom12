# TẦNG 3: MIDDLEWARE / AUTOMATION ENGINE (NODE-RED)
**Phụ trách chính:** Châu Phát Lộc (MSSV: 2001230469 - SV2)

## Nhiệm vụ & Xử lý Logic Thực (Không chỉ Forward thô):
1. **Tiếp nhận 2 luồng Uplink qua HiveMQ SSL 8883:**
   - `nhom12/baokhoi/telemetry` (định kỳ 5 giây)
   - `nhom12/baokhoi/alert` (khẩn cấp < 1 giây khi vào mức `DANGER`)
2. **Edge-Trigger Automation Engine (Chống ghi đè lệnh Manual):**
   - Chỉ phát lệnh xuống `nhom12/baokhoi/cmd` khi trạng thái môi trường **chuyển ngưỡng** (`SAFE` $\leftrightarrow$ `WARNING` $\leftrightarrow$ `DANGER`).
   - Khi khói > 600 PPM hoặc nhiệt > 55°C: ưu tiên an toàn tính mạng $\rightarrow$ gửi `{"cmd": "FAN_ON"}` + `{"buzzer": 1}`.
   - Khi đang ở chế độ `Manual` (`FAN_ON`/`FAN_OFF` do người dùng bấm trên Web), Middleware giữ nguyên `manualOverride` ở mức `SAFE`/`WARNING`, tuyệt đối không bắn lặp `AUTO` làm tắt quạt mỗi 5 giây.
3. **Watchdog Phát hiện Mất kết nối (`Timeout > 20s`):**
   - Quá 20 giây không có Telemetry mới từ ESP32 $\rightarrow$ kích hoạt sự kiện `OFFLINE_TIMEOUT`, báo đỏ Dashboard, báo Telegram và ghi CSV.
4. **Ghi Log Sự Kiện Thật (`Event History CSV`):**
   - Tự động lưu các biến cố (`SYSTEM_ONLINE_SAFE`, `WARNING_HIGH_SMOKE`, `DANGER_AUTO_TRIGGER`, `RECOVERY_SAFE`, `MANUAL_FAN_ON/OFF`, `OFFLINE_TIMEOUT`, `DEVICE_RECONNECTED`, `AUTH_DENIED_VIEWER`) vào file **`logs/event_history.csv`** và đẩy lên bảng lịch sử trên Dashboard.

## Cách chạy nhanh:
* **Khuyên dùng (Chạy chung cả Tầng 3 + Tầng 4):** Double-click **`CHAY_DASHBOARD.bat`** ở thư mục gốc repo.
* **Hoặc import riêng Tab Tầng 3:** Mở Node-RED (`http://localhost:1880`) $\rightarrow$ `Menu` $\rightarrow$ `Import` $\rightarrow$ chọn file `middleware_nodered/flows_template.json` $\rightarrow$ điền tài khoản HiveMQ (`iot_t4_1315` / `iot_t4_1315`) $\rightarrow$ `Deploy`.
