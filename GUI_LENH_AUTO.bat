@echo off
chcp 65001 > nul
title GUI LENH CHUYEN CHE DO TU DONG (AUTO MODE)
cls
echo =====================================================================
echo    GUI LENH DOWNLINK: CHUYEN VE TU DONG (AUTO)
echo    Ket noi HiveMQ Cloud SSL 8883 -> ESP32 Wokwi
echo =====================================================================
echo.
echo [*] Dang gui lenh {"cmd":"AUTO"} xuong topic nhom12/baokhoi/cmd...

python -c "import paho.mqtt.client as mqtt, ssl, json; client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='Downlink_Tester_Auto'); client.username_pw_set('iot_t4_1315', 'iot_t4_1315'); client.tls_set(cert_reqs=ssl.CERT_NONE); client.tls_insecure_set(True); client.connect('956cadb3d6604926bcb8c34835ece2f7.s1.eu.hivemq.cloud', 8883); client.publish('nhom12/baokhoi/cmd', json.dumps({'cmd': 'AUTO'}), qos=1); client.disconnect(); print('>>> [THANH CONG] Da ban lenh AUTO xuong ESP32!')"

echo.
echo =====================================================================
echo [*] XONG! Huy hay nhin vao cua so Serial Monitor tren Wokwi:
echo     Se xuat hien dong: >>> [CMD THUC THI] CHUYEN VE CHE DO TU DONG (AUTO)
echo     va trang thai: Quat: ... (Auto)
echo =====================================================================
echo.
pause
