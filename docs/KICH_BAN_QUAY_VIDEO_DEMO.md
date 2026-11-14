# KỊCH BẢN & HƯỚNG DẪN QUAY VIDEO DEMO E2E (MỤC 5 - CHECKLIST #7 & #8)
> **Đề tài 04:** Hệ thống báo khói cảnh báo sớm — **Nhóm 12 (HUIT IT4735)**  
> **Thời lượng chuẩn:** 2 phút 30 giây – 3 phút 00 giây (Quay 1 mạch hoặc ghép gọn, độ phân giải 1080p)  
> **Yêu cầu Excel của Thầy (*Checklist #7 & #8*):** Phải thể hiện đủ **luồng 4 tầng (Uplink + Downlink)**, **kịch bản bình thường**, **ít nhất 1 tình huống cảnh báo/lỗi (cháy + mất kết nối Timeout)**, **cơ chế tự động hóa (không chỉ bật tắt tay)** và **phân quyền/trạng thái cơ bản**.

---

## A. CHUẨN BỊ TRƯỚC KHI BẤM QUAY (3 PHÚT SETUP)

### 1. Bật đúng 3 cửa sổ và xếp gọn lên 1 màn hình:
1. **Cửa sổ Trái (40% màn hình):** Mô phỏng ESP32:
   * *Cách 1 (Khuyên dùng cho Wokwi Web):* Mở Project Wokwi công khai trên trình duyệt -> bấm nút **Start Simulation (Tam giác xanh)**, kéo gọn phần **Serial Monitor** ở dưới để thấy chữ in ra.
   * *Cách 2 (Dự phòng cực nhanh hoặc test phụ):* Double-click file **`CHAY_GIA_LAP_ESP32.bat`** ở thư mục gốc repo.
2. **Cửa sổ Phải (60% màn hình):** Node-RED Dashboard:
   * Double-click file **`CHAY_DASHBOARD.bat`** ở thư mục gốc repo (tự khởi động cả **Tầng 3 Middleware** + **Tầng 4 Dashboard** + ghi **CSV Log**).
   * Mở trình duyệt vào **`http://localhost:1880/ui`** (để ở chế độ Zoom 80–90% sao cho thấy gọn cả 3 cột trên 1 khung hình).
   * Mở sẵn **1 tab thứ 2** kế bên tại **`http://localhost:1880`** (giao diện Node-RED Flow Editor) để cuối video bấm qua khoe dây nối + node MQTT `connected` màu xanh.
3. **Telegram (Góc nhỏ bên phải hoặc quay màn hình điện thoại ghép vào):**
   * Mở Telegram Desktop / Web ở góc màn hình (hoặc để điện thoại ngay trước cam nếu quay 2 thiết bị) tại **Group Telegram Nhóm 12** có bot `@BaoKhoiCanhBao_bot`.

### 2. Công cụ quay màn hình nhanh trên Windows:
* **Cách dễ nhất (có sẵn trên Windows 10/11):** Nhấn tổ hợp phím **`Win + Alt + R`** để bắt đầu quay toàn màn hình (hoặc dùng **OBS Studio** chọn `Display Capture`).
* Bật **Micro** để vừa thao tác vừa thuyết minh ngắn gọn theo từng cảnh bên dưới (nếu không thu mic thì chèn phụ đề/text theo đúng kịch bản).

---

## B. KỊCH BẢN QUAY CHI TIẾT TỪNG GIÂY (6 CẢNH CHUẨN RUBRIC)

### 🎬 CẢNH 1 (0:00 – 0:25) — Khởi động & Trạng thái An toàn (`SAFE`)
* **Thao tác trên màn hình:**
  1. Chỉ chuột vào Serial Monitor của Wokwi / Giả lập thấy dòng **`-> THANH CONG!`** (HiveMQ SSL Port `8883`), **LED Xanh (GPIO25)** đang sáng, Quạt tắt, Còi tắt.
  2. Chỉ sang Dashboard (`localhost:1880/ui`):
     * Huy hiệu **`🟢 ESP32 ONLINE • HIVEMQ SSL 8883`** sáng xanh.
     * Đồng hồ Gauge khói màu xanh **< 300 PPM**, thẻ báo **`✅ MÔI TRƯỜNG AN TOÀN`**.
* **Lời đọc mẫu (hoặc text chú thích):**
  > *"Xin chào Thầy, đây là Demo toàn trình 4 tầng của Nhóm 12 — Đề tài Hệ thống báo khói cảnh báo sớm. Hiện tại ESP32 đang kết nối bảo mật HiveMQ SSL cổng 8883, cảm biến ở mức An toàn dưới 300 PPM, LED xanh sáng và trạng thái trên Dashboard là ONLINE."*

---

### 🎬 CẢNH 2 (0:25 – 0:55) — Kịch bản Cảnh báo sớm (`WARNING`: 300 – 600 PPM)
* **Thao tác trên màn hình:**
  1. Kéo thanh trượt cảm biến **MQ-2 (chiết áp)** trên Wokwi lên khoảng **420 – 480 PPM** *(nếu dùng giả lập Python thì gõ phím **`2`** rồi nhấn **Enter**)*.
  2. Chờ 1–2 giây chỉ rõ 3 thay đổi:
     * **Trên mạch Wokwi:** **LED Vàng (GPIO26)** sáng, **Quạt hút (LED xanh dương qua Relay GPIO18) TỰ ĐỘNG BẬT**, Còi **CHƯA hú** (tránh làm ồn khi nấu ăn nhẹ).
     * **Trên Dashboard:** Đồng hồ Gauge nhảy sang vùng **Vàng (~450 PPM)**, thẻ đổi sang **`⚠️ CẢNH BÁO: KHÓI TĂNG`**, và bảng **Lịch sử sự kiện Middleware (CSV)** tự thêm dòng `WARNING_HIGH_SMOKE`.
* **Lời đọc mẫu:**
  > *"Khi nồng độ khói tăng từ 300 đến 600 PPM, Tầng 1 và Tầng 3 tự động chuyển sang mức WARNING: bật đèn vàng và tự kích quạt hút tản khói mà chưa hú còi. Dữ liệu cập nhật ngay lên Dashboard và ghi vào lịch sử sự kiện CSV."*

---

### 🎬 CẢNH 3 (0:55 – 1:35) — Kịch bản Cháy khẩn cấp (`DANGER`) & Telegram Bot (< 1 giây)
* **Thao tác trên màn hình:**
  1. Kéo mạnh thanh trượt **MQ-2** lên **> 650 PPM** (khoảng 750–850 PPM) **hoặc** tăng nhiệt độ **DHT22 lên > 55°C** *(trên giả lập gõ phím **`3`** hoặc **`4`** rồi **Enter**)*.
  2. Chỉ rõ phản ứng tức thời:
     * **Trên Wokwi:** **LED Đỏ (GPIO27)** bật ngay, **Còi Buzzer (GPIO19) hú 1000Hz**, Quạt quay tối đa, Serial in dòng **`🚨 [ALERT] DA BAN GOI TIN KHAN CAP LEN TOPIC: nhom12/baokhoi/alert`**.
     * **Trên Dashboard:** Đồng hồ chuyển vùng **Đỏ**, thẻ báo **`🚨 NGUY CƠ HỎA HOẠN!`**, bảng **Nhật ký Telegram gần nhất** cập nhật thông số cháy, bảng CSV thêm `DANGER_AUTO_TRIGGER` / `FIRE_ALARM_URGENT`.
     * **Trên Telegram:** Quay rõ tin nhắn cảnh báo đỏ từ bot **`@BaoKhoiCanhBao_bot`** vừa nổ kèm PPM, nhiệt độ, độ ẩm và thời gian thực!
* **Lời đọc mẫu:**
  > *"Khi khói vượt 600 PPM hoặc nhiệt độ vượt 55°C, ESP32 phát gói tin Alert khẩn cấp ngay lập tức không cần chờ chu kỳ 5 giây. LED đỏ sáng, còi hú, quạt chạy hết công suất và Bot Telegram bắn cảnh báo về nhóm ngay tức thì."*

---

### 🎬 CẢNH 4 (1:35 – 2:10) — Điều khiển 2 chiều (`Downlink`) & Phân quyền `RBAC`
* **Thao tác trên màn hình:**
  1. Kéo **MQ-2** và **DHT22** về lại mức An toàn (**< 300 PPM**, **< 30°C** — giả lập gõ phím **`1` + Enter**) để thấy hệ thống tự khôi phục `SAFE` (`RECOVERY_SAFE`).
  2. Chứng minh **Downlink & Edge-Trigger không ghi đè nút tay**:
     * Trên Dashboard bấm nút **`🌀 BẬT QUẠT HÚT (MANUAL ON)`** $\rightarrow$ Nhìn sang Serial ESP32 thấy **`[MQTT DOWNLINK] ... FAN_ON`** và Quạt trên Wokwi bật sáng! Đợi qua 1 chu kỳ 5 giây vẫn giữ nguyên Quạt BẬT (không bị lệnh `AUTO` đè tắt mất).
     * Bấm **`⏹️ TẮT QUẠT HÚT (MANUAL OFF)`** $\rightarrow$ Quạt tắt.
     * Bấm **`🔄 CHẾ ĐỘ TỰ ĐỘNG (AUTO MODE)`** $\rightarrow$ Hệ thống nhường quyền lại cho cảm biến.
  3. Chứng minh **Phân quyền cơ bản (Tuần 6)**:
     * Ở ô **`🔑 Phân quyền:`**, đổi từ `Operator` sang **`Viewer (Giám sát - Chỉ xem)`**.
     * Bấm thử lại nút **`BẬT QUẠT HÚT`** $\rightarrow$ Hiện khung đỏ **`🔒 TỪ CHỐI LỆNH (CHỈ XEM)`**, ESP32 không nhận lệnh và bảng CSV ghi `AUTH_DENIED_VIEWER`. Sau đó chuyển lại về **`Operator`**.
* **Lời đọc mẫu:**
  > *"Ở chiều điều khiển ngược lại Downlink, từ Dashboard có thể gửi lệnh JSON FAN_ON, FAN_OFF, AUTO xuống ESP32. Nhờ cơ chế Edge-Trigger ở Middleware, lệnh thủ công được giữ ổn định không bị ghi đè. Đồng thời hệ thống có phân quyền Operator và Viewer để chặn thao tác trái phép khi chỉ giám sát."*

---

### 🎬 CẢNH 5 (2:10 – 2:45) — Kịch bản Bất thường `Timeout > 20s` (Tuần 7) & Minh chứng Node-RED + CSV
* **Thao tác trên màn hình:**
  1. Tắt/Tạm dừng mô phỏng ESP32 (trên Wokwi bấm nút Stop vuông đỏ; trên giả lập Python gõ phím **`p` + Enter**).
  2. *(Có thể tua nhanh 15 giây lúc edit hoặc giữ nguyên 20 giây)* $\rightarrow$ Quá 20 giây không có dữ liệu, huy hiệu trên Dashboard tự đổi sang màu đỏ: **`🔴 MẤT KẾT NỐI (OFFLINE TIMEOUT > 20s)`**, bảng Lịch sử ghi `OFFLINE_TIMEOUT`, và Bot Telegram gửi cảnh báo mất kết nối thiết bị!
  3. Bấm sang tab **`http://localhost:1880`** (Node-RED Flow Editor): lướt nhanh qua **2 tab (`Tầng 3: Middleware & Automation` và `Tầng 4: Dashboard & Telegram`)**, chỉ rõ các node MQTT hiện chữ xanh **`connected`**.
  4. Mở nhanh file **`logs/event_history.csv`** (trong VS Code / Excel / Notepad) để thấy dữ liệu log thật vừa được ghi.
* **Lời đọc mẫu:**
  > *"Với kịch bản bất thường ở Tuần 7, khi ngắt kết nối ESP32 quá 20 giây, Watchdog ở Tầng 3 lập tức phát hiện Timeout, chuyển trạng thái sang OFFLINE trên Dashboard, gửi cảnh báo mất kết nối qua Telegram và lưu vết đầy đủ vào file event_history.csv."*

---

### 🎬 CẢNH 6 (2:45 – 2:55) — Kết thúc
* **Thao tác:** Cho ESP32 chạy lại (Dashboard tự hồi phục `🟢 ESP32 ONLINE` và ghi `DEVICE_RECONNECTED`), nói lời cảm ơn Thầy Võ Hoàng Hải và kết thúc quay (`Win + Alt + R`).

---

## C. CHECKLIST TỰ KIỂM TRA TRƯỚC KHI NỘP VIDEO
- [ ] Video rõ nét chữ số PPM, chữ trên Serial Monitor và chữ trên Dashboard (không quay mờ/chói).
- [ ] Thấy rõ đủ **4 trạng thái**: `SAFE` -> `WARNING` -> `DANGER` (khói hoặc nhiệt) -> `OFFLINE TIMEOUT`.
- [ ] Thấy rõ **điều khiển 2 chiều**: Wokwi lên Web (Uplink) và Web xuống Wokwi (Downlink `FAN_ON`/`OFF`/`AUTO`).
- [ ] Thấy rõ tin nhắn **Telegram thật** và file **`logs/event_history.csv`** có dữ liệu thật.
- [ ] Thời lượng gọn khoảng **2:30 – 3:00 phút** (không dài lê thê).
