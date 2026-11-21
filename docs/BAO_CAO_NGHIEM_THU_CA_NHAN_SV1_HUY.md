# BÁO CÁO NGHIỆM THU CÔNG VIỆC CÁ NHÂN (SV1 - SENSING / EMBEDDED)
## HỆ THỐNG BÁO KHÓI CẢNH BÁO SỚM THÔNG MINH - NHÓM 12 (ĐỀ TÀI 04)
**Môn học:** Internet of Things (IT4735) - Trường Đại học Công Thương TP.HCM (HUIT)  
**Giảng viên hướng dẫn:** Thầy Võ Hoàng Hải  

---

### THÔNG TIN SINH VIÊN
* **Họ và tên:** Tăng Gia Huy
* **MSSV:** 2001230313
* **Vai trò trong nhóm:** SV1 – Kỹ sư Tầng 1: Sensing / Embedded
* **Kho lưu trữ GitHub:** [IoT_HeThongBaoKhoi_Nhom12](https://github.com/tidocr0/IoT_HeThongBaoKhoi_Nhom12)
* **Link Mô phỏng Wokwi Công khai (Checklist #7):** [https://wokwi.com/projects/480660154780749825](https://wokwi.com/projects/480660154780749825)
* **Khối lượng công việc tích lũy:** ≥ 60 giờ (Tuần 1 – Tuần 8, Milestone M1 → M4)

---

### BẢNG ĐỐI CHIẾU TIÊU CHÍ RUBRIC & CHECKLIST DELIVERABLES CỦA SV1

| STT | Hạng mục Rubric | Yêu cầu chuẩn theo Syllabus | Sản phẩm bàn giao của SV1 (Evidence) | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **Simulation & Embedded** (20đ) | Mô phỏng Wokwi đầy đủ cảm biến & cơ cấu chấp hành; mạch điện nối đúng nguyên lý; firmware thể hiện đúng bài toán. | Project Wokwi công khai ([https://wokwi.com/projects/480660154780749825](https://wokwi.com/projects/480660154780749825) & [firmware_esp32/diagram.json](../firmware_esp32/diagram.json)) với ESP32, MQ-2 (ADC34), DHT22 (GPIO15), Relay quạt (GPIO18), Còi Buzzer (GPIO19) và hệ thống 3 LED chỉ thị (Xanh GPIO25, Vàng GPIO26, Đỏ GPIO27). | **ĐẠT 100%** |
| 2 | **Lọc nhiễu tín hiệu & Chống lỗi NaN (Tuần 7)** | Không dùng giá trị đo thô; phải có giải thuật xử lý tín hiệu và xử lý ngoại lệ cảm biến. | Thuật toán **Lọc trung bình trượt (Moving Average Filter)** với `SMOKE_SAMPLES = 10` mẫu trong hàm `docVaLocKhoi()` và cơ chế kiểm tra `isnan(t)` cho DHT22, loại bỏ hoàn toàn các gai nhiễu điện áp analog trước khi ánh xạ sang thang đo $0 - 1000\text{ PPM}$. | **ĐẠT 100%** |
| 3 | **Máy trạng thái FSM & Đa cảm biến** (20đ) | Phân cấp kịch bản rõ ràng (SAFE, WARNING, DANGER); xử lý logic tự động kết hợp nhiều cảm biến. | Máy trạng thái FSM 3 mức chuẩn xác:<br>• **SAFE (< 300 PPM, temp $\le 55^\circ\text{C}$):** Sáng LED Xanh, Quạt tắt, Còi tắt.<br>• **WARNING (300 - 600 PPM):** Sáng LED Vàng, Relay tự kích Quạt hút khói.<br>• **DANGER (> 600 PPM hoặc temp > $55^\circ\text{C}$):** Nhấp nháy LED Đỏ khẩn cấp, Quạt chạy tối đa, Còi hú $1000\text{Hz}$ liên tục. | **ĐẠT 100%** |
| 4 | **Bố trí không gian thực tế** (Layout) | Sơ đồ lắp đặt vật lý thực tế ngoài đời để chuẩn bị cho giai đoạn triển khai thực tế. | Bản vẽ phối cảnh 3D Isometric tiếng Việt ([docs/Ban_ve_Bo_tri_Layout_Thuc_te.jpg](Ban_ve_Bo_tri_Layout_Thuc_te.jpg)) định vị chuẩn xác: Cảm biến MQ-2 trần bếp, DHT22 tường 1.5m, Quạt hút cửa sổ, Còi cửa thoát hiểm, Tủ ESP32. | **ĐẠT 100%** |
| 5 | **Điều khiển 2 chiều Downlink & Manual Override (Tuần 8)** (10đ) | Phát hiện chuyển trạng thái khẩn cấp không chờ chu kỳ; nhận lệnh Downlink điều khiển từ xa không bị ghi đè. | Cơ chế phát hiện cạnh chuyển trạng thái (`previousState != DANGER && currentState == DANGER`) bắn cảnh báo khẩn cấp `<1s`; hàm `callback` xử lý lệnh JSON `FAN_ON`, `FAN_OFF`, `BUZZER_ON`, `BUZZER_OFF`, `AUTO` và giữ cờ `manualFanOverride` qua các chu kỳ Uplink 5s. | **ĐẠT 100%** |

---

### HÌNH ẢNH MINH CHỨNG THỰC NGHIỆM ĐÃ KIỂM THỬ THÀNH CÔNG

1. **Minh chứng Thực nghiệm Wokwi nhận lệnh Downlink Manual Override (`Quat: 0 (Manual) | Coi: 1 (Manual)` ở 833 PPM - Tuần 7 & 8):**  
   ![Wokwi Downlink Manual Override](MinhChung_Wokwi_Downlink_Manual_SV1.png)

2. **Minh chứng Điều khiển BẬT Quạt Thủ Công (`MANUAL_FAN_ON`) đồng bộ từ Dashboard xuống ESP32:**  
   ![Dashboard Manual Fan ON](MinhChung_Downlink_Manual_FanOn_SV1.png)

3. **Minh chứng Điều khiển TẮT Quạt Thủ Công (`MANUAL_FAN_OFF`) giữ nguyên Override không bị chu kỳ 5s ghi đè:**  
   ![Dashboard Manual Fan OFF](MinhChung_Downlink_Manual_FanOff_SV1.png)

4. **Sơ đồ mạch mô phỏng Wokwi có cụm 3 LED chỉ thị (Tăng Gia Huy):**  
   ![Sơ đồ mạch Wokwi](Sodo_Wokwi_3LED_Huy.png)

5. **Bản vẽ thiết kế Bố trí Thiết bị Thực tế trong Phòng Bếp (Physical Deployment Layout):**  
   ![Bản vẽ Layout Thực tế](Ban_ve_Bo_tri_Layout_Thuc_te.jpg)

6. **Mã nguồn Firmware ESP32 được cấu trúc Module hóa sạch sẽ:**  
   Toàn bộ mã nguồn C++ do SV1 phụ trách tại thư mục [firmware_esp32/src/main.cpp](../firmware_esp32/src/main.cpp) được chia thành các hàm chức năng tường minh:
   * `docVaLocKhoi()`: Đọc cảm biến MQ-2 & lọc trung bình trượt 10 mẫu (`SMOKE_SAMPLES = 10`).
   * `capNhatDenLED(state)`: Cập nhật 3 đèn LED Xanh - Vàng - Đỏ (nhấp nháy khẩn cấp khi `DANGER`) theo trạng thái FSM.
   * `dieuKhienThietBi(state)`: Tự động đóng ngắt Relay Quạt và điều khiển tần số Còi Buzzer, tôn trọng cờ `manualFanOverride` & `manualBuzzerOverride`.

---

### KẾT LUẬN TIẾN ĐỘ CỦA SV1 (TĂNG GIA HUY):
* Toàn bộ phần việc cá nhân của SV1 từ Milestone M1 đến Milestone M4 (Tuần 1 – Tuần 8) đã **HOÀN THÀNH & KIỂM THỬ THỰC TẾ 100% ĐẠT CHUẨN RUBRIC**.
* Mã nguồn đã được biên dịch thành công với PlatformIO, chạy ổn định trên Wokwi Public và đồng bộ 2 chiều Uplink/Downlink với hệ thống nhóm ([BAO_CAO_KIEM_THU_E2E_TUAN_7_8.md](BAO_CAO_KIEM_THU_E2E_TUAN_7_8.md)).
