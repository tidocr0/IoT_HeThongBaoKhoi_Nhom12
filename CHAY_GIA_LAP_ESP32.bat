@echo off
chcp 65001 > nul
title GIA LAP THIET BI ESP32 - HE THONG BAO KHOI NHOM 12
cls
echo =====================================================================
echo    MÔ PHỎNG THIẾT BỊ PHẦN CỨNG ESP32 (ĐỀ TÀI 04 - NHÓM 12)
echo    Kết nối HiveMQ Cloud SSL 8883 - Giám sát hai chiều E2E
echo =====================================================================
echo.
python "%~dp0esp32_simulator.py"
pause
