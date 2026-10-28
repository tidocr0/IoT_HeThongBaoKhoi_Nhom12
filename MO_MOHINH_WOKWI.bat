@echo off
chcp 65001 > nul
title MO MO HINH WOKWI ESP32 - NHOM 12
echo =====================================================================
echo    ĐANG MỞ MÔ HÌNH MẠCH ĐIỆN WOKWI TRONG VISUAL STUDIO CODE...
echo =====================================================================
echo.
echo Khi màn hình VS Code hiện lên:
echo 1. Nhìn vào file diagram.json vừa mở.
echo 2. Bấm nút Play (tam giác xanh lá) ở thanh Wokwi để chạy mô phỏng!
echo.
code "%~dp0firmware_esp32" "%~dp0firmware_esp32\diagram.json"
