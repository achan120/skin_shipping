@echo off
chcp 65001 >nul
echo ================================================
echo 🐳 使用Docker一键构建APK
echo ================================================
echo.

echo 📋 Docker方案优势：
echo ✅ 一键运行，无需配置环境
echo ✅ 隔离环境，不影响系统
echo ✅ 可重复构建
echo ✅ 支持离线使用
echo.

echo 🔧 前提条件：
echo 1. 安装Docker Desktop（https://www.docker.com/products/docker-desktop）
echo 2. 启动Docker服务
echo.

set /p confirm="Docker已安装并启动？(y/n): "
if /i not "%confirm%"=="y" (
    echo.
    echo 📥 请先安装Docker Desktop：
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b
)

echo.
echo 🚀 开始使用Docker构建APK...
echo.

echo 📁 当前目录：%CD%
echo.

echo 🐳 运行Docker构建容器...
docker run --rm -v "%CD%":/app -w /app kivy/buildozer:latest buildozer android debug

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo ✅ APK构建成功！
    echo ================================================
    echo 📦 APK文件位置：bin\
    echo 📱 请将APK传输到手机安装
    echo.
    if exist "bin\*.apk" (
        echo 📋 生成的APK文件：
        dir /b bin\*.apk
    ) else (
        echo ⚠️  未在bin目录找到APK文件，请检查构建日志
    )
) else (
    echo.
    echo ================================================
    echo ❌ APK构建失败！
    echo ================================================
    echo.
    echo 💡 可能的解决方案：
    echo 1. 确认Docker正在运行
    echo 2. 检查网络连接
    echo 3. 查看上方错误信息
    echo 4. 尝试重新运行脚本
)

echo.
pause
