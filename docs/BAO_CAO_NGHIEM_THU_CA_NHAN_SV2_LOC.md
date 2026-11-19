# BÁO CÁO NGHIỆM THU CÔNG VIỆC CÁ NHÂN (SV2 - NETWORK & MIDDLEWARE)
## HỆ THỐNG BÁO KHÓI CẢNH BÁO SỚM THÔNG MINH - NHÓM 12 (ĐỀ TÀI 04)
**Môn học:** Internet of Things (IT4735) - Trường Đại học Công Thương TP.HCM (HUIT)  
**Giảng viên hướng dẫn:** Thầy Võ Hoàng Hải  

---

### THÔNG TIN SINH VIÊN
* **Họ và tên:** Châu Phát Lộc
* **MSSV:** 2001230469
* **Vai trò trong nhóm:** SV2 – Kỹ sư Tầng 2 & 3: Network / Connectivity & Middleware Engine
* **Kho lưu trữ GitHub:** [IoT_HeThongBaoKhoi_Nhom12](https://github.com/tidocr0/IoT_HeThongBaoKhoi_Nhom12)
* **Khối lượng công việc tích lũy:** ≥ 60 giờ (Tuần 1 – Tuần 8)

---

### BẢNG ĐỐI CHIẾU TIÊU CHÍ RUBRIC & CHECKLIST DELIVERABLES CỦA SV2

| STT | Hạng mục Rubric | Yêu cầu chuẩn theo Syllabus | Sản phẩm bàn giao của SV2 (Evidence) | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **Kiến trúc Tầng 2 - Network / Broker** (25đ) | Thiết lập Cloud Broker kết nối mã hóa bảo mật SSL/TLS; phân định danh mục Topics rõ ràng; quản lý kết nối an toàn. | Máy chủ **HiveMQ Cloud SSL Port 8883** (`956cadb3d6604926bcb8c34835ece2f7.s1.eu.hivemq.cloud`), xác thực Username/Password, Client ID động tránh xung đột đa máy ([docs/MinhChung_MQTTX_Tuan4.png](MinhChung_MQTTX_Tuan4.png)). | **ĐẠT 100%** |
| 2 | **Chuẩn hóa Danh mục 3 Topic MQTT** (Checklist #5) | Danh sách topic, payload JSON mẫu và hướng truyền thông Uplink/Downlink rõ ràng. | Quy chuẩn 3 Topic chuẩn xác:<br>• **Uplink Telemetry (5s):** `nhom12/baokhoi/telemetry` (QoS 0)<br>• **Uplink Alert (< 1s):** `nhom12/baokhoi/alert` (QoS 1)<br>• **Downlink Command:** `nhom12/baokhoi/cmd` (QoS 1) | **ĐẠT 100%** |
| 3 | **Tầng 3 - Middleware Engine** (Checklist #4) | Middleware phải thực hiện xử lý logic, không chỉ forward dữ liệu thô; hợp nhất chạy chung luồng hệ thống. | Tab **Tầng 3: Middleware & Automation (Lộc)** tích hợp trực tiếp trong [application_dashboard/flows_dashboard_telegram.json](../application_dashboard/flows_dashboard_telegram.json) và bản export độc lập [middleware_nodered/flows_template.json](../middleware_nodered/flows_template.json). | **ĐẠT 100%** |
| 4 | **Edge-Trigger Automation & Anti-Override** (20đ) | Có tối thiểu 02 quy tắc tự động hóa + 01 kịch bản bất thường; điều khiển 2 chiều không xung đột. | Hàm `Rule Engine (Edge-Trigger 3 Ngưỡng)`:<br>• Chỉ bắn lệnh tự động khi chuyển ngưỡng (`SAFE ↔ WARNING ↔ DANGER`), **không bắn lặp `AUTO` mỗi 5s** làm ghi đè nút bấm `FAN_ON`/`FAN_OFF` thủ công.<br>• **Rule Cháy nổ:** Khói > 600 PPM hoặc Nhiệt > 55°C $\rightarrow$ Cưỡng bức `{"cmd": "FAN_ON"}`, `{"buzzer": 1}`.<br>• **Rule Tản khói & Phục hồi:** 300–600 PPM bật quạt `AUTO`; < 300 PPM trả về `AUTO` (giữ `manualOverride` nếu người dùng bật/tắt tay). | **ĐẠT 100%** |
| 5 | **Watchdog Timeout > 20s & CSV Event Logging** | Xử lý kịch bản mất kết nối bất thường (Tuần 7) + Lưu vết sự kiện thật (`log/event history` Tuần 5). | Watchdog tự động cảnh báo **`OFFLINE_TIMEOUT`** khi quá 20 giây mất Telemetry; Node ghi file thật **`logs/event_history.csv`** lưu thời gian VN, loại sự kiện, nguồn, PPM, nhiệt độ, độ ẩm & hành động. | **ĐẠT 100%** |

---

### HÌNH ẢNH & TÀI LIỆU MINH CHỨNG THỰC NGHIỆM

1. **Sơ đồ Kiến trúc 4 Tầng 2 Chiều (Uplink & Downlink):**  
   ![Sơ đồ Kiến trúc 4 Tầng](SoDo_KienTruc_4Tang_Nhom12.png)

2. **Minh chứng Flow Node-RED Tầng 3 kết nối HiveMQ SSL (`connected`):**  
   ![Minh chứng Node-RED Flow](MinhChung_NodeRED_Flow_Full.png)

3. **Minh chứng Kết nối MQTT Broker HiveMQ SSL Port 8883 qua MQTTX:**  
   ![Minh chứng MQTTX](MinhChung_MQTTX_Tuan4.png)

---

### KẾT LUẬN TIẾN ĐỘ CỦA SV2 (CHÂU PHÁT LỘC):
* Toàn bộ phần việc Tầng 2 & Tầng 3 trong Milestone M3 & M4 (Edge-Trigger, CSV Log, Watchdog Timeout > 20s) đã **HOÀN THÀNH & KIỂM THỬ THỰC TẾ 100% ĐẠT CHUẨN RUBRIC**.
* Đã sẵn sàng thuyết trình và trả lời vấn đáp kỹ thuật cả 4 tầng cùng Nhóm 12 ([HUONG_DAN_VAN_DAP_QA_4_TANG.md](HUONG_DAN_VAN_DAP_QA_4_TANG.md)).
