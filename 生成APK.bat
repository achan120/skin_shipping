@echo off
chcp 65001 >nul
echo ================================================
echo 🚀 发货助手 - APK构建工具
echo ================================================
echo.

echo 📍 当前目录：%CD%
echo 📂 确认在正确目录：%~dp0
cd /d "%~dp0"
echo.

echo ⚡ 开始构建APK文件...
echo ⏰ 预计耗时：10-30分钟
echo 💡 首次构建需要下载Android开发工具，请耐心等待
echo.

buildozer android debug

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo ✅ APK构建成功！
    echo ================================================
    echo 📦 APK文件位置：bin\shippingapp-1.0-debug.apk
    echo 📱 请将APK文件传输到手机进行安装
    echo 📖 安装指南：手机安装使用指南.md
    echo.
    pause
) else (
    echo.
    echo ================================================
    echo ❌ APK构建失败！
    echo ================================================
    echo 💡 可能的解决方案：
    echo    1. 检查网络连接
    echo    2. 重新运行脚本
    echo    3. 查看错误信息
    echo.
    pause
)
