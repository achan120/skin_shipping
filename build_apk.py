#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android APK构建脚本
自动化构建发货助手Android版APK
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_buildozer():
    """检查buildozer是否安装"""
    try:
        result = subprocess.run(['buildozer', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Buildozer版本: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ 未安装Buildozer")
    print("请运行: pip install buildozer")
    return False

def check_android_sdk():
    """检查Android SDK环境"""
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if not android_home:
        print("⚠️  未设置ANDROID_HOME环境变量")
        print("请设置Android SDK路径")
        return False
    
    sdk_path = Path(android_home)
    if not sdk_path.exists():
        print(f"❌ Android SDK路径不存在: {android_home}")
        return False
    
    print(f"✅ Android SDK: {android_home}")
    return True

def prepare_build():
    """准备构建环境"""
    print("🔧 准备构建环境...")
    
    # 清理之前的构建
    build_dirs = ['.buildozer', 'bin']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 确保数据文件存在
    data_dir = Path('data')
    if not data_dir.exists():
        print("❌ 数据目录不存在")
        return False
    
    required_files = [
        'sendGoodsMode.txt',
        'code30day.txt',
        'code90day.txt',
        'code365day.txt',
        'code1day.txt'
    ]
    
    missing_files = []
    for filename in required_files:
        if not (data_dir / filename).exists():
            missing_files.append(filename)
    
    if missing_files:
        print(f"❌ 缺少数据文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 构建环境准备完成")
    return True

def build_debug_apk():
    """构建调试版APK"""
    print("🚀 开始构建调试版APK...")
    
    try:
        # 初始化buildozer（如果需要）
        if not os.path.exists('.buildozer'):
            print("初始化Buildozer...")
            subprocess.run(['buildozer', 'init'], check=True)
        
        # 构建APK
        print("构建APK（这可能需要几分钟）...")
        result = subprocess.run(['buildozer', 'android', 'debug'], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ APK构建成功！")
            
            # 查找生成的APK文件
            bin_dir = Path('bin')
            if bin_dir.exists():
                apk_files = list(bin_dir.glob('*.apk'))
                if apk_files:
                    apk_file = apk_files[0]
                    print(f"📱 APK文件: {apk_file}")
                    print(f"📊 文件大小: {apk_file.stat().st_size / 1024 / 1024:.1f} MB")
                    return True
        
        print("❌ APK构建失败")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程出错: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  构建被用户中断")
        return False

def build_release_apk():
    """构建发布版APK"""
    print("🚀 开始构建发布版APK...")
    print("⚠️  注意：发布版需要签名配置")
    
    try:
        result = subprocess.run(['buildozer', 'android', 'release'], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ 发布版APK构建成功！")
            return True
        else:
            print("❌ 发布版APK构建失败")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程出错: {e}")
        return False

def main():
    """主函数"""
    print("📱 发货助手 Android APK构建工具")
    print("=" * 50)
    
    # 检查环境
    if not check_buildozer():
        return 1
    
    if not check_android_sdk():
        print("提示：可以跳过SDK检查，buildozer会自动下载SDK")
        response = input("是否继续构建？(y/N): ")
        if response.lower() != 'y':
            return 1
    
    # 准备构建
    if not prepare_build():
        return 1
    
    # 选择构建类型
    print("\n构建选项:")
    print("1. 调试版APK（推荐，用于测试）")
    print("2. 发布版APK（需要签名配置）")
    
    try:
        choice = input("请选择 (1-2): ").strip()
        
        if choice == '1':
            success = build_debug_apk()
        elif choice == '2':
            success = build_release_apk()
        else:
            print("无效选择")
            return 1
        
        if success:
            print("\n🎉 构建完成！")
            print("APK文件在 bin/ 目录下")
            print("可以通过ADB安装或直接复制到Android设备")
            return 0
        else:
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹️  构建被用户中断")
        return 1

if __name__ == '__main__':
    sys.exit(main())
