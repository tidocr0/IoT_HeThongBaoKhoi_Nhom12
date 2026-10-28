@echo off
chcp 65001 > nul
title MO DU AN TRONG ANTIGRAVITY IDE - NHOM 12
echo =====================================================================
echo    ĐANG KHỞI ĐỘNG DỰ ÁN TRÊN ANTIGRAVITY IDE...
echo =====================================================================
echo.

set ANTIGRAVITY_EXE=C:\Users\ADMIN\AppData\Local\Programs\antigravity\Antigravity.exe

if exist "%ANTIGRAVITY_EXE%" (
    start "" "%ANTIGRAVITY_EXE%" "%~dp0"
) else (
    explorer "%~dp0"
)
