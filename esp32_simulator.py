import sys
import time
import json
import ssl
import random
import threading
import paho.mqtt.client as mqtt

# UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BROKER_HOST = "956cadb3d6604926bcb8c34835ece2f7.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
BROKER_USER = "iot_t4_1315"
BROKER_PASS = "iot_t4_1315"

TOPIC_TELEMETRY = "nhom12/baokhoi/telemetry"
TOPIC_ALERT = "nhom12/baokhoi/alert"
TOPIC_CMD = "nhom12/baokhoi/cmd"

# Initial state (khớp 100% logic FSM của firmware_esp32/src/main.cpp)
manual_fan_override = False
manual_buzzer_override = False
fan_state = 0          # 0: OFF, 1: ON
buzzer_state = 0       # 0: OFF, 1: ON
smoke_ppm = 150.0
temp = 28.5
hum = 65.0
state_str = "SAFE"     # SAFE, WARNING, DANGER
prev_state_str = "SAFE"
paused_telemetry = False

lock = threading.Lock()
running = True


def compute_fsm_state(ppm_val, temp_val):
    if ppm_val > 600.0 or temp_val > 55.0:
        return "DANGER"
    if ppm_val >= 300.0:
        return "WARNING"
    return "SAFE"


def update_state_logic():
    global state_str, fan_state, buzzer_state
    with lock:
        state_str = compute_fsm_state(smoke_ppm, temp)
        if not manual_fan_override:
            fan_state = 0 if state_str == "SAFE" else 1
        if not manual_buzzer_override:
            buzzer_state = 1 if state_str == "DANGER" else 0


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("\n" + "=" * 68)
        print("  [ESP32 SIM] KẾT NỐI HIVEMQ CLOUD SSL 8883 THÀNH CÔNG! (200 OK)")
        print("=" * 68)
        client.subscribe(TOPIC_CMD)
        print(f"[*] Đã subscribe topic điều khiển: {TOPIC_CMD}")
        print("[*] Đang phát telemetry định kỳ mỗi 5 giây (khớp firmware ESP32)...")
        print("-" * 68)
        print("PHÍM TẮT ĐIỀU KHIỂN KỊCH BẢN (NHẤN SỐ RỒI ENTER):")
        print("  [1] -> SAFE         (Khói 120 PPM, Nhiệt 28.0°C | LED Xanh | Quạt TẮT)")
        print("  [2] -> WARNING      (Khói 450 PPM, Nhiệt 36.5°C | LED Vàng | Quạt TỰ BẬT)")
        print("  [3] -> DANGER KHÓI  (Khói 780 PPM, Nhiệt 62.0°C | LED Đỏ + Còi + Alert)")
        print("  [4] -> DANGER NHIỆT (Khói 220 PPM, Nhiệt 59.0°C | Cháy không khói > 55°C)")
        print("  [p] -> Tạm ngưng/Tiếp tục gửi Telemetry (Test kịch bản Timeout > 20s)")
        print("  [q] -> Thoát giả lập")
        print("=" * 68 + "\n")
    else:
        print(f"[!] Lỗi kết nối HiveMQ Broker! Mã lỗi: {rc}")


def on_message(client, userdata, msg):
    global fan_state, buzzer_state, manual_fan_override, manual_buzzer_override
    try:
        payload_str = msg.payload.decode("utf-8")
        doc = json.loads(payload_str)
        print(f"\n📩 [DOWNLINK TỪ BROKER] Topic [{msg.topic}]: {payload_str}")

        with lock:
            if "cmd" in doc and doc["cmd"] is not None:
                cmd = str(doc["cmd"])
                if cmd == "FAN_ON":
                    manual_fan_override = True
                    fan_state = 1
                    print("   >>> [RELAY] QUẠT HÚT BẬT CƯỠNG BỨC (MANUAL FAN_ON)")
                elif cmd == "FAN_OFF":
                    manual_fan_override = True
                    fan_state = 0
                    print("   >>> [RELAY] QUẠT HÚT TẮT CƯỠNG BỨC (MANUAL FAN_OFF)")
                elif cmd == "AUTO":
                    manual_fan_override = False
                    manual_buzzer_override = False
                    print("   >>> [MODE] CHUYỂN VỀ CHẾ ĐỘ TỰ ĐỘNG (AUTO)")

            if "buzzer" in doc and doc["buzzer"] is not None:
                bz = int(doc["buzzer"])
                manual_buzzer_override = True
                buzzer_state = 1 if bz == 1 else 0
                print(f"   >>> [BUZZER] CÒI BÁO ĐỘNG: {'BẬT (1000Hz)' if buzzer_state else 'TẮT'}")

        update_state_logic()
    except Exception as e:
        print(f"[!] Lỗi phân tích lệnh JSON: {e}")


client_id = f"ESP32_Sim_Nhom12_{random.randint(1000, 9999)}"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
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


def send_alert_now():
    with lock:
        payload = {
            "alert": "FIRE_ALARM",
            "smoke_ppm": round(smoke_ppm),
            "temp": round(temp, 1),
            "hum": round(hum, 1),
            "state": "DANGER",
            "msg": "PHAT HIEN NGUY HIEM HOA HOAN! Da tu dong bat coi & quat.",
        }
    json_data = json.dumps(payload, ensure_ascii=False)
    client.publish(TOPIC_ALERT, json_data, qos=1)
    print(f"🚨 [PUBLISH ALERT TỨC THÌ] {json_data}")


def telemetry_loop():
    global smoke_ppm, temp, hum, prev_state_str
    while running:
        update_state_logic()
        fire_edge = False
        with lock:
            if not paused_telemetry:
                if state_str == "SAFE" and temp <= 55.0:
                    smoke_ppm = max(80.0, min(220.0, smoke_ppm + random.uniform(-4, 4)))
                    temp = max(26.0, min(31.0, temp + random.uniform(-0.2, 0.2)))
                    hum = max(60.0, min(70.0, hum + random.uniform(-0.4, 0.4)))
                    update_state_logic_locked()

                if prev_state_str != "DANGER" and state_str == "DANGER":
                    fire_edge = True
                prev_state_str = state_str

                payload = {
                    "smoke_ppm": int(round(smoke_ppm)),
                    "temp": round(temp, 1),
                    "hum": round(hum, 1),
                    "state": state_str,
                    "fan": fan_state,
                    "buzzer": buzzer_state,
                }
            else:
                payload = None

        if payload is not None:
            if fire_edge:
                send_alert_now()
            json_data = json.dumps(payload, ensure_ascii=False)
            client.publish(TOPIC_TELEMETRY, json_data, qos=0)
            mode_fan = "Manual" if manual_fan_override else "Auto"
            print(
                f"📊 [TELEMETRY 5s] PPM: {payload['smoke_ppm']} | Temp: {payload['temp']}°C | "
                f"Hum: {payload['hum']}% | State: {payload['state']} | Fan: {payload['fan']} ({mode_fan}) | Buzzer: {payload['buzzer']}"
            )
        time.sleep(5)


def update_state_logic_locked():
    global state_str, fan_state, buzzer_state
    state_str = compute_fsm_state(smoke_ppm, temp)
    if not manual_fan_override:
        fan_state = 0 if state_str == "SAFE" else 1
    if not manual_buzzer_override:
        buzzer_state = 1 if state_str == "DANGER" else 0


t_telemetry = threading.Thread(target=telemetry_loop, daemon=True)
t_telemetry.start()

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
                manual_fan_override = False
                manual_buzzer_override = False
                paused_telemetry = False
                update_state_logic_locked()
                prev_state_str = state_str
            print("\n>>> [1] CHUYỂN MỨC SAFE (120 PPM, 28.0°C) ✅\n")
        elif cmd == "2":
            with lock:
                smoke_ppm = 450.0
                temp = 36.5
                hum = 55.0
                manual_fan_override = False
                manual_buzzer_override = False
                paused_telemetry = False
                update_state_logic_locked()
                prev_state_str = state_str
            print("\n>>> [2] CHUYỂN MỨC WARNING (450 PPM, 36.5°C) - QUẠT TỰ BẬT ⚠️\n")
        elif cmd == "3":
            with lock:
                smoke_ppm = 780.0
                temp = 62.0
                hum = 42.0
                manual_fan_override = False
                manual_buzzer_override = False
                paused_telemetry = False
                update_state_logic_locked()
                prev_state_str = "DANGER"
            send_alert_now()
            print("\n>>> [3] BÁO ĐỘNG CHÁY KHẨN CẤP (780 PPM, 62.0°C) 🚨🔥\n")
        elif cmd == "4":
            with lock:
                smoke_ppm = 220.0
                temp = 59.0
                hum = 40.0
                manual_fan_override = False
                manual_buzzer_override = False
                paused_telemetry = False
                update_state_logic_locked()
                prev_state_str = "DANGER"
            send_alert_now()
            print("\n>>> [4] BÁO ĐỘNG NHIỆT ĐỘ CAO (220 PPM, 59.0°C > 55°C) 🌡️🚨\n")
        elif cmd == "p":
            with lock:
                paused_telemetry = not paused_telemetry
                state_pause = paused_telemetry
            if state_pause:
                print("\n>>> [p] ĐÃ TẠM NGƯNG TELEMETRY (Đợi > 20s để test Offline Timeout trên Dashboard) ⏸️\n")
            else:
                print("\n>>> [p] ĐÃ TIẾP TỤC GỬI TELEMETRY ▶️\n")
        elif cmd == "q":
            print("\nĐang dừng giả lập...")
            running = False
            break
except KeyboardInterrupt:
    running = False

client.loop_stop()
client.disconnect()
print("Đã thoát giả lập ESP32.")
