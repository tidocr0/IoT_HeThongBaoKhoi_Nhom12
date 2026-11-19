@echo off
chcp 65001 > nul
cd /d "%~dp0"
title GIA LAP THIET BI ESP32 - HE THONG BAO KHOI NHOM 12
cls
echo =====================================================================
echo    MÔ PHỎNG THIẾT BỊ PHẦN CỨNG ESP32 (ĐỀ TÀI 04 - NHÓM 12)
echo    Kết nối HiveMQ Cloud SSL 8883 - Hỗ trợ chạy đa máy
echo =====================================================================
echo.

set "PY_CMD="
where python >nul 2>nul && set "PY_CMD=python"
if not defined PY_CMD (
    where py >nul 2>nul && set "PY_CMD=py -3"
)
if not defined PY_CMD (
    echo [LOI] May nay chua cai Python 3! Vui long cai Python tai https://www.python.org/
    pause
    exit /b 1
)

%PY_CMD% -c "import paho.mqtt.client" >nul 2>nul
if errorlevel 1 (
    echo [*] Dang tu dong cai dat thu vien paho-mqtt cho may moi...
    %PY_CMD% -m pip install paho-mqtt
    if errorlevel 1 (
        echo [LOI] Khong the cai dat paho-mqtt. Vui long kiem tra ket noi mang.
        pause
        exit /b 1
    )
)

%PY_CMD% "%~dp0esp32_simulator.py"
pause
