#!/bin/bash

echo "================================================"
echo "🚀 发货助手 - WSL一键构建APK"
echo "================================================"
echo

# 检查是否在WSL中
if [[ ! -f /proc/version ]] || ! grep -q Microsoft /proc/version; then
    echo "❌ 请在WSL中运行此脚本"
    exit 1
fi

echo "📋 第1步：检查和安装依赖..."

# 检查Java
if ! command -v java &> /dev/null; then
    echo "📦 安装Java 8..."
    sudo apt update
    sudo apt install -y openjdk-8-jdk
    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    export PATH=$PATH:$JAVA_HOME/bin
    echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
    echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
else
    echo "✅ Java已安装"
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "📦 安装Python..."
    sudo apt install -y python3 python3-pip
else
    echo "✅ Python已安装"
fi

# 检查构建工具
echo "📦 安装构建依赖..."
sudo apt install -y git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential ccache

# 检查Buildozer
if ! command -v buildozer &> /dev/null; then
    echo "📦 安装Buildozer..."
    pip3 install --user buildozer==1.5.0 cython==0.29.33
    export PATH=$PATH:~/.local/bin
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
else
    echo "✅ Buildozer已安装"
fi

echo
echo "📋 第2步：准备项目文件..."

# 创建项目目录
PROJECT_DIR="$HOME/shipping-app"
if [ -d "$PROJECT_DIR" ]; then
    echo "🔄 清理旧项目..."
    rm -rf "$PROJECT_DIR"
fi

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 从Windows复制文件
WINDOWS_PATH="/mnt/d/phpEnv/www/localhost/sendGoods/android"
if [ -d "$WINDOWS_PATH" ]; then
    echo "📁 从Windows复制项目文件..."
    cp "$WINDOWS_PATH"/* . -r
    
    # 验证重要文件
    if [ ! -f "main_chinese.py" ]; then
        echo "❌ 主程序文件不存在: main_chinese.py"
        exit 1
    fi
    
    if [ ! -f "buildozer.spec" ]; then
        echo "❌ 配置文件不存在: buildozer.spec"
        exit 1
    fi
    
    echo "✅ 项目文件复制完成"
    echo "📋 项目文件列表："
    ls -la
else
    echo "❌ Windows项目路径不存在: $WINDOWS_PATH"
    echo "💡 请修改脚本中的路径为您的实际项目路径"
    exit 1
fi

echo
echo "📋 第3步：开始构建APK..."
echo "⏰ 预计耗时：15-30分钟"
echo "☕ 可以去喝杯咖啡..."
echo

# 清理之前的构建
rm -rf .buildozer bin

# 设置环境变量
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin:~/.local/bin

# 开始构建
echo "🚀 执行 buildozer android debug..."
buildozer android debug

# 检查构建结果
if [ -f "bin/"*.apk ]; then
    echo
    echo "================================================"
    echo "🎉 APK构建成功！"
    echo "================================================"
    echo
    
    APK_FILE=$(ls bin/*.apk | head -1)
    echo "📱 APK文件：$APK_FILE"
    echo "📦 文件大小：$(du -h "$APK_FILE" | cut -f1)"
    
    # 复制到Windows目录
    echo "📋 复制APK到Windows目录..."
    cp bin/*.apk "$WINDOWS_PATH/"
    
    echo "✅ APK已复制到Windows项目目录"
    echo "📁 Windows路径：$WINDOWS_PATH"
    echo
    echo "📱 接下来："
    echo "1. 在Windows中找到APK文件"
    echo "2. 传输到手机"  
    echo "3. 安装并使用"
    echo
else
    echo
    echo "================================================"
    echo "❌ APK构建失败"
    echo "================================================"
    echo
    echo "💡 可能的解决方案："
    echo "1. 检查上面的错误信息"
    echo "2. 确保网络连接正常"
    echo "3. 重新运行脚本"
    echo "4. 检查依赖是否正确安装"
    echo
    
    if [ -d ".buildozer" ]; then
        echo "📋 查看详细日志："
        echo "tail -50 .buildozer/android/platform/build-*/build.log"
    fi
fi

echo "脚本执行完成"
