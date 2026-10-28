import sys
import time
import json
import ssl
import threading
import paho.mqtt.client as mqtt

# UTF-8 console output
sys.stdout.reconfigure(encoding='utf-8')

BROKER_HOST = "956cadb3d6604926bcb8c34835ece2f7.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
BROKER_USER = "iot_t4_1315"
BROKER_PASS = "iot_t4_1315"

TOPIC_TELEMETRY = "nhom12/baokhoi/telemetry"
TOPIC_ALERT = "nhom12/baokhoi/alert"
TOPIC_CMD = "nhom12/baokhoi/cmd"

# Initial state
current_mode = "AUTO"  # AUTO or MANUAL
fan_state = 0          # 0: OFF, 1: ON
buzzer_state = 0       # 0: OFF, 1: ON
smoke_ppm = 150.0
temp = 28.5
hum = 65.0
state_str = "SAFE"     # SAFE, WARNING, DANGER

lock = threading.Lock()
running = True

def update_state_logic():
    global smoke_ppm, temp, hum, state_str, fan_state, buzzer_state, current_mode
    with lock:
        if current_mode == "AUTO":
            if smoke_ppm > 600.0 or temp > 55.0:
                state_str = "DANGER"
                fan_state = 1
                buzzer_state = 1
            elif smoke_ppm > 300.0:
                state_str = "WARNING"
                fan_state = 0
                buzzer_state = 0
            else:
                state_str = "SAFE"
                fan_state = 0
                buzzer_state = 0

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("\n" + "="*65)
        print("  [ESP32] KẾT NỐI HIVEMQ CLOUD SSL 8883 THÀNH CÔNG! (200 OK)")
        print("="*65)
        client.subscribe(TOPIC_CMD)
        print(f"[*] Đã đăng ký lắng nghe lệnh điều khiển tại topic: {TOPIC_CMD}")
        print("[*] Đang gửi dữ liệu cảm biến định kỳ mỗi 3 giây lên Dashboard...")
        print("-" * 65)
        print("PHÍM TẮT GIẢ LẬP TRÊN BÀN PHÍM:")
        print("  [1] -> Mức AN TOÀN   (Khói 150 PPM, Nhiệt 28°C, Quạt TẮT, LED Xanh)")
        print("  [2] -> Mức CHÚ Ý     (Khói 420 PPM, Nhiệt 36°C, Quạt TẮT, LED Vàng)")
        print("  [3] -> BÁO CHÁY NỔ   (Khói 780 PPM, Nhiệt 60°C, Quạt BẬT, Còi HÚ, Bắn Telegram!)")
        print("  [q] -> Thoát giả lập")
        print("="*65 + "\n")
    else:
        print(f"[!] Lỗi kết nối HiveMQ Broker! Mã lỗi: {rc}")

def on_message(client, userdata, msg):
    global fan_state, buzzer_state, current_mode
    try:
        payload_str = msg.payload.decode('utf-8')
        doc = json.loads(payload_str)
        print(f"\n📩 [DOWNLINK TỪ WEB DASHBOARD] Nhận gói tin: {payload_str}")
        
        with lock:
            if "cmd" in doc:
                cmd = doc["cmd"]
                if cmd == "FAN_ON":
                    current_mode = "MANUAL"
                    fan_state = 1
                    print("   >>> [RELAY KÍCH HOẠT] Quạt hút ĐÃ BẬT CƯỠNG BỨC (MANUAL ON) 🌀")
                elif cmd == "FAN_OFF":
                    current_mode = "MANUAL"
                    fan_state = 0
                    print("   >>> [RELAY NGẮT] Quạt hút ĐÃ TẮT CƯỠNG BỨC (MANUAL OFF) ⏹️")
                elif cmd == "AUTO":
                    current_mode = "AUTO"
                    print("   >>> [CHUYỂN CHẾ ĐỘ] Đã quay về TỰ ĐỘNG THEO CẢM BIẾN (AUTO) 🔄")
        update_state_logic()
    except Exception as e:
        print(f"[!] Lỗi phân tích lệnh JSON: {e}")

# Setup MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ESP32_Safety_Station_Nhom12")
client.username_pw_set(BROKER_USER, BROKER_PASS)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
except Exception as e:
    print(f"[!] Không thể kết nối HiveMQ: {e}")
    sys.exit(1)

def telemetry_loop():
    global running, smoke_ppm, temp, hum, state_str, fan_state, buzzer_state, current_mode
    while running:
        update_state_logic()
        with lock:
            payload = {
                "smoke_ppm": round(smoke_ppm, 1),
                "temp": round(temp, 1),
                "hum": round(hum, 1),
                "state": state_str,
                "fan": fan_state,
                "fan_mode": current_mode,
                "buzzer": buzzer_state
            }
            # Add small realistic fluctuation
            if state_str == "SAFE":
                import random
                smoke_ppm = max(80.0, min(220.0, smoke_ppm + random.uniform(-5, 5)))
                temp = max(26.0, min(31.0, temp + random.uniform(-0.2, 0.2)))
                hum = max(60.0, min(70.0, hum + random.uniform(-0.5, 0.5)))
        
        json_data = json.dumps(payload, ensure_ascii=False)
        client.publish(TOPIC_TELEMETRY, json_data, qos=0)
        
        # If danger, also publish to alert topic
        if payload["state"] == "DANGER":
            client.publish(TOPIC_ALERT, json_data, qos=1)
            print(f"🔥 [PUBLISH ALERT] Khói: {payload['smoke_ppm']} PPM | Nhiệt: {payload['temp']}°C | Quạt: {payload['fan']} | Còi: {payload['buzzer']}")
        else:
            print(f"📊 [TELEMETRY] Khói: {payload['smoke_ppm']} PPM ({payload['state']}) | Nhiệt: {payload['temp']}°C | Ẩm: {payload['hum']}% | Quạt: {payload['fan']}")
        
        time.sleep(3)

t_telemetry = threading.Thread(target=telemetry_loop, daemon=True)
t_telemetry.start()

# Main input loop
try:
    while running:
        line = sys.stdin.readline()
        if not line:
            time.sleep(0.5)
            continue
        cmd = line.strip().lower()
        if cmd == "1":
            with lock:
                smoke_ppm = 120.0
                temp = 28.0
                hum = 65.0
                current_mode = "AUTO"
            print("\n>>> ĐÃ CHUYỂN SANG: [1] MỨC AN TOÀN (< 300 PPM) ✅\n")
        elif cmd == "2":
            with lock:
                smoke_ppm = 450.0
                temp = 36.5
                hum = 55.0
                current_mode = "AUTO"
            print("\n>>> ĐÃ CHUYỂN SANG: [2] MỨC CẢNH BÁO CHÚ Ý (300-600 PPM) ⚠️\n")
        elif cmd == "3":
            with lock:
                smoke_ppm = 780.0
                temp = 62.0
                hum = 42.0
                current_mode = "AUTO"
            print("\n>>> ĐÃ CHUYỂN SANG: [3] BÁO ĐỘNG HỎA HOẠN (> 600 PPM)! 🚨🔥\n")
        elif cmd == "q":
            print("\nĐang dừng giả lập...")
            running = False
            break
except KeyboardInterrupt:
    running = False

client.loop_stop()
client.disconnect()
print("Đã thoát giả lập ESP32.")
