# BÁO CÁO NGHIỆM THU CÔNG VIỆC CÁ NHÂN (SV2 - NETWORK & MIDDLEWARE)
## HỆ THỐNG BÁO KHÓI CẢNH BÁO SỚM THÔNG MINH - NHÓM 12 (ĐỀ TÀI 04)
**Môn học:** Internet of Things (IT4735) - Trường Đại học Công Thương TP.HCM (HUIT)  
**Giảng viên hướng dẫn:** Thầy Võ Hoàng Hải  
**Giai đoạn:** Nghiệm thu Milestone M4 (Tuần 7 & Tuần 8)  

---

### THÔNG TIN SINH VIÊN
* **Họ và tên:** Châu Phát Lộc
* **MSSV:** 2001230469
* **Vai trò trong nhóm:** SV2 – Kỹ sư Tầng 2 & 3: Network / Connectivity & Middleware Engine
* **Kho lưu trữ GitHub:** [IoT_HeThongBaoKhoi_Nhom12](https://github.com/tidocr0/IoT_HeThongBaoKhoi_Nhom12)
* **Khối lượng công việc tích lũy:** ≥ 80 giờ (Tuần 1 – Tuần 8)

---

### BẢNG ĐỐI CHIẾU TIÊU CHÍ RUBRIC & CHECKLIST DELIVERABLES CỦA SV2 (TUẦN 7 & 8)

| STT | Hạng mục Rubric | Yêu cầu chuẩn theo Syllabus | Sản phẩm bàn giao của SV2 (Evidence) | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **Kiến trúc Tầng 2 - MQTT TLS Broker** | Máy chủ Cloud Broker bảo mật mã hóa SSL/TLS Port 8883; phân định 3 Topic Uplink/Downlink rõ ràng. | Máy chủ **HiveMQ Cloud SSL Port 8883** (`956cadb3d6604926bcb8c34835ece2f7.s1.eu.hivemq.cloud`), xác thực bằng tài khoản `iot_t4_1315`, vận hành ổn định qua MQTTX ([docs/MinhChung_MQTTX_Tuan4.png](MinhChung_MQTTX_Tuan4.png)). | **ĐẠT 100%** |
| 2 | **Chuẩn hóa Danh mục 3 Topic MQTT** | Phân cấp Topic rõ ràng, hỗ trợ cả giám sát định kỳ, cảnh báo tức thời và điều khiển 2 chiều. | • **Uplink Telemetry (5s):** `nhom12/baokhoi/telemetry`<br>• **Uplink Alert (< 1s, QoS 1):** `nhom12/baokhoi/alert`<br>• **Downlink Command (QoS 1):** `nhom12/baokhoi/cmd` | **ĐẠT 100%** |
| 3 | **Tình huống lỗi #1: Watchdog Timeout (20s)** | Tự động phát hiện khi thiết bị ngắt kết nối quá 20s và phát cảnh báo sự cố. | Hàm `Kiểm Tra Dữ Liệu & Watchdog Timeout (20s)` trong Node-RED: Đếm đúng 20s không có gói tin telemetry $\rightarrow$ Chuyển Dashboard sang `🔴 MẤT KẾT NỐI (OFFLINE TIMEOUT > 20s)`, bắn tin Telegram và ghi mã `OFFLINE_TIMEOUT` vào CSV. | **ĐẠT 100%** |
| 4 | **Tình huống lỗi #2: Bộ lọc Dữ liệu rác** | Loại bỏ các gói tin rác hoặc cảm biến lỗi không làm sập luồng middleware. | Kiểm tra điều kiện `typeof msg.payload.smoke_ppm !== "number"` hoặc `isNaN()` $\rightarrow$ Hủy gói tin rác, ghi nhật ký cảnh báo và bảo vệ luồng Node-RED vận hành liên tục không gián đoạn. | **ĐẠT 100%** |
| 5 | **Ghi nhận Lịch sử Sự kiện (Audit Log CSV)** | Lưu vết toàn bộ hoạt động của hệ thống phục vụ kiểm toán và tra cứu sự cố. | Luồng ghi log tự động ghi nhận vào tệp [logs/event_history.csv](../logs/event_history.csv) đủ 7 mã sự kiện chuẩn: `SYSTEM_ONLINE_SAFE`, `WARNING_HIGH_SMOKE`, `FIRE_ALARM_URGENT`, `MANUAL_FAN_ON`, `AUTH_DENIED_VIEWER`, `SET_AUTO_MODE`, `OFFLINE_TIMEOUT`. | **ĐẠT 100%** |
| 6 | **Minh chứng Git cá nhân trên GitHub** | Có lịch sử commit rõ ràng mang tên cá nhân trên kho mã nguồn nhóm. | Thực hiện commit và push trực tiếp lên nhánh `main` với tài khoản mang tên Châu Phát Lộc, ghi nhận các đóng góp về Middleware và kiểm thử đo độ trễ. | **ĐẠT 100%** |

---

### HÌNH ẢNH & TÀI LIỆU MINH CHỨNG THỰC NGHIỆM

1. **Minh chứng Kết nối MQTT Broker HiveMQ SSL Port 8883 qua MQTTX:**  
   ![Minh chứng MQTTX](MinhChung_MQTTX_Tuan4.png)

2. **File Flow Node-RED Middleware hoàn chỉnh cho Milestone M4:**  
   Toàn bộ mã nguồn luồng xử lý do SV2 phụ trách tại thư mục [application_dashboard/flows_dashboard_telegram.json](../application_dashboard/flows_dashboard_telegram.json) với 37 nodes xử lý bao gồm Watchdog Timeout, Bộ lọc rác, RBAC Gate và CSV Logger.

3. **Tệp dữ liệu Audit Log CSV:**  
   Đã được tạo lập và lưu trữ tại [logs/event_history.csv](../logs/event_history.csv) chứa đầy đủ lịch sử kiểm thử chéo với các mốc thời gian chi tiết.

---

### KẾT LUẬN TIẾN ĐỘ CỦA SV2 (CHÂU PHÁT LỘC):
* Toàn bộ phần việc cá nhân của SV2 trong Milestone M4 (Tuần 7 - 8) đã **HOÀN THÀNH 100% ĐẠT CHUẨN RUBRIC**.
* Đảm bảo thông suốt đường truyền mã hóa TLS 8883 giữa Tầng 1 (ESP32 Wokwi của SV1 Huy) và Tầng 4 (Dashboard & Telegram Bot của SV3 Thịnh).
* Đã sẵn sàng thuyết trình và trả lời vấn đáp kỹ thuật Tầng 2 & 3 với Giảng viên Võ Hoàng Hải theo tài liệu [HUONG_DAN_VAN_DAP_QA_4_TANG.md](HUONG_DAN_VAN_DAP_QA_4_TANG.md).
