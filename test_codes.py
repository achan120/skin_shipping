#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试激活码读取功能
"""

import os

def read_codes_from_file(filename: str):
    """从文件读取激活码"""
    try:
        path = os.path.join('data', filename)
        if not os.path.exists(path):
            print(f"❌ 文件不存在: {path}")
            return []
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        codes = []
        for line in lines:
            line = line.strip()
            # 过滤掉标题、分隔符、空行等，只保留激活码
            if (line and 
                not line.startswith('#') and 
                not line.startswith('激活码列表') and
                not line.startswith('生成时间') and
                not line.startswith('总数') and
                not line.startswith('字符集') and
                not line.startswith('===') and
                not line.startswith('第') and
                not line.startswith('组') and
                '组' not in line and
                len(line) >= 8 and  # 激活码至少8位
                line.isalnum()):    # 只包含字母和数字
                codes.append(line)
        
        return codes
    except Exception as e:
        print(f"❌ 读取激活码失败：{str(e)}")
        return []

if __name__ == '__main__':
    print("测试激活码读取...")
    
    files = [
        'code30day.txt',
        'code1day.txt',
        'code90day.txt',
        'code365day.txt'
    ]
    
    for filename in files:
        codes = read_codes_from_file(filename)
        print(f"\n📄 {filename}:")
        print(f"   找到 {len(codes)} 个激活码")
        if codes:
            print(f"   前5个: {codes[:5]}")
        else:
            print("   ❌ 没有找到有效激活码")
