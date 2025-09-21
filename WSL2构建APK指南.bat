@echo off
chcp 65001 >nul
echo ================================================
echo 🚀 使用WSL2本地构建APK - 完整指南
echo ================================================
echo.

echo 📋 WSL2方案优势：
echo ✅ 在Windows内直接使用Linux环境
echo ✅ 无需虚拟机，性能更好
echo ✅ 文件共享方便
echo ✅ 一次配置，永久使用
echo.

echo 🔧 第一步：安装WSL2
echo.
echo 1. 以管理员身份运行PowerShell
echo 2. 执行：wsl --install
echo 3. 重启电脑
echo 4. 设置Ubuntu用户名密码
echo.

echo 📦 第二步：在WSL中安装依赖
echo.
echo 打开WSL终端，执行以下命令：
echo.
echo # 更新系统
echo sudo apt update && sudo apt upgrade -y
echo.
echo # 安装Java和Python
echo sudo apt install -y openjdk-17-jdk python3 python3-pip
echo.
echo # 安装构建依赖
echo sudo apt install -y git zip unzip autoconf libtool pkg-config
echo sudo apt install -y zlib1g-dev libncurses5-dev libncursesw5-dev 
echo sudo apt install -y libtinfo5 cmake libffi-dev libssl-dev
echo.
echo # 安装Buildozer
echo pip3 install --user buildozer
echo export PATH=$PATH:~/.local/bin
echo.

echo 🏗️ 第三步：构建APK
echo.
echo # 进入项目目录（Windows文件在/mnt/下）
echo cd /mnt/d/phpEnv/www/localhost/sendGoods/android
echo.
echo # 构建APK
echo buildozer android debug
echo.

echo ================================================
echo 💡 提示：
echo - WSL安装后需要重启电脑
echo - 构建过程约15-30分钟
echo - 生成的APK在bin目录下
echo ================================================
echo.

set /p install="现在开始安装WSL2吗？(y/n): "
if /i "%install%"=="y" (
    echo.
    echo 🚀 正在以管理员权限安装WSL2...
    powershell -Command "Start-Process powershell -ArgumentList 'wsl --install' -Verb RunAs"
    echo.
    echo ✅ WSL安装命令已执行
    echo 📋 请按提示完成安装并重启电脑
) else (
    echo 已取消安装
)

pause
