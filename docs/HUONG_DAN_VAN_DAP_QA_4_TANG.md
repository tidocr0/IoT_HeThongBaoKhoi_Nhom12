# HƯỚNG DẪN ÔN TẬP VẤN ĐÁP KỸ THUẬT 4 TẦNG IOT (Q&A CHI TIẾT)
## HỆ THỐNG BÁO KHÓI CẢNH BÁO SỚM THÔNG MINH - NHÓM 12 (ĐỀ TÀI 04)
**Môn học:** Internet of Things (IT4735) - Trường Đại học Công Thương TP.HCM (HUIT)  
**Giảng viên hướng dẫn & Chấm thi:** Thầy Võ Hoàng Hải  
**Bộ tài liệu:** Phục vụ bảo vệ Milestone M4 (Tuần 7 & Tuần 8) - Đạt chuẩn Rubric 100 điểm  

---

## 🎯 BẢNG PHÂN VAI VẤN ĐÁP THEO CHUYÊN TRÁCH TỪNG TẦNG
| Thành viên | MSSV | Vai trò chính | Tầng phụ trách bảo vệ |
| :--- | :---: | :--- | :--- |
| **Tăng Gia Huy** | 2001230313 | SV1 – Embedded & Sensing | **Tầng 1:** Thiết bị phần cứng, Cảm biến MQ-2, DHT22, FSM, Bộ lọc 10 mẫu, Relay & Buzzer. |
| **Châu Phát Lộc** | 2001230469 | SV2 – Connectivity & Middleware | **Tầng 2 & 3:** Mạng MQTT TLS 8883, Topic chuẩn, Watchdog Timeout 20s, Bộ lọc JSON, Audit Log CSV. |
| **Lục Xuân Thịnh** | 2001230931 | SV3 – Application & Trưởng nhóm | **Tầng 4 & Toàn luồng:** Dashboard, Bot Telegram, Edge-Trigger, Phân quyền RBAC, Kiểm thử E2E & Độ trễ. |

---

# PHẦN 1: TẦNG 1 - SENSING & EMBEDDED (DÀNH CHO SV1 - TĂNG GIA HUY)

### Câu 1: Em hãy giải thích nguyên lý hoạt động của cảm biến MQ-2 và tại sao trong code firmware phải dùng bộ lọc trung bình trượt 10 mẫu (SMOKE_SAMPLES = 10)?
* **Trả lời chuẩn:**
  * **Nguyên lý MQ-2:** Cảm biến sử dụng vật liệu nhạy cảm $\text{SnO}_2$ (Thiếc dioxit). Trong không khí sạch, độ dẫn điện thấp. Khi có khí dễ cháy hoặc khói, nồng độ khí càng cao thì độ dẫn điện của cảm biến càng tăng, làm sụt áp trên điện trở tải thay đổi. ESP32 đọc giá trị điện áp này qua chân ADC34 ($0 - 4095$ tương ứng $0 - 3.3\text{V}$) rồi ánh xạ sang thang đo $0 - 1000\text{ PPM}$.
  * **Tại sao cần bộ lọc trung bình trượt 10 mẫu:** Trong môi trường thực tế cũng như mô phỏng, tín hiệu analog luôn bị ảnh hưởng bởi nhiễu nguồn (power ripple), nhiễu điện từ xung quanh và sự dao động nhiệt của cảm biến. Nếu đọc giá trị thô từng mẫu (instantaneous raw sample), các "gai nhiễu" (spikes) đột ngột vượt qua ngưỡng có thể gây ra hiện tượng **báo động giả (false alarm)** làm hú còi inh ỏi. Thuật toán **Moving Average Filter với $N=10$ mẫu** hoạt động theo công thức:
    $$V_{\text{smooth}}[k] = \frac{1}{10} \sum_{i=0}^{9} V_{\text{raw}}[k-i]$$
    Giúp san phẳng các xung nhiễu đột biến ngắn hạn, chỉ giữ lại xu hướng nồng độ khói thực sự, đảm bảo hệ thống phản ứng chính xác và ổn định.

---

### Câu 2: Cảm biến DHT22 giao tiếp theo chuẩn gì? Tại sao hay gặp lỗi NaN (Not a Number) và nhóm xử lý ra sao trong firmware?
* **Trả lời chuẩn:**
  * **Chuẩn giao tiếp:** DHT22 sử dụng chuẩn truyền thông **Single-bus (1 dây tín hiệu số)**. ESP32 gửi xung Start (kéo chân GPIO xuống mức LOW trong khoảng 1-10ms), sau đó DHT22 phản hồi bằng chuỗi 40 bit dữ liệu (16 bit độ ẩm + 16 bit nhiệt độ + 8 bit checksum).
  * **Nguyên nhân lỗi NaN:** DHT22 cần thời gian lấy mẫu tối thiểu $2\text{ giây}$. Nếu vi điều khiển đọc quá nhanh hoặc đường dây bị lỏng, xung timing sai lệch vài micro-giây, hàm thư viện `dht.readTemperature()` không giải mã được checksum và sẽ trả về giá trị `NaN`.
  * **Cách xử lý trong code Nhóm 12:** Trong hàm `loop()` tại file `firmware_esp32/src/main.cpp`:
    ```cpp
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    globalHum  = isnan(h) ? 0.0 : h;
    globalTemp = isnan(t) ? 0.0 : t;
    ```
    Nhóm dùng toán tử ba ngôi kiểm tra hàm `isnan()`. Nếu phát hiện NaN, biến toàn cục sẽ gán về giá trị an toàn fallback ($0.0$), tuyệt đối không để giá trị rác lọt vào chuỗi JSON MQTT làm sập parser của Node-RED hay gây lỗi tính toán logic FSM.

---

### Câu 3: Hãy trình bày cấu trúc Máy trạng thái hữu hạn (FSM) 3 mức và giải thích Rule 3B (Đa cảm biến kết hợp) được thiết kế như thế nào?
* **Trả lời chuẩn:**
  * Hệ thống chia làm 3 mức trạng thái FSM rõ rệt:
    1. **Mức 1 - SAFE (An toàn):** Khói $< 300\text{ PPM}$ VÀ Nhiệt độ $\le 55^\circ\text{C}$ $\rightarrow$ Sáng **LED Xanh** (GPIO25), Quạt TẮT, Còi TẮT.
    2. **Mức 2 - WARNING (Cảnh báo sớm):** Khói từ $300 - 600\text{ PPM}$ VÀ Nhiệt $\le 55^\circ\text{C}$ $\rightarrow$ Sáng **LED Vàng** (GPIO26), **Quạt hút tự động BẬT** để thông khí, Còi vẫn TẮT để không gây hoảng loạn khi nấu ăn.
    3. **Mức 3 - DANGER (Nguy cơ hỏa hoạn khẩn cấp):**
       * **Trường hợp 3A (Khói dày đặc):** Khói $> 600\text{ PPM}$.
       * **Trường hợp 3B (Đa cảm biến - Cháy nhiệt cao ít khói):** Khói $< 300\text{ PPM}$ nhưng Nhiệt độ phòng $> 55^\circ\text{C}$ (ví dụ $62^\circ\text{C}$).
       $\rightarrow$ Cả 2 trường hợp đều kích hoạt: **LED Đỏ nhấp nháy liên tục**, **Quạt hút quay tối đa**, **Còi Buzzer hú tần số $1000\text{Hz}$**, và phát gói tin khẩn cấp `alert` lên Cloud.
  * **Ý nghĩa thực tế của Rule 3B:** Đây là bài toán thực tiễn quan trọng khi cháy các chất cồn, khí gas công nghiệp hóa lỏng (LPG), hoặc cháy âm ỉ trên trần cách nhiệt sinh nhiệt cực lớn mà không tỏa nhiều khói đen. Nếu chỉ đo khói đơn lẻ thì hệ thống sẽ bỏ lọt đám cháy chết người này.

---

### Câu 4: Khi Dashboard gửi lệnh Downlink `{"cmd":"FAN_ON"}` xuống ESP32, tại sao trạng thái quạt không bị vòng lặp 5 giây tự động đè lại?
* **Trả lời chuẩn:**
  * Trong firmware của Huy, nhóm thiết kế 2 biến cờ ghi đè độc lập: `manualFanOverride` và `manualBuzzerOverride`.
  * Bình thường ở chế độ `AUTO`, `manualFanOverride = false`, hàm `dieuKhienThietBi(state)` sẽ quyết định trạng thái quạt theo cảm biến.
  * Khi nhận gói Downlink có lệnh `"FAN_ON"`, cờ `manualFanOverride` được bật lên `true`. Trong các chu kỳ lặp 1s và 5s tiếp theo:
    ```cpp
    if (!manualFanOverride) {
        // Chỉ chạy logic tự động khi KHÔNG bị ghi đè thủ công
    }
    ```
    Khối lệnh tự động bị bỏ qua, quạt được giữ nguyên trạng thái `HIGH` và Serial Monitor in rõ `Quat: 1 (Manual)`. Trạng thái này được duy trì vĩnh viễn cho đến khi người dùng trên Web bấm nút `🔄 CHẾ ĐỘ TỰ ĐỘNG (AUTO)`, lúc này `manualFanOverride = false` thì quyền điều khiển mới trả về cho cảm biến.

---

# PHẦN 2: TẦNG 2 & 3 - NETWORK MQTT & MIDDLEWARE (DÀNH CHO SV2 - CHÂU PHÁT LỘC)

### Câu 5: Tại sao nhóm lại chọn giao thức MQTT chạy trên cổng bảo mật SSL/TLS 8883 thay vì cổng 1883 hay dùng HTTP REST API?
* **Trả lời chuẩn:**
  * **So với HTTP:** HTTP là giao thức Request/Response có overhead tiêu đề (header) rất lớn ($500 - 1000\text{ bytes}$ mỗi gói), đòi hỏi bắt tay TCP liên tục gây hao tốn băng thông và năng lượng của vi điều khiển. MQTT là mô hình Publish/Subscribe siêu nhẹ, header chỉ từ $2\text{ bytes}$, duy trì kết nối persistent thông qua gói PingReq/PingResp nhỏ gọn.
  * **So với MQTT Port 1883 thông thường:** Cổng 1883 truyền dữ liệu dạng plain text (bản rõ). Bất kỳ kẻ tấn công nào bắt được gói tin qua Wi-Fi (Man-in-the-Middle) đều đọc được Username, Password và nội dung cảm biến, thậm chí giả mạo lệnh Downlink tắt quạt còi khi đang có cháy. Cổng **8883 sử dụng mã hóa TLS (Transport Layer Security)**, toàn bộ payload được mã hóa đối xứng AES với chứng chỉ số, ngăn chặn hoàn toàn việc nghe lén hoặc giả mạo gói tin.

---

### Câu 6: Danh mục 3 Topic MQTT của nhóm được quy chuẩn như thế nào? Tại sao lại tách riêng Telemetry và Alert?
* **Trả lời chuẩn:**
  * Nhóm quy chuẩn 3 Topic phân định tường minh theo chuẩn công nghiệp:
    1. `nhom12/baokhoi/telemetry` (Uplink - Chu kỳ 5s, QoS 0): Dữ liệu định kỳ giám sát gồm nồng độ khói, nhiệt độ, độ ẩm, trạng thái quạt/còi.
    2. `nhom12/baokhoi/alert` (Uplink - Tức thời $< 1\text{s}$, QoS 1): Gói tin khẩn cấp bắn ngay khi chuyển sang trạng thái DANGER, đảm bảo gửi tin cậy với cơ chế bắt tay PUBACK.
    3. `nhom12/baokhoi/cmd` (Downlink - Chiều xuống, QoS 1): Nhận lệnh điều khiển cơ cấu chấp hành từ Web Dashboard (`FAN_ON`, `FAN_OFF`, `AUTO`, `BUZZER_OFF`).
  * **Lý do tách Telemetry và Alert:** Nếu gộp chung vào 1 topic, Broker và Middleware sẽ phải phân tích từng gói tin định kỳ 5s, gây trễ hàng đợi (queue delay). Khi tách riêng `alert`, Middleware có thể đăng ký luồng ưu tiên cao (High Priority Pipeline) để đẩy ngay cảnh báo về Telegram trong vòng chưa đầy $0.5\text{ giây}$ mà không phải chờ chu kỳ 5s.

---

### Câu 7: Em hãy giải thích cơ chế kiểm thử lỗi "Watchdog Timeout (20s)" ở Tầng 3 Middleware và cách hệ thống xử lý khi mất mạng?
* **Trả lời chuẩn:**
  * **Mục đích:** Trong IoT an toàn phòng cháy chữa cháy, việc thiết bị gặp sự cố (cháy đứt dây nguồn, router Wi-Fi sập, treo chip) mà Dashboard vẫn hiển thị thông số cũ màu xanh là cực kỳ nguy hiểm.
  * **Nguyên lý hoạt động Node-RED:** 
    * Mỗi khi nhận được 1 gói tin định kỳ tại `mqtt_in_telemetry_ui`, hàm `Kiểm Tra Dữ Liệu & Watchdog Timeout (20s)` sẽ gọi lệnh xóa bộ đếm cũ `clearTimeout(timer)` và đặt lại một bộ đếm mới $20\text{ giây}$.
    * Nếu thiết bị bị ngắt (tắt Wokwi hoặc ngắt mạng) quá 20s không có gói tin nào gửi lên, bộ đếm timer sẽ kích hoạt (fire):
      1. Đổi trạng thái hiển thị trên Dashboard thành `🔴 MẤT KẾT NỐI (OFFLINE TIMEOUT > 20s)`.
      2. Bắn thông báo cảnh báo mất kết nối về Telegram nhóm.
      3. Ghi ngay một bản ghi sự cố có mã `OFFLINE_TIMEOUT` vào file `logs/event_history.csv`.
    * Khi thiết bị có mạng trở lại, gói tin đầu tiên gửi lên sẽ nhận diện trạng thái phục hồi, đưa hệ thống về `🟢 KẾT NỐI BÌNH THƯỜNG (ONLINE)` và ghi nhận log `SYSTEM_ONLINE_SAFE`.

---

### Câu 8: File `logs/event_history.csv` lưu trữ những gì? Ý nghĩa của 7 mã sự kiện chuẩn trong hệ thống là gì?
* **Trả lời chuẩn:**
  * File CSV lưu vết toàn bộ hoạt động của hệ thống phục vụ công tác thanh tra và kiểm toán an toàn (Audit Trail). Mỗi dòng có 9 trường dữ liệu chuẩn:
    `Timestamp, Event_Code, Smoke_PPM, Temperature_C, Humidity_Pct, Fan_State, Buzzer_State, User_Role, Description`
  * **Ý nghĩa 7 mã sự kiện chuẩn:**
    1. `SYSTEM_ONLINE_SAFE`: Thiết bị khởi động hoặc vừa khôi phục kết nối an toàn.
    2. `WARNING_HIGH_SMOKE`: Khói vượt ngưỡng cảnh báo sớm ($300 - 600\text{ PPM}$), quạt tự bật.
    3. `FIRE_ALARM_URGENT`: Kích hoạt kịch bản hỏa hoạn khẩn cấp ($> 600\text{ PPM}$ hoặc $> 55^\circ\text{C}$).
    4. `MANUAL_FAN_ON`: Người dùng có quyền Operator bấm bật quạt cưỡng bức qua Web.
    5. `AUTH_DENIED_VIEWER`: Hệ thống bảo mật RBAC chặn thao tác bấm nút của người dùng quyền Viewer.
    6. `SET_AUTO_MODE`: Người dùng chuyển hệ thống từ điều khiển tay trở lại tự động.
    7. `OFFLINE_TIMEOUT`: Watchdog phát hiện mất kết nối phần cứng quá $20\text{ giây}$.

---

# PHẦN 3: TẦNG 4 & TOÀN LUỒNG E2E (DÀNH CHO SV3 - LỤC XUÂN THỊNH)

### Câu 9: Trình bày cơ chế chống spam cảnh báo Telegram bằng thuật toán Edge-Trigger (Phát hiện cạnh trạng thái)?
* **Trả lời chuẩn:**
  * **Vấn đề nếu dùng Level-Trigger:** ESP32 gửi dữ liệu định kỳ mỗi 5s. Khi nồng độ khói đạt $780\text{ PPM}$, nếu chỉ so sánh điều kiện $PPM > 600$ đơn thuần thì cứ mỗi 5 giây Bot Telegram sẽ bắn 1 tin nhắn. Chỉ sau 2 phút, điện thoại người dùng sẽ nhận $24\text{ tin nhắn rác}$, gây nghẽn API Telegram (lỗi HTTP 429 Too Many Requests) và làm người dùng tắt chuông thông báo.
  * **Giải pháp Edge-Trigger của Nhóm 12:** Nhóm lưu vết trạng thái trước đó vào bộ nhớ ngữ cảnh `lastAlertState`:
    * **Cạnh lên (Rising Edge):** Khi trạng thái trước đó là `SAFE` hoặc `WARNING` và trạng thái mới chuyển thành `DANGER` $\rightarrow$ Kích hoạt bắn **đúng 1 tin nhắn báo cháy khẩn cấp**. Trong các chu kỳ 5s tiếp theo, dù khói vẫn duy trì $> 600\text{ PPM}$, hệ thống nhận thấy `lastAlertState == DANGER` nên **tuyệt đối không gửi lặp lại**.
    * **Cạnh xuống (Falling Edge):** Khi khói hạ xuống $< 300\text{ PPM}$ và nhiệt $\le 55^\circ\text{C}$, hệ thống phát hiện chuyển từ `DANGER` về `SAFE` $\rightarrow$ Bắn **đúng 1 tin nhắn xác nhận môi trường đã an toàn trở lại**.

---

### Câu 10: Cơ chế phân quyền người dùng RBAC (Role-Based Access Control) trên Dashboard hoạt động như thế nào?
* **Trả lời chuẩn:**
  * Hệ thống chia làm 2 vai trò truy cập (Role) được quản lý qua nút chọn `ui_dropdown_rbac`:
    1. **Operator (Người vận hành):** Có toàn quyền điều khiển cơ cấu chấp hành. Khi bấm "BẬT QUẠT", lệnh JSON được đẩy xuống topic `nhom12/baokhoi/cmd` và ghi mã `MANUAL_FAN_ON` vào CSV.
    2. **Viewer (Khách / Người chỉ xem):** Chỉ được theo dõi số liệu Gauge và Biểu đồ.
  * **Cơ chế chặn ở Middleware Node-RED:** Trước khi lệnh nút bấm được truyền đến node `mqtt out`, nó bắt buộc phải đi qua hàm `Kiểm Tra Quyền RBAC`:
    ```javascript
    var currentRole = global.get("currentUserRole") || "Operator";
    if (currentRole === "Viewer") {
        // Chặn luồng, không cho truyền tới node MQTT Out
        return [null, { payload: denyFeedback }, { payload: csvDeny }];
    }
    ```
    Nếu là Viewer, lệnh bị chặn ngay lập tức, Dashboard hiển thị cảnh báo đỏ `🔒 TỪ CHỐI LỆNH (CHỈ XEM)`, đồng thời ghi nhận hành vi truy cập trái phép có mã `AUTH_DENIED_VIEWER` vào nhật ký kiểm toán.

---

### Câu 11: Em hãy giải thích toàn bộ luồng truyền thông hai chiều End-to-End (Uplink và Downlink) và kết quả đo độ trễ?
* **Trả lời chuẩn:**
  * **Luồng Uplink (Chiều lên - Thu thập & Cảnh báo):**
    $\text{MQ-2 / DHT22} \xrightarrow{\text{Analog/GPIO}} \text{ESP32 (Lọc 10 mẫu)} \xrightarrow{\text{MQTT TLS 8883}} \text{HiveMQ Cloud} \xrightarrow{\text{TLS}} \text{Node-RED Middleware} \xrightarrow{} \begin{cases} \text{Web Dashboard (Gauge, Chart)} \\ \text{Telegram Bot API (HTTPS 443)} \end{cases}$
  * **Luồng Downlink (Chiều xuống - Điều khiển cơ cấu):**
    $\text{Nút bấm Dashboard} \xrightarrow{\text{RBAC Gate}} \text{Topic nhom12/baokhoi/cmd} \xrightarrow{\text{HiveMQ TLS}} \text{ESP32 (Hàm callback)} \xrightarrow{\text{Kích Relay/Buzzer}} \text{Quạt quay / Còi tắt}$
  * **Đo độ trễ thực tế:**
    * **Độ trễ Uplink Telemetry:** $\approx 120 - 180\text{ ms}$ (tính từ lúc ESP32 `client.publish()` đến khi Gauge trên Dashboard cập nhật).
    * **Độ trễ Downlink Command:** $\approx 150 - 220\text{ ms}$ (từ lúc nhấp chuột trên Web đến khi Serial Monitor Wokwi in `[CMD THUC THI]`).
    * **Độ trễ Cảnh báo Telegram:** $\approx 450 - 650\text{ ms}$ (do đi qua Cloud API của Telegram tại châu Âu).
    Tất cả các độ trễ đều nhỏ hơn rất nhiều so với ngưỡng yêu cầu thời gian thực của đề tài ($< 1.0\text{ giây}$).

---

### Câu 12: Thầy hỏi: "Nếu Broker HiveMQ Cloud bị sập hoặc cáp quang biển bị đứt, trạm báo khói tại chỗ có còn báo cháy và bật quạt được không?"
* **Trả lời chuẩn 100 điểm:**
  * **Thưa Thầy: VẪN HOẠT ĐỘNG HOÀN TOÀN TẠI CHỖ (Edge Computing / Local Autonomous)!**
  * Đây là điểm cốt lõi trong kiến trúc nhúng của nhóm em: Toàn bộ logic máy trạng thái FSM 3 mức (`docVaLocKhoi`, `capNhatDenLED`, `dieuKhienThietBi`) được thực thi cục bộ ngay trên bộ nhớ Flash của ESP32 trong Chu kỳ 1 ($1\text{ giây}$).
  * Broker MQTT và Cloud chỉ làm nhiệm vụ giám sát từ xa (Tầng 2 - 4). Nếu đứt mạng, hàm `client.connected()` trả về `false`, ESP32 vẫn phát hiện khói $> 600\text{ PPM}$ ngay tại giây đầu tiên, vẫn tự động bật Relay quạt hút, hú còi và nhấp nháy LED đỏ. Sau đó hàm `reconnect()` chạy ngầm non-blocking mỗi 4s để tự động nối lại mạng khi có kết nối mà không bao giờ làm treo hệ thống báo cháy tại hiện trường.

---
*Tài liệu đã được biên soạn đồng bộ với mã nguồn và kịch bản thực nghiệm của Nhóm 12.*
