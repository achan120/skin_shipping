@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ==========================================
echo 🚀 发货助手 Android版 - 桌面测试
echo ==========================================
echo.

echo 检查Python环境...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 检查Kivy依赖...
python -c "import kivy" > nul 2>&1
if errorlevel 1 (
    echo ⚠️  未安装Kivy，正在安装...
    pip install kivy[base]
    if errorlevel 1 (
        echo ❌ Kivy安装失败
        pause
        exit /b 1
    )
)

echo 启动测试程序...
echo.
python run_test.py

if errorlevel 1 (
    echo.
    echo ❌ 程序运行出错
    pause
)
