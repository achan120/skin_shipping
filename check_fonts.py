#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查系统字体是否支持中文
"""

import os
from kivy.core.text import LabelBase

def check_fonts():
    """检查可用的中文字体"""
    print("检查系统字体...")
    
    # Windows字体路径
    windows_fonts = [
        ('微软雅黑', 'C:/Windows/Fonts/msyh.ttc'),
        ('微软雅黑Light', 'C:/Windows/Fonts/msyhl.ttc'),
        ('宋体', 'C:/Windows/Fonts/simsun.ttc'),
        ('黑体', 'C:/Windows/Fonts/simhei.ttf'),
        ('楷体', 'C:/Windows/Fonts/simkai.ttf'),
        ('仿宋', 'C:/Windows/Fonts/simfang.ttf'),
    ]
    
    found_fonts = []
    
    for name, path in windows_fonts:
        if os.path.exists(path):
            print(f"✅ 找到字体: {name} -> {path}")
            found_fonts.append((name, path))
        else:
            print(f"❌ 未找到: {name} -> {path}")
    
    if found_fonts:
        print(f"\n总共找到 {len(found_fonts)} 个中文字体")
        
        # 尝试注册第一个找到的字体
        name, path = found_fonts[0]
        try:
            LabelBase.register(name='TestChinese', fn_regular=path)
            print(f"✅ 成功注册字体: {name}")
            return True
        except Exception as e:
            print(f"❌ 注册字体失败: {e}")
            return False
    else:
        print("❌ 没有找到任何中文字体")
        return False

if __name__ == '__main__':
    check_fonts()
