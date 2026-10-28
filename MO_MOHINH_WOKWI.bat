@echo off
chcp 65001 > nul
title MO DU AN TRONG ANTIGRAVITY IDE - NHOM 12
echo =====================================================================
echo    ĐANG MỞ DỰ ÁN VÀ CODE TRONG ANTIGRAVITY IDE...
echo    (Nơi có sẵn AI Assistant đồng hành cùng bạn 24/7)
echo =====================================================================
echo.

set ANTIGRAVITY_EXE=C:\Users\ADMIN\AppData\Local\Programs\antigravity\Antigravity.exe

if exist "%ANTIGRAVITY_EXE%" (
    start "" "%ANTIGRAVITY_EXE%" "%~dp0" "%~dp0firmware_esp32\diagram.json"
) else (
    explorer "%~dp0"
)
