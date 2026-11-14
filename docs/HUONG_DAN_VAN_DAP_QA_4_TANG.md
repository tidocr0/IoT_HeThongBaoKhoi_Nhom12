# HƯỚNG DẪN VẤN ĐÁP (Q&A) 4 TẦNG & BẢNG KIỂM THỬ HỆ THỐNG — NHÓM 12
> **Quy định bắt buộc trong Syllabus Excel (*Sheet Phân công nhóm & Kế hoạch 10 tuần*):**  
> *"Mỗi sinh viên phải có evidence công việc cá nhân VÀ giải thích được toàn bộ luồng E2E 4 tầng, không chỉ phần mình phụ trách."*

---

## 1. BẢNG TEST INPUT $\rightarrow$ PROCESSING $\rightarrow$ OUTPUT (DELIVERABLE TUẦN 3, 7, 8, 9)

| Mã TC | Kịch bản kiểm thử | Input (Tầng 1 / Người dùng) | Processing (ESP32 & Middleware Tầng 3) | Output kỳ vọng (LED, Quạt, Còi, Dashboard, Telegram, CSV) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC01** | Môi trường Bình thường (`SAFE`) | MQ-2: `135 PPM`, DHT22: `27.5°C` | Lọc Moving Avg $N=5$; FSM -> `SAFE`; Edge Trigger ghi nhận online | LED **Xanh** sáng; Quạt TẮT, Còi TẮT; Dashboard **ONLINE / An toàn**; CSV ghi `SYSTEM_ONLINE_SAFE` | ✅ ĐẠT |
| **TC02** | Chớm có khói (`WARNING`) | MQ-2: `440 PPM`, DHT22: `36.2°C` | FSM -> `WARNING` ($300 \le \text{PPM} \le 600$); Middleware giữ `AUTO` (không đè Manual) | LED **Vàng** sáng; Quạt **TỰ BẬT** tản khói; Còi **TẮT**; Dashboard màu **Vàng**; CSV ghi `WARNING_HIGH_SMOKE` | ✅ ĐẠT |
| **TC03** | Cháy do khói cao (`DANGER`) | MQ-2: `780 PPM`, DHT22: `62.0°C` | FSM -> `DANGER`; `previousState != DANGER` bắn ngay Alert QoS 1 (<1s) | LED **Đỏ** sáng; Quạt **MAX**, Còi **1000Hz**; Dashboard **Đỏ**; Bot Telegram nổ tin; CSV ghi `FIRE_ALARM_URGENT` | ✅ ĐẠT |
| **TC04** | Cháy âm ỉ nhiệt cao không khói (`DANGER`) | MQ-2: `190 PPM`, DHT22: `58.5°C > 55°C` | Điều kiện OR đa cảm biến (`ppm > 600 \|\| temp > 55.0`) -> `DANGER` | LED **Đỏ**, Quạt MAX, Còi **1000Hz**; Dashboard hiện **Đỏ** dù PPM thấp; Telegram cảnh báo | ✅ ĐẠT |
| **TC05** | Điều khiển 2 chiều & Chống đè Manual (`Edge-Trigger`) | Bấm nút `FAN_ON` rồi `FAN_OFF` trong `SAFE`/`WARNING`, đợi > 10s | Node-RED set `manualOverride=true`; Edge Trigger bỏ qua gói telemetry lặp chu kỳ 5s | ESP32 giữ đúng trạng thái `Manual` không bị `AUTO` tắt mất quạt sau 5s; CSV ghi `MANUAL_FAN_ON/OFF` | ✅ ĐẠT |
| **TC06** | Phân quyền cơ bản (`RBAC`) | Đổi Dropdown sang `Viewer (Chỉ xem)` rồi bấm `FAN_ON` | `fn_auth_gate` kiểm tra `userRole === 'VIEWER'` $\rightarrow$ Chặn lệnh MQTT | Không gửi MQTT xuống ESP32; Dashboard hiện `🔒 TỪ CHỐI LỆNH`; CSV ghi `AUTH_DENIED_VIEWER` | ✅ ĐẠT |
| **TC07** | Kịch bản bất thường: Mất kết nối (`Timeout > 20s`) | Ngắt nguồn / Tạm ngưng ESP32 quá `20 giây` | Watchdog `trigger` (20s) hết hạn $\rightarrow$ `OFFLINE_TIMEOUT` | Dashboard đổi badge Đỏ **`OFFLINE TIMEOUT > 20s`**; Telegram báo mất kết nối; CSV ghi `OFFLINE_TIMEOUT` | ✅ ĐẠT |
| **TC08** | Phục hồi kết nối (`Reconnect`) | Cấp lại nguồn / Bật lại ESP32 gửi Telemetry | `reconnect()` tự động nối lại Broker sau 4s; Middleware nhận gói mới | Dashboard về **`🟢 ESP32 ONLINE`**; CSV ghi `DEVICE_RECONNECTED` | ✅ ĐẠT |

---

## 2. TÓM TẮT LUỒNG 4 TẦNG BẰNG 4 CÂU (AI CŨNG PHẢI THUỘC)

1. **Tầng 1 (Sensing - Huy):** ESP32 đọc cảm biến khói **MQ-2 (ADC34)** qua bộ lọc trung bình trượt **N=5**, đọc nhiệt/ẩm **DHT22 (GPIO15)**, phân loại 3 mức FSM (**SAFE / WARNING / DANGER**) để điều khiển **3 LED (25, 26, 27)**, **Relay Quạt (18)** và **Còi 1000Hz (19)**.
2. **Tầng 2 (Network - Lộc):** ESP32 dùng Wi-Fi kết nối tới **HiveMQ Cloud MQTT Broker** cổng bảo mật **SSL/TLS 8883** (`iot_t4_1315`), giao tiếp qua 3 Topic chuẩn: `telemetry` (định kỳ 5s), `alert` (khẩn cấp <1s), và `cmd` (nhận lệnh điều khiển từ xa).
3. **Tầng 3 (Middleware - Lộc):** Node-RED không chỉ chuyển tiếp thô mà chạy **Edge-Trigger Rule Engine** (chỉ bắn lệnh tự động khi đổi mức, tránh đè nút tay `FAN_ON/OFF`), chạy **Watchdog Timeout > 20s** phát hiện mất kết nối thiết bị, và ghi vết mọi sự cố ra file **`logs/event_history.csv`**.
4. **Tầng 4 (Application - Thịnh):** **Node-RED Dashboard** (Light Theme) vẽ đồng hồ Gauge, biểu đồ nhiệt ẩm, bảng lịch sử CSV, badge Online/Offline, kiểm tra phân quyền **Operator/Viewer**, nút bấm Downlink và tích hợp **Bot Telegram `@BaoKhoiCanhBao_bot`** chống spam 60 giây.

---

## 3. BỘ CÂU HỎI VẤN ĐÁP THƯỜNG GẶP & CÁCH TRẢ LỜI GHI ĐIỂM

### 🔹 Nhóm câu hỏi Tầng 1 (Thường hỏi Huy, nhưng Lộc & Thịnh phải biết):
1. **Tại sao phải dùng bộ lọc trung bình trượt `N=5` (`docVaLocKhoi`)?**
   * *Trả lời:* Tín hiệu ADC từ MQ-2 dễ bị gai nhiễu điện áp ngẫu nhiên làm số PPM nhảy giật cục, dễ báo cháy giả. Lấy trung bình cộng 5 mẫu gần nhất (mỗi giây 1 mẫu) bằng vòng đệm giúp số đo mượt, ổn định mà vẫn phản ứng đủ nhanh trong vài giây.
2. **Tại sao có khói mức `WARNING` (300–600 PPM) lại bật quạt nhưng KHÔNG bật còi?**
   * *Trả lời:* Đây là ngưỡng khói nhẹ khi nấu ăn hoặc mới chớm rò khói. Bật quạt giúp tản khói sớm mà không gây hoảng loạn/tiếng ồn giả. Chỉ khi vượt 600 PPM hoặc nhiệt độ > 55°C (`DANGER`) mới hú còi 1000Hz và báo Telegram.
3. **Tại sao Wokwi dùng biến trở (Potentiometer) thay cho linh kiện MQ-2?**
   * *Trả lời:* Thư viện mặc định của Wokwi mô phỏng MQ-2 bằng module analog hoặc biến trở cấp áp 0–3.3V vào chân ADC 34 (`map(avgADC, 0, 4095, 0, 1000)`). Nguyên lý đọc điện áp analog trên chân GPIO34 giống hệt cảm biến MQ-2 thật, cho phép kéo mô phỏng mượt từ 0 đến 1000 PPM khi demo.
4. **Nếu cảm biến khói chưa kịp nhận khói mà phòng đã cháy nóng > 55°C thì sao?**
   * *Trả lời:* Nhờ logic dung hợp đa cảm biến (`globalSmokePPM > 600 || globalTemp > 55.0`), hệ thống vẫn lập tức nhảy trạng thái `DANGER`, bật còi + quạt + bắn Alert trong 1 giây.

### 🔹 Nhóm câu hỏi Tầng 2 & 3 (Thường hỏi Lộc, nhưng Huy & Thịnh phải biết):
5. **Tại sao dùng port 8883 thay vì 1883? HiveMQ có bảo mật gì?**
   * *Trả lời:* Port 1883 là MQTT truyền rõ (plaintext) dễ bị nghe lén payload và cướp lệnh điều khiển quạt. Port **8883** bọc toàn bộ dữ liệu bằng **TLS/SSL**, kết hợp xác thực **Username/Password** và Client ID riêng cho mỗi node kết nối.
6. **Tại sao tách riêng `telemetry` (5s) và `alert` (<1s)? Sao không dùng 1 topic?**
   * *Trả lời:* `telemetry` gửi định kỳ mỗi 5s với QoS 0 để vẽ biểu đồ nhẹ nhàng. Nếu gộp chung vào chu kỳ 5s thì khi cháy có thể trễ tới 5 giây vàng mới báo động. Tách topic `alert` (QoS 1) kết hợp bắt cạnh `previousState != DANGER && currentState == DANGER` giúp báo động đến Dashboard & Telegram ngay lập tức (<1s) và đảm bảo broker nhận ít nhất 1 lần.
7. **Middleware của nhóm em làm gì mà không bị coi là "chỉ forward dữ liệu"?**
   * *Trả lời:* Tầng 3 làm 3 xử lý thật: (1) **Edge-Trigger Rule Engine** kiểm tra ngưỡng và đồng bộ cờ `manualOverride` để không ghi đè thao tác thủ công của người dùng; (2) **Watchdog 20 giây** phát hiện mất kết nối ESP32; (3) **Ghi Event Log ra file CSV** (`logs/event_history.csv`) và đẩy bảng lịch sử lên Dashboard.
8. **Nếu người dùng vừa bấm `FAN_ON` thủ công mà khói đang dưới 300 PPM thì chuyện gì xảy ra sau 5 giây?**
   * *Trả lời:* Nhờ cơ chế **Edge-Trigger** và cờ `manualFanOverride` ở cả ESP32 lẫn Node-RED, khi mức khói không đổi (`SAFE -> SAFE`), Middleware không bắn lặp lệnh `AUTO` nên quạt vẫn giữ đúng trạng thái `MANUAL` người dùng mong muốn, chỉ trừ khi có cháy khẩn cấp (`DANGER`) thì hệ thống mới ưu tiên an toàn tính mạng bật tối đa.

### 🔹 Nhóm câu hỏi Tầng 4 & Tích hợp Hệ thống (Thường hỏi Thịnh, nhưng Huy & Lộc phải biết):
9. **Làm sao Dashboard xử lý được chống spam Telegram khi cháy kéo dài 5 phút?**
   * *Trả lời:* Hàm `fn_telegram_check` lưu mốc `lastAlertTime` trong context Node-RED và áp dụng **Rate-limit 60 giây**, đảm bảo khi khói giữ >600 PPM liên tục thì cứ tối đa 60s mới gửi lại 1 tin, tránh bị Telegram khóa API (lỗi `429 Too Many Requests`).
10. **Nhóm chứng minh phần "phân quyền / trạng thái cơ bản" (Tuần 6) bằng gì?**
    * *Trả lời:* Chứng minh qua 3 lớp: (1) Trạng thái thiết bị `ONLINE / OFFLINE TIMEOUT > 20s` theo thời gian thực trên UI; (2) Bộ chọn phân quyền **Operator vs Viewer** trên Dashboard (`fn_auth_gate` khóa hoàn toàn nút điều khiển và ghi log `AUTH_DENIED_VIEWER` nếu tài khoản chỉ có quyền Xem); (3) Phân quyền truy cập MQTT bằng tài khoản SSL và bảo mật Telegram Token bằng `.gitignore` (`*.local.json`).
11. **Nếu mất kết nối Internet ở ESP32 hoặc ESP32 bị treo nguồn, hệ thống biết không?**
    * *Trả lời:* Có. Tầng 3 có node Watchdog đợi tối đa 20 giây giữa 2 gói Telemetry. Quá 20s không thấy ESP32 gửi lên sẽ tự đánh dấu `OFFLINE_TIMEOUT`, bật cảnh báo đỏ trên Dashboard, gửi cảnh báo qua Telegram và ghi CSV. Khi ESP32 có mạng lại, `reconnect()` tự nối Broker mỗi 4s và ghi `DEVICE_RECONNECTED`.
12. **Tại sao trên GitHub không lưu Token Telegram thật?**
    * *Trả lời:* Để đảm bảo nguyên tắc An toàn & Bảo mật IoT (không rò rỉ khóa bí mật lên repo công khai). File tracked trên Git chỉ giữ placeholder (`<YOUR_TELEGRAM_BOT_TOKEN>`), còn file chạy thật `*.local.json` và `*_cred.json` được chặn tuyệt đối trong `.gitignore`.
