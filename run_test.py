#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android版发货软件 - 桌面测试启动器
用于在开发环境中测试Android版本的功能
"""

import os
import sys
import shutil

def setup_test_environment():
    """设置测试环境"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # 确保数据目录存在
    os.makedirs(data_dir, exist_ok=True)
    
    # 检查必要文件是否存在
    required_files = [
        'sendGoodsMode.txt',
        'code30day.txt',
        'code90day.txt', 
        'code365day.txt',
        'code1day.txt'
    ]
    
    missing_files = []
    for filename in required_files:
        file_path = os.path.join(data_dir, filename)
        if not os.path.exists(file_path):
            missing_files.append(filename)
    
    if missing_files:
        print("⚠️  缺少以下数据文件：")
        for filename in missing_files:
            print(f"   - {filename}")
        print(f"\n请将这些文件复制到：{data_dir}")
        print("\n或者从上级目录自动复制...")
        
        # 尝试从上级目录复制
        parent_dir = os.path.dirname(current_dir)
        copied_files = []
        
        for filename in missing_files:
            source_path = os.path.join(parent_dir, filename)
            if os.path.exists(source_path):
                dest_path = os.path.join(data_dir, filename)
                try:
                    shutil.copy2(source_path, dest_path)
                    copied_files.append(filename)
                    print(f"✅ 已复制: {filename}")
                except Exception as e:
                    print(f"❌ 复制失败 {filename}: {e}")
        
        if copied_files:
            print(f"\n成功复制了 {len(copied_files)} 个文件")
        
        remaining_missing = [f for f in missing_files if f not in copied_files]
        if remaining_missing:
            print(f"\n仍然缺少 {len(remaining_missing)} 个文件，请手动复制")
            return False
    
    print("✅ 数据文件检查完成")
    return True

def check_dependencies():
    """检查依赖库"""
    try:
        import kivy
        print(f"✅ Kivy 版本: {kivy.__version__}")
    except ImportError:
        print("❌ 未安装 Kivy")
        print("   请运行: pip install kivy[base]")
        return False
    
    try:
        import docx
        print("✅ python-docx 已安装")
    except ImportError:
        print("⚠️  未安装 python-docx (DOCX导入功能将不可用)")
        print("   可选安装: pip install python-docx")
    
    return True

def main():
    """主函数"""
    print("🚀 发货助手 Android版 - 桌面测试")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 设置测试环境
    if not setup_test_environment():
        return 1
    
    print("\n🎯 启动应用...")
    print("   提示：这是Android版本在桌面环境的测试")
    print("   实际Android设备上的体验会更好")
    print()
    
    # 启动主程序
    try:
        from main import ShippingAppMain
        ShippingAppMain().run()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
