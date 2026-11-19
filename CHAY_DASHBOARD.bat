@echo off
chcp 65001 > nul
cd /d "%~dp0"
title HE THONG BAO KHOI NHOM 12 - NODE-RED MIDDLEWARE & DASHBOARD
cls
echo =====================================================================
echo    HE THONG BAO KHOI CANH BAO SOM - NHOM 12 (DE TAI 04)
echo    Truong nhom: Luc Xuan Thinh - MSSV: 2001230931
echo =====================================================================
echo.

set "PATH=%APPDATA%\npm;%PATH%"

where node-red >nul 2>nul
if errorlevel 1 (
    echo [!] May nay chua cai Node-RED. Dang kiem tra Node.js / npm...
    where npm >nul 2>nul
    if errorlevel 1 (
        echo [LOI] Chua cai Node.js! Vui long cai Node.js LTS tai https://nodejs.org/
        pause
        exit /b 1
    )
    echo [*] Dang tu dong cai dat node-red va node-red-dashboard...
    call npm install -g node-red node-red-dashboard
    if errorlevel 1 (
        echo [LOI] Khong the cai dat Node-RED. Vui long mo CMD voi quyen Admin va chay:
        echo       npm install -g node-red node-red-dashboard
        pause
        exit /b 1
    )
)

set "DASH_INSTALLED=0"
if exist "%APPDATA%\npm\node_modules\node-red-dashboard\package.json" set "DASH_INSTALLED=1"
if exist "%USERPROFILE%\.node-red\node_modules\node-red-dashboard\package.json" set "DASH_INSTALLED=1"
if "%DASH_INSTALLED%"=="0" (
    echo [*] Dang tu dong cai dat module giao dien node-red-dashboard...
    if not exist "%USERPROFILE%\.node-red" mkdir "%USERPROFILE%\.node-red"
    call npm install --prefix "%USERPROFILE%\.node-red" node-red-dashboard
)

if not exist "%~dp0logs" mkdir "%~dp0logs"
if not exist "%~dp0logs\event_history.csv" (
    echo ThoiGian,SuKien,Nguon,Khoi_PPM,NhietDo_C,DoAm_Pct,HanhDong> "%~dp0logs\event_history.csv"
)

set "LOCAL_FLOW=%~dp0application_dashboard\flows_dashboard_telegram.local.json"
set "TEMPLATE_FLOW=%~dp0application_dashboard\flows_dashboard_telegram.json"
set "LOCAL_CRED=%~dp0application_dashboard\flows_dashboard_telegram.local_cred.json"

if not exist "%LOCAL_FLOW%" (
    echo [*] Khoi tao file chay local tu ban mau Git...
    copy /Y "%TEMPLATE_FLOW%" "%LOCAL_FLOW%" > nul
)

if not exist "%LOCAL_CRED%" (
    echo [*] Khoi tao thong tin dang nhap MQTT HiveMQ SSL cho may moi...
    >"%LOCAL_CRED%" (
        echo {
        echo   "mqtt_broker_shared": {
        echo     "user": "iot_t4_1315",
        echo     "password": "iot_t4_1315"
        echo   }
        echo }
    )
)

echo [*] Dang khoi dong may chu Node-RED (Tang 3 Middleware + Tang 4 Dashboard)...
echo [*] Giao dien Dashboard se mo tai: http://localhost:1880/ui
echo [*] Giao dien Thiet ke Flow tai:   http://localhost:1880
echo [*] File CSV Log su kien luu tai: logs\event_history.csv
echo.
echo (Nhan Ctrl + C neu muon dung Node-RED)
echo ---------------------------------------------------------------------
echo.

node-red -s "%~dp0application_dashboard\nodered_settings.js" "%LOCAL_FLOW%"
pause
