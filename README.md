# ĐỒ ÁN MÔN HỌC IOT (IT4735) - NHÓM 12
## ĐỀ TÀI 04: HỆ THỐNG BÁO KHÓI CẢNH BÁO SỚM (EARLY FIRE & SMOKE DETECTION SYSTEM)

> **Trường Đại học Công Thương TP.HCM (HUIT)**  
> **Khoa Công nghệ Thông tin - Bộ môn Kỹ thuật Mạng & IoT**  
> **Giảng viên hướng dẫn:** Thầy Võ Hoàng Hải
> **Tiêu chuẩn đồ án:** 10 tuần / Tối thiểu 60 giờ mỗi sinh viên / Đáp ứng trọn vẹn Rubric 100 điểm.

---

## 👥 THÀNH VIÊN NHÓM 12 & PHÂN CÔNG VAI TRÒ

| STT | Họ và Tên | MSSV | Vai trò chính | Nhiệm vụ đảm trách |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Lục Xuân Thịnh** | **2001230931** | **Trưởng nhóm (Lead)** | Kiến trúc hệ thống, Tầng 4 (Dashboard & Telegram Bot), Báo cáo & Quản trị tiến độ |
| 2 | **Châu Phát Lộc** | **200123...** | **Kỹ sư Tầng 2 & 3** | Cấu hình HiveMQ SSL 8883, Middleware Node-RED, Logic tự động hóa & Event Logging |
| 3 | **Tăng Gia Huy** | **200123...** | **Kỹ sư Tầng 1** | Mô phỏng Wokwi ESP32, Cảm biến MQ-2, DHT22, Cơ cấu chấp hành (Quạt, Còi, 3 LED) |

---

## 🏛️ KIẾN TRÚC 4 TẦNG IOT CHUẨN MỰC

```text
+-----------------------------------------------------------------------------------+
|                           TẦNG 4: APPLICATION / PLATFORM                         |
|  - Node-RED Dashboard: Đồng hồ đo PPM khói, Biểu đồ nhiệt độ/độ ẩm, Nút bật/tắt quạt|
|  - Telegram Bot: Tự động gửi tin nhắn báo động cháy khẩn cấp kèm giá trị PPM        |
+-----------------------------------------▲-----------------------------------------+
                                          | (HTTP / WebSocket / MQTT)
+-----------------------------------------▼-----------------------------------------+
|                        TẦNG 3: MIDDLEWARE / AUTOMATION ENGINE                     |
|  - Node-RED Flow Engine: Lọc nhiễu, phân tích JSON payload từ ESP32               |
|  - Automation Rules: Tự động quyết định bật quạt hút & còi hú khi vượt ngưỡng     |
|  - Event Logging: Lưu vết lịch sử các lần cảnh báo                                |
+-----------------------------------------▲-----------------------------------------+
                                          | (MQTT SSL/TLS Port 8883)
+-----------------------------------------▼-----------------------------------------+
|                      TẦNG 2: NETWORK / CONNECTIVITY (BROKER)                      |
|  - Cloud MQTT Broker: HiveMQ Cloud (s1.eu.hivemq.cloud)                           |
|  - Cổng bảo mật: Port 8883 (Mã hóa SSL/TLS đường truyền an toàn)                  |
|  - Wi-Fi Gateway: Wokwi-GUEST Virtual Network                                     |
+-----------------------------------------▲-----------------------------------------+
                                          | (Publish Telemetry & Subscribe Commands)
+-----------------------------------------▼-----------------------------------------+
|                          TẦNG 1: SENSING / PHYSICAL (DEVICE)                      |
|  - Node điều khiển: ESP32 DevKit V1 (Mô phỏng Wokwi)                             |
|  - Cảm biến đầu vào: MQ-2 Gas/Smoke Sensor (ADC34) + DHT22 Temp/Hum (GPIO15)      |
|  - Thiết bị đầu ra: Relay bật quạt hút (GPIO18) + Buzzer hú còi (GPIO19)          |
|  - Hệ thống chỉ thị 3 LED: Xanh (GPIO25) - Vàng (GPIO26) - Đỏ (GPIO27)             |
+-----------------------------------------------------------------------------------+
```

---

## 📡 QUY CHUẨN MẠNG & MQTT TOPICS

### 1. Thông tin kết nối HiveMQ Cloud:
- **Broker Host:** `956cadb3d6604926bcb8c34835ece2f7.s1.eu.hivemq.cloud`
- **Port:** `8883` (SSL/TLS mã hóa an toàn)
- **Username:** `iot_t4_1315`
- **Password:** `iot_t4_1315`

### 2. Danh mục Topics:
* **Uplink Telemetry (Định kỳ mỗi 5 giây):** `nhom12/baokhoi/telemetry`
  ```json
  {
    "smoke_ppm": 450,
    "temp": 32.5,
    "hum": 65.0,
    "state": "WARNING",
    "fan": 1,
    "buzzer": 0
  }
  ```

* **Uplink Alert (Bắn tức thời trong 1 giây khi có cháy):** `nhom12/baokhoi/alert`
  ```json
  {
    "alert": "FIRE_ALARM",
    "smoke_ppm": 780,
    "temp": 62.0,
    "hum": 55.0,
    "state": "DANGER",
    "msg": "PHAT HIEN NGUY HIEM HOA HOAN! Da tu dong bat coi & quat."
  }
  ```

* **Downlink Command (Lệnh điều khiển từ Middleware/Dashboard xuống):** `nhom12/baokhoi/cmd`
  * Bật quạt hút cưỡng bức: `{"cmd": "FAN_ON"}`
  * Tắt quạt hút: `{"cmd": "FAN_OFF"}`
  * Trả về chế độ tự động: `{"cmd": "AUTO"}`
  * Bật còi hú: `{"buzzer": 1}`
  * Tắt còi hú: `{"buzzer": 0}`

---

## 🚦 CÁC NGƯỠNG PHÂN CẤP CẢNH BÁO

| Cấp độ | Tên trạng thái | Điều kiện kích hoạt | Đèn LED | Trạng thái Quạt hút | Trạng thái Còi Buzzer | Cảnh báo Telegram |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Mức 1** | **SAFE** | Khói < 300 PPM và Nhiệt độ ≤ 55°C | 🟢 **LED Xanh** | TẮT (OFF) | TẮT (OFF) | Không |
| **Mức 2** | **WARNING** | 300 ≤ Khói ≤ 600 PPM | 🟡 **LED Vàng** | BẬT (ON) | TẮT (OFF) | Không |
| **Mức 3** | **DANGER** | Khói > 600 PPM hoặc Nhiệt độ > 55°C | 🔴 **LED Đỏ** | BẬT MAX (ON) | HÚ CÒI (1000Hz) | **Bắn tin khẩn cấp** |

---

## 🚀 HƯỚNG DẪN CHẠY DỰ ÁN

### 1. Khởi chạy Mô phỏng ESP32 (Wokwi):
1. Cài đặt extension **Wokwi Simulator** trong VS Code.
2. Mở thư mục `firmware_esp32`.
3. Bấm `F1` $\rightarrow$ Chọn `Wokwi: Start Simulator` (hoặc mở file `diagram.json`).
4. Quan sát Terminal: ESP32 kết nối Wi-Fi $\rightarrow$ kết nối HiveMQ SSL thành công $\rightarrow$ bắt đầu phát dữ liệu mỗi 5s.

### 2. Khởi chạy Middleware & Dashboard (Node-RED):
1. Khởi động Node-RED: gõ lệnh `node-red` trong terminal.
2. Truy cập: `http://localhost:1880`.
3. Import file `middleware_nodered/flows_template.json`.
4. Bấm **Deploy**.
5. Mở Dashboard giám sát: `http://localhost:1880/ui`.

---

## 📂 CẤU TRÚC THƯ MỤC REPOSITORY

```text
IoT_HeThongBaoKhoi_Nhom12/
├── README.md                          # Tài liệu hướng dẫn & kiến trúc tổng thể
├── .gitignore                         # Bỏ qua các file build PlatformIO rác
├── docs/                              # Bản vẽ bố trí layout, sơ đồ mạch Wokwi & minh chứng
│   ├── Ban_ve_Bo_tri_Layout_Thuc_te.jpg
│   ├── Sodo_Wokwi_3LED_Huy.png
│   ├── Layout_VatLy_ThucTe.png
│   └── MinhChung_MQTTX_Tuan4.png
├── firmware_esp32/                    # Mã nguồn C++ ESP32 Wokwi (Tăng Gia Huy)
│   ├── platformio.ini
│   ├── wokwi.toml
│   ├── diagram.json
│   └── src/
│       └── main.cpp
├── middleware_nodered/                # Flow Node-RED & Rules tự động hóa (Châu Phát Lộc)
│   ├── README.md
│   └── flows_template.json
└── application_dashboard/             # Giao diện Dashboard & Bot Telegram (Lục Xuân Thịnh)
    └── README.md
```

---
*Bản quyền thuộc về Nhóm 12 - Học phần An toàn và Bảo mật IoT (IT4735) - HUIT 2026.*
