@echo off
chcp 65001 > nul
title MO SO DO WOKWI TRONG ANTIGRAVITY IDE

set ANTIGRAVITY_EXE=C:\Users\ADMIN\AppData\Local\Programs\antigravity\Antigravity.exe

if exist "%ANTIGRAVITY_EXE%" (
    start "" "%ANTIGRAVITY_EXE%" -r "%~dp0firmware_esp32\diagram.json"
) else (
    notepad "%~dp0firmware_esp32\diagram.json"
)
