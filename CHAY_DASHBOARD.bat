@echo off
chcp 65001 > nul
title HE THONG BAO KHOI NHOM 12 - NODE-RED DASHBOARD
cls
echo =====================================================================
echo    HỆ THỐNG BÁO KHÓI CẢNH BÁO SỚM - NHÓM 12 (ĐỀ TÀI 04)
echo    Trưởng nhóm: Lục Xuân Thịnh - MSSV: 2001230931
echo =====================================================================
echo.
echo [*] Đang khởi động máy chủ Node-RED Dashboard...
echo [*] Giao diện Dashboard sẽ mở tại: http://localhost:1880/ui
echo [*] Giao diện Thiết kế Flow tại:   http://localhost:1880
echo.
echo (Nhấn Ctrl + C nếu muốn dừng Node-RED)
echo ---------------------------------------------------------------------
echo.

node-red "%~dp0application_dashboard\flows_dashboard_telegram.local.json"
pause
