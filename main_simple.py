#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android版发货软件 - 简化版本（解决中文显示问题）
"""

import os
import sys
import random
from typing import List

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger

# 设置窗口大小（仅在桌面端测试时使用）
if platform != 'android':
    Window.size = (420, 750)

class ShippingApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_dir = self.get_base_dir()
        self.current_content = ""
        self.copy_context = 'single'
        
    def get_base_dir(self) -> str:
        """获取应用数据目录"""
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path
                return os.path.join(primary_external_storage_path(), 'ShippingApp')
            except ImportError:
                Logger.warning('Android storage not available, using local directory')
                return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        else:
            # 桌面测试时使用data子目录
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    def build(self):
        """构建主界面"""
        # 创建数据目录
        os.makedirs(self.base_dir, exist_ok=True)
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 标题
        title = Label(
            text='发货助手 Android版',
            size_hint_y=None,
            height=60,
            font_size='22sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title)
        
        # 按钮区域 - 使用英文标签避免中文显示问题
        button_layout = GridLayout(cols=2, size_hint_y=None, height=280, spacing=10, padding=5)
        
        # 功能按钮 - 临时使用英文
        buttons = [
            ('Ship', self.on_shipping),
            ('Bulk', self.on_bulk),
            ('30D', lambda x: self.on_fill_code('30')),
            ('90D', lambda x: self.on_fill_code('90')),
            ('365D', lambda x: self.on_fill_code('365')),
            ('Import', self.on_import_file),
            ('Copy', self.on_copy),
            ('Clear', self.on_clear)
        ]
        
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=60,
                font_size='18sp',
                bold=True
            )
            btn.bind(on_press=callback)
            button_layout.add_widget(btn)
        
        main_layout.add_widget(button_layout)
        
        # 文本编辑区域
        text_label = Label(
            text='Content Editor:',
            size_hint_y=None,
            height=40,
            font_size='16sp',
            bold=True,
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(text_label)
        
        # 可滚动的文本输入框
        scroll = ScrollView()
        self.text_input = TextInput(
            text='',
            multiline=True,
            size_hint_y=None,
            font_size='14sp',
            padding=[10, 10, 10, 10]
        )
        self.text_input.bind(minimum_height=self.text_input.setter('height'))
        scroll.add_widget(self.text_input)
        main_layout.add_widget(scroll)
        
        # 状态栏
        self.status_label = Label(
            text='Ready',
            size_hint_y=None,
            height=40,
            font_size='14sp',
            color=(0.6, 0.6, 0.6, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # 初始化默认内容
        Clock.schedule_once(self.load_default_content, 0.1)
        
        return main_layout
    
    def update_status(self, message: str):
        """更新状态栏"""
        self.status_label.text = message
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Ready'), 3)
    
    def load_default_content(self, dt):
        """加载默认内容"""
        try:
            path = os.path.join(self.base_dir, 'sendGoodsMode.txt')
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self.text_input.text = content
                    self.current_content = content
            else:
                # 创建默认内容文件
                default_content = """会员您好，您购买的商品现为您发货：

最新链接：复制粘贴到浏览器，直接下载：
https://workdrive.zohopublic.com.cn/external/abca5cb143d6f162815cd40eddcb1094c348a0afa325244a13b713bbd0d30db/download

固定链接：我用夸克网盘给您分享了软件，点击链接或复制整段内容，打开「夸克APP」即可获取
链接：https://pan.quark.cn/s/a71a458ccea7

如果您经常在网吧使用，请找我兑换网吧激活码

下载后，双击 TS_v2.3.1 .exe ，打开 TS 文件夹，启动GO，复制粘贴激活码就成，直接使用

软件包内有 使用视频教程，和使用说明

后面有任何疑问，或者不懂的，不用自己想，直接随时找我解决就行"""
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(default_content)
                
                self.text_input.text = default_content
                self.current_content = default_content
        except Exception as e:
            self.update_status(f'Load error: {str(e)}')
    
    def read_codes_from_file(self, filename: str) -> List[str]:
        """从文件读取激活码"""
        try:
            path = os.path.join(self.base_dir, filename)
            if not os.path.exists(path):
                return []
            
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            codes = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    codes.append(line)
            
            return codes
        except Exception as e:
            self.update_status(f'Read codes error: {str(e)}')
            return []
    
    def on_shipping(self, instance):
        """发货按钮"""
        self.copy_context = 'single'
        self.load_default_content(None)
        self.update_status('Loaded shipping template')
    
    def on_bulk(self, instance):
        """散装按钮"""
        self.copy_context = 'bulk'
        try:
            # 加载基础内容
            base_content = self.current_content or self.text_input.text
            
            # 读取散装激活码
            codes_30 = self.read_codes_from_file('code30day.txt')
            codes_1 = self.read_codes_from_file('code1day.txt')
            
            if not codes_30 and not codes_1:
                self.update_status('No activation codes found')
                return
            
            # 构建散装内容
            lines = [base_content]
            
            if codes_30:
                lines.append('\n30天散装激活码：')
                for code in codes_30[:25]:  # 限制25个
                    lines.append(code)
            
            if codes_1:
                lines.append('\n以下是25个1天的激活码，激活之后才开始生效：')
                # 添加空行分组
                for i, code in enumerate(codes_1[:25]):
                    if i == 10 or i == 15:  # 在第10和15个后添加空行
                        lines.append('')
                    lines.append(code)
            
            bulk_content = '\n'.join(lines)
            self.text_input.text = bulk_content
            self.update_status('Loaded bulk mode')
            
        except Exception as e:
            self.update_status(f'Bulk load error: {str(e)}')
    
    def on_fill_code(self, days: str):
        """填充指定天数的激活码"""
        self.copy_context = 'single'
        try:
            # 读取对应的激活码文件
            filename = f'code{days}day.txt'
            codes = self.read_codes_from_file(filename)
            
            if not codes:
                self.update_status(f'No {days}D codes found')
                return
            
            # 随机选择一个激活码
            code = random.choice(codes)
            
            # 重新加载基础内容
            self.load_default_content(None)
            base_content = self.text_input.text
            
            # 移除现有的激活码行
            lines = base_content.split('\n')
            filtered_lines = []
            for line in lines:
                if not (line.strip().startswith('30天激活码：') or 
                       line.strip().startswith('90天激活码：') or 
                       line.strip().startswith('365天激活码：')):
                    filtered_lines.append(line)
            
            # 在"如果您经常在网吧使用"之前插入新的激活码
            activation_line = f'{days}天激活码：{code}'
            
            final_lines = []
            inserted = False
            for line in filtered_lines:
                if '如果您经常在网吧使用' in line and not inserted:
                    final_lines.append(activation_line)
                    final_lines.append('')  # 空行
                    inserted = True
                final_lines.append(line)
            
            # 如果没有找到插入位置，添加到末尾
            if not inserted:
                final_lines.append('')
                final_lines.append(activation_line)
            
            content = '\n'.join(final_lines)
            self.text_input.text = content
            self.update_status(f'Filled {days}D activation code')
            
        except Exception as e:
            self.update_status(f'Fill code error: {str(e)}')
    
    def on_import_file(self, instance):
        """导入文件"""
        self.update_status('Import function not implemented in simple version')
    
    def on_copy(self, instance):
        """复制内容到剪贴板"""
        try:
            content = self.text_input.text
            if not content.strip():
                self.update_status('No content to copy')
                return
            
            # 根据复制上下文进行文本处理
            if self.copy_context == 'bulk':
                # 散装模式：保持原有格式
                processed_content = content
            else:
                # 单个模式：规范化空行
                processed_content = self.normalize_text_for_paste(content)
            
            Clipboard.copy(processed_content)
            self.update_status('Content copied to clipboard')
            
        except Exception as e:
            self.update_status(f'Copy error: {str(e)}')
    
    def normalize_text_for_paste(self, text: str) -> str:
        """规范化文本中的空行"""
        import re
        # 将多个连续空行合并为单个空行
        normalized = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        return normalized.strip()
    
    def on_clear(self, instance):
        """清空内容"""
        self.text_input.text = ''
        self.update_status('Content cleared')


if __name__ == '__main__':
    ShippingApp().run()
