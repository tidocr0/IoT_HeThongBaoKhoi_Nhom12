@echo off
chcp 65001 > nul
title MO MO HINH WOKWI TRONG ANTIGRAVITY IDE

set ANTIGRAVITY_EXE=C:\Users\ADMIN\AppData\Local\Programs\antigravity\Antigravity.exe

if exist "%ANTIGRAVITY_EXE%" (
    start "" "%ANTIGRAVITY_EXE%" "%~dp0firmware_esp32\diagram.json"
) else (
    notepad "%~dp0firmware_esp32\diagram.json"
)
