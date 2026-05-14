@echo off
chcp 65001 >nul
echo ========================================
echo    Outlook 注册 - 启动 CloakBrowser
echo ========================================
echo.

cd /d "%~dp0"
python start_cloakbrowser.py

if errorlevel 1 (
    echo.
    echo ❌ 启动失败！请检查：
    echo    1. Python 是否已安装
    echo    2. CloakBrowser 路径是否正确
    echo.
    pause
)
