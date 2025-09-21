#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android版发货软件 - 中文支持版本
"""

import os
import sys
import json
import random
from typing import List, Optional

# 设置编码
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger
from kivy.core.text import LabelBase

# 设置窗口大小（仅在桌面端测试时使用）
if platform != 'android':
    Window.size = (420, 750)

# 注册中文字体 - 在App类定义之前
def register_chinese_font():
    """注册中文字体"""
    if platform == 'android':
        # Android字体路径
        font_paths = [
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/NotoSansCJK.ttc',
        ]
    else:
        # Windows字体路径
        font_paths = [
            'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
            'C:/Windows/Fonts/msyhl.ttc',   # 微软雅黑Light
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='Chinese', fn_regular=font_path)
                Logger.info(f'Font: Registered Chinese font: {font_path}')
                return True
            except Exception as e:
                Logger.warning(f'Font: Failed to register {font_path}: {e}')
                continue
    
    Logger.warning('Font: No Chinese font found, using system default')
    return False

# 注册字体
chinese_font_available = register_chinese_font()

class ShippingApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_dir = self.get_base_dir()
        self.current_content = ""
        self.copy_context = 'single'
        # 激活码文件路径存储
        self.code_file_paths = {
            '1': None,    # 1天激活码文件路径
            '30': None,   # 30天激活码文件路径
            '90': None,   # 90天激活码文件路径
            '365': None   # 365天激活码文件路径
        }
        # 激活码使用状态跟踪
        self.current_codes = {
            'bulk': [],      # 当前显示的散装激活码
            '30': None,      # 当前显示的30天激活码
            '90': None,      # 当前显示的90天激活码  
            '365': None      # 当前显示的365天激活码
        }
        self.codes_used = {
            'bulk': False,   # 散装激活码是否已使用
            '30': False,     # 30天激活码是否已使用
            '90': False,     # 90天激活码是否已使用
            '365': False     # 365天激活码是否已使用
        }
        self.load_code_file_paths()
        
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
        
        # 主布局 - 深色背景
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=15, 
            spacing=12
        )
        
        # 设置现代化渐变背景
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.05, 0.05, 0.1, 1)  # 深蓝黑色背景
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # 超极简标题区域
        title_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=18,  # 进一步减少到18px
            padding=[3, 1, 3, 1]  # 极小padding
        )
        
        # 超小标题
        title = Label(
            text='📦 发货助手',
            font_size='12sp',  # 减小到12sp
            font_name='Chinese' if chinese_font_available else None,
            bold=True,
            color=(0.9, 0.95, 1, 1),
            halign='center'
        )
        title_layout.add_widget(title)
        
        main_layout.add_widget(title_layout)
        
        # 可滚动的文本输入框（增加高度）
        scroll = ScrollView(
            bar_width=10,  # 滚动条宽度
            scroll_type=['bars', 'content'],  # 显示滚动条
            effect_cls='ScrollEffect'  # 滚动效果
        )
        
        # 超大文本输入框 - 极致显示空间
        self.text_input = TextInput(
            text='',
            multiline=True,
            size_hint_y=None,
            height=510,  # 进一步增加到510px
            font_size='14sp',
            background_color=(0.95, 0.97, 1, 1),
            foreground_color=(0.1, 0.1, 0.2, 1),
            cursor_color=(0.3, 0.5, 0.9, 1),
            selection_color=(0.3, 0.5, 0.9, 0.3),
            padding=[12, 10, 12, 10],  # 进一步减少padding
            font_name='Chinese' if chinese_font_available else None
        )
        
        # 确保文本框内容超出时可以滚动
        self.text_input.bind(minimum_height=self.text_input.setter('height'))
        scroll.add_widget(self.text_input)
        main_layout.add_widget(scroll)
        
        # 激活码按钮区域 - 进一步压缩
        code_layout = GridLayout(
            cols=2,
            size_hint_y=None,
            height=95,  # 再减少5px
            spacing=10,
            padding=[8, 3, 8, 3]  # 减少上下padding
        )
        
        # 激活码按钮 - 与底部按钮统一尺寸
        code_buttons = [
            ('365天', lambda x: self.on_fill_code('365'), (0.8, 0.2, 0.3, 1)),
            ('30天', lambda x: self.on_fill_code('30'), (0.2, 0.7, 0.3, 1)),
            ('90天', lambda x: self.on_fill_code('90'), (0.9, 0.6, 0.1, 1)),
            ('散装', self.on_bulk, (0.5, 0.3, 0.8, 1)),
        ]
        
        for text, callback, color in code_buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=45,  # 与底部按钮统一高度
                font_size='16sp',
                font_name='Chinese' if chinese_font_available else None,
                bold=True,
                background_color=color,
                background_normal='',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            code_layout.add_widget(btn)
        
        main_layout.add_widget(code_layout)
        
        # 底部按钮区域 - 三按钮布局
        bottom_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=52,
            spacing=8,  # 稍微减少间距适应三个按钮
            padding=[8, 3, 8, 3]
        )
        
        # 上传按钮 - 左侧
        upload_btn = Button(
            text='📁 上传',
            size_hint_x=0.3,  # 调整为30%
            size_hint_y=None,
            height=45,
            font_size='15sp',  # 稍微减小字体适应三按钮
            font_name='Chinese' if chinese_font_available else None,
            bold=True,
            background_color=(0.3, 0.5, 0.9, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        upload_btn.bind(on_press=self.on_upload)
        bottom_layout.add_widget(upload_btn)
        
        # 编辑按钮 - 中间
        edit_btn = Button(
            text='✏️ 编辑',
            size_hint_x=0.25,  # 25%宽度
            size_hint_y=None,
            height=45,
            font_size='15sp',
            font_name='Chinese' if chinese_font_available else None,
            bold=True,
            background_color=(0.8, 0.6, 0.2, 1),  # 橙色系
            background_normal='',
            color=(1, 1, 1, 1)
        )
        edit_btn.bind(on_press=self.on_edit)
        bottom_layout.add_widget(edit_btn)
        
        # 复制内容按钮 - 右侧
        copy_btn = Button(
            text='📋 复制内容',
            size_hint_x=0.45,  # 调整为45%
            size_hint_y=None,
            height=45,
            font_size='15sp',  # 稍微减小字体
            font_name='Chinese' if chinese_font_available else None,
            bold=True,
            background_color=(0.2, 0.8, 0.4, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        copy_btn.bind(on_press=self.on_copy)
        bottom_layout.add_widget(copy_btn)
        
        main_layout.add_widget(bottom_layout)
        
        # 清晰状态栏
        self.status_label = Label(
            text='✨ 准备就绪',
            size_hint_y=None,
            height=32,  # 增加到32px给字体更多空间
            font_size='14sp',  # 增大到14sp，更清晰可读
            font_name='Chinese' if chinese_font_available else None,
            color=(0.6, 0.8, 1, 1),
            halign='center'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        main_layout.add_widget(self.status_label)
        
        # 绑定文本变化事件，用于自动保存草稿
        self.text_input.bind(text=self.on_text_changed)
        
        # 初始化默认内容 - 启动时自动加载模板
        Clock.schedule_once(self.load_default_content, 0.1)
        
        # 标记是否为程序自动更新文本（避免在自动加载时触发保存）
        self.is_auto_update = False
        
        # 编辑模式状态
        self.is_editing = False
        
        return main_layout
    
    def load_code_file_paths(self):
        """加载激活码文件路径配置"""
        try:
            config_path = os.path.join(self.base_dir, 'code_paths.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.code_file_paths.update(json.load(f))
        except Exception as e:
            Logger.warning(f'Failed to load code file paths: {e}')
    
    def save_code_file_paths(self):
        """保存激活码文件路径配置"""
        try:
            config_path = os.path.join(self.base_dir, 'code_paths.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.code_file_paths, f, ensure_ascii=False, indent=2)
        except Exception as e:
            Logger.warning(f'Failed to save code file paths: {e}')
    
    def _update_rect(self, instance, value):
        """更新背景矩形"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def show_message(self, title: str, message: str):
        """显示消息弹窗"""
        popup = Popup(
            title=title,
            content=Label(
                text=message, 
                text_size=(300, None), 
                halign='center',
                font_name='Chinese' if chinese_font_available else None
            ),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def update_status(self, message: str):
        """更新状态栏"""
        self.status_label.text = message
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', '就绪'), 3)
    
    def load_default_content(self, dt):
        """加载默认内容 - 优先加载草稿"""
        try:
            self.is_auto_update = True  # 标记为自动更新，避免触发保存
            
            # 检查是否有草稿文件
            draft_path = os.path.join(self.base_dir, 'draft.txt')
            template_path = os.path.join(self.base_dir, 'sendGoodsMode.txt')
            
            if os.path.exists(draft_path):
                # 有草稿文件，直接加载草稿
                with open(draft_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self.text_input.text = content
                    self.current_content = content
                    self.update_status('已加载草稿内容')
                return
            
            # 没有草稿，加载默认模板
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self.text_input.text = content
                    self.current_content = content
                    self.update_status('已加载默认模板')
            else:
                # 加载内置默认内容
                self.load_builtin_template()
                
        except Exception as e:
            self.update_status(f'加载内容失败：{str(e)}')
        finally:
            self.is_auto_update = False
    
    def load_builtin_template(self):
        """加载内置默认模板"""
        default_content = """会员您好，您购买的商品现为您发货：

最新链接：复制粘贴到浏览器，直接下载：
https://workdrive.zohopublic.com.cn/external/a54d69935446b55e625ee705ccb564d7cf0773adcaaf4a03bbd11dfbad4867fb/download

固定链接：我用夸克网盘给您分享了软件，点击链接或复制整段内容，打开「夸克APP」即可获取
链接：https://pan.quark.cn/s/a71a458ccea7

如果您经常在网吧使用，请找我兑换网吧激活码

下载后，双击 TS_v2.3.1 .exe ，打开 TS 文件夹，启动GO，复制粘贴激活码就成，直接使用

软件包内有 使用视频教程，和使用说明

后面有任何疑问，或者不懂的，不用自己想，直接随时找我解决就行"""
        
        # 创建默认模板文件
        template_path = os.path.join(self.base_dir, 'sendGoodsMode.txt')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        
        self.text_input.text = default_content
        self.current_content = default_content
        self.update_status('已创建默认模板')
    
    
    def on_text_changed(self, instance, text):
        """文本改变时自动保存草稿"""
        if self.is_auto_update or not self.is_editing:
            return  # 如果是程序自动更新或不在编辑模式，不保存草稿
            
        try:
            # 延迟保存，避免频繁IO操作
            Clock.unschedule(self.save_draft)
            Clock.schedule_once(self.save_draft, 1.0)  # 1秒后保存
        except Exception as e:
            Logger.warning(f'Schedule save draft failed: {e}')
    
    def save_draft(self, dt=None):
        """保存草稿到文件"""
        try:
            if not self.text_input.text.strip():
                return  # 空内容不保存
                
            draft_path = os.path.join(self.base_dir, 'draft.txt')
            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(self.text_input.text)
        except Exception as e:
            Logger.warning(f'Save draft failed: {e}')
    
    def is_valid_code(self, s: str) -> bool:
        """验证激活码是否有效 - 与桌面端逻辑一致"""
        s = s.strip()
        if len(s) != 10:
            return False
        for ch in s:
            if not (ch.isdigit() or ('A' <= ch <= 'Z')):
                return False
        return True
    
    def read_codes_from_file(self, filename: str) -> List[str]:
        """从文件读取激活码 - 优先从用户上传的文件读取"""
        try:
            # 提取天数标识
            days = filename.replace('code', '').replace('day.txt', '')
            
            # 优先使用用户上传的文件路径
            if self.code_file_paths.get(days):
                path = self.code_file_paths[days]
                if not os.path.exists(path):
                    self.update_status(f'上传的{days}天激活码文件不存在')
                    return []
            else:
                # 回退到默认路径
                path = os.path.join(self.base_dir, filename)
                if not os.path.exists(path):
                    return []
            
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            codes = []
            for line in lines:
                line = line.strip()
                # 过滤掉标题、分隔符、空行等，只保留激活码
                # 使用与桌面端一致的验证逻辑：10位，只包含大写字母A-Z和数字0-9
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
                    not '以下是25个1天的激活码' in line and
                    self.is_valid_code(line)):
                    codes.append(line)
            
            return codes
        except Exception as e:
            self.update_status(f'读取激活码失败：{str(e)}')
            return []
    
    def on_bulk(self, instance):
        """散装按钮 - 25个1天激活码（延迟消耗机制）"""
        self.copy_context = 'bulk'
        try:
            # 重新加载基础内容，确保没有单个激活码
            self.load_default_content(None)
            base_content = self.text_input.text
            
            # 移除基础内容中可能存在的单个激活码行
            lines = base_content.split('\n')
            filtered_lines = []
            for line in lines:
                if not (line.strip().startswith('30天激活码：') or 
                       line.strip().startswith('90天激活码：') or 
                       line.strip().startswith('365天激活码：')):
                    filtered_lines.append(line)
            
            clean_base_content = '\n'.join(filtered_lines)
            
            # 如果还没有使用过当前激活码，重用当前激活码
            if not self.codes_used['bulk'] and self.current_codes['bulk']:
                codes_to_use = self.current_codes['bulk']
                self.update_status('已加载散装模式（重用当前激活码）')
            else:
                # 读取新的1天激活码
                codes_1 = self.read_codes_from_file('code1day.txt')
                
                if not codes_1:
                    self.show_message('警告', '未找到1天激活码文件')
                    return
                
                if len(codes_1) < 25:
                    self.show_message('警告', f'1天激活码不足25个，只有{len(codes_1)}个')
                    return
                
                # 保存新的激活码，但不标记为已使用
                codes_to_use = codes_1[:25]
                self.current_codes['bulk'] = codes_to_use
                self.codes_used['bulk'] = False
                self.update_status('已加载散装模式（25个新激活码）')
            
            # 构建散装内容 - 与桌面端逻辑一致
            content_parts = [clean_base_content]
            content_parts.append('\n以下是25个1天的激活码，激活之后才开始生效：')
            
            # 添加25个1天激活码，在第10和15个后添加空行
            for i, code in enumerate(codes_to_use):
                content_parts.append(code)
                # 在第10和15个激活码后添加空行
                if i == 9 or i == 14:  # 索引从0开始，第10个是索引9，第15个是索引14
                    content_parts.append('')
            
            bulk_content = '\n'.join(content_parts)
            self.text_input.text = bulk_content
            
        except Exception as e:
            self.show_message('错误', f'加载散装内容失败：{str(e)}')
    
    def on_fill_code(self, days: str):
        """填充指定天数的激活码（延迟消耗机制）"""
        self.copy_context = 'single'
        try:
            # 如果还没有使用过当前激活码，重用当前激活码
            if not self.codes_used[days] and self.current_codes[days]:
                code = self.current_codes[days]
                self.update_status(f'已填充{days}天激活码（重用当前激活码）')
            else:
                # 读取新的激活码
                filename = f'code{days}day.txt'
                codes = self.read_codes_from_file(filename)
                
                if not codes:
                    self.show_message('警告', f'未找到{days}天激活码文件')
                    return
                
                # 随机选择一个新的激活码
                code = random.choice(codes)
                
                # 保存新的激活码，但不标记为已使用
                self.current_codes[days] = code
                self.codes_used[days] = False
                self.update_status(f'已填充{days}天激活码（新激活码）')
            
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
            self.update_status(f'已填充{days}天激活码')
            
        except Exception as e:
            self.show_message('错误', f'填充{days}天激活码失败：{str(e)}')
    
    def on_upload_codes(self, instance):
        """上传激活码文件"""
        try:
            # 创建激活码类型选择弹窗
            content = BoxLayout(orientation='vertical', padding=20, spacing=15)
            
            title_label = Label(
                text='选择要上传的激活码类型：',
                size_hint_y=None,
                height=40,
                font_size='18sp',
                font_name='Chinese' if chinese_font_available else None,
                bold=True,
                color=(0.2, 0.2, 0.2, 1)
            )
            content.add_widget(title_label)
            
            # 激活码类型按钮
            button_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, height=180)
            
            code_types = [
                ('1天激活码', '1'),
                ('30天激活码', '30'),
                ('90天激活码', '90'),
                ('365天激活码', '365')
            ]
            
            for text, days in code_types:
                btn = Button(
                    text=text,
                    size_hint_y=None,
                    height=40,
                    font_size='16sp',
                    font_name='Chinese' if chinese_font_available else None,
                    background_color=(0.2, 0.6, 1, 1),
                    color=(1, 1, 1, 1)
                )
                btn.bind(on_press=lambda x, d=days: self.select_code_file(d, popup))
                button_layout.add_widget(btn)
            
            content.add_widget(button_layout)
            
            # 取消按钮
            cancel_btn = Button(
                text='取消',
                size_hint_y=None,
                height=40,
                font_size='16sp',
                font_name='Chinese' if chinese_font_available else None
            )
            cancel_btn.bind(on_press=lambda x: popup.dismiss())
            content.add_widget(cancel_btn)
            
            popup = Popup(
                title='上传激活码文件',
                content=content,
                size_hint=(0.8, 0.6)
            )
            
            popup.open()
            
        except Exception as e:
            self.show_message('错误', f'打开上传界面失败：{str(e)}')
    
    def select_code_file(self, days: str, parent_popup):
        """选择激活码文件"""
        try:
            parent_popup.dismiss()
            
            # 获取存储根目录
            if platform == 'android':
                try:
                    from android.storage import primary_external_storage_path
                    root_path = primary_external_storage_path()
                except ImportError:
                    # Android存储路径选项
                    android_paths = [
                        '/storage/emulated/0',  # 主要外部存储
                        '/sdcard',              # 传统路径
                        '/storage/self/primary', # 新版Android
                        '/mnt/sdcard'           # 备选路径
                    ]
                    root_path = '/storage/emulated/0'  # 默认使用主要外部存储
                    for path in android_paths:
                        if os.path.exists(path):
                            root_path = path
                            break
            else:
                # 桌面测试时使用当前data目录的上级目录，方便测试
                root_path = os.path.dirname(self.base_dir)
            
            # 创建文件选择弹窗
            content = BoxLayout(orientation='vertical', spacing=5)
            
            # 路径导航栏
            nav_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            
            # 返回上级目录按钮
            up_btn = Button(
                text='↑ 上级',
                size_hint_x=None,
                width=80,
                font_size='14sp',
                font_name='Chinese' if chinese_font_available else None
            )
            nav_layout.add_widget(up_btn)
            
            # 快速路径按钮
            quick_paths = []
            if platform == 'android':
                quick_paths = [
                    ('根目录', '/storage/emulated/0'),
                    ('下载', '/storage/emulated/0/Download'),
                    ('文档', '/storage/emulated/0/Documents')
                ]
            else:
                # 桌面测试快速路径
                quick_paths = [
                    ('数据', self.base_dir),
                    ('桌面', os.path.join(os.path.expanduser('~'), 'Desktop')),
                    ('文档', os.path.join(os.path.expanduser('~'), 'Documents'))
                ]
            
            for name, path in quick_paths:
                if os.path.exists(path):
                    quick_btn = Button(
                        text=name,
                        size_hint_x=None,
                        width=60,
                        font_size='12sp',
                        font_name='Chinese' if chinese_font_available else None
                    )
                    quick_btn.bind(on_press=lambda x, p=path: setattr(filechooser, 'path', p))
                    nav_layout.add_widget(quick_btn)
            
            content.add_widget(nav_layout)
            
            # 当前路径显示
            path_label = Label(
                text=f'当前路径: {root_path}',
                size_hint_y=None,
                height=35,
                font_size='13sp',
                font_name='Chinese' if chinese_font_available else None,
                text_size=(None, None),
                halign='left',
                color=(0.3, 0.3, 0.3, 1)
            )
            path_label.bind(size=path_label.setter('text_size'))
            content.add_widget(path_label)
            
            # 文件选择器
            filechooser = FileChooserListView(
                path=root_path,
                filters=['*.txt'],
                dirselect=False,  # 只能选择文件
                show_hidden=False  # 不显示隐藏文件
            )
            content.add_widget(filechooser)
            
            # 返回上级目录功能
            def go_up(instance):
                current_path = filechooser.path
                parent_path = os.path.dirname(current_path)
                if parent_path != current_path:  # 确保不是根目录
                    filechooser.path = parent_path
            
            up_btn.bind(on_press=go_up)
            
            # 更新路径显示
            def update_path_label(instance, path):
                path_label.text = f'当前路径: {path}'
            
            def update_selection_label(instance, selection):
                if selection:
                    filename = os.path.basename(selection[0])
                    path_label.text = f'选中文件: {filename}'
                else:
                    path_label.text = f'当前路径: {filechooser.path}'
            
            filechooser.bind(path=update_path_label)
            filechooser.bind(selection=update_selection_label)
            
            button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
            
            select_btn = Button(
                text='选择此文件',
                font_name='Chinese' if chinese_font_available else None
            )
            cancel_btn = Button(
                text='取消',
                font_name='Chinese' if chinese_font_available else None
            )
            
            button_layout.add_widget(select_btn)
            button_layout.add_widget(cancel_btn)
            content.add_widget(button_layout)
            
            popup = Popup(
                title=f'选择{days}天激活码文件',
                content=content,
                size_hint=(0.95, 0.9)
            )
            
            def select_file(btn):
                if filechooser.selection:
                    file_path = filechooser.selection[0]
                    self.upload_code_file(days, file_path)
                    popup.dismiss()
                else:
                    self.show_message('提示', '请选择一个文件')
            
            def cancel(btn):
                popup.dismiss()
            
            select_btn.bind(on_press=select_file)
            cancel_btn.bind(on_press=cancel)
            
            popup.open()
            
        except Exception as e:
            self.show_message('错误', f'选择文件失败：{str(e)}')
    
    def upload_code_file(self, days: str, file_path: str):
        """上传并验证激活码文件"""
        try:
            # 验证文件是否存在
            if not os.path.exists(file_path):
                self.show_message('错误', '选择的文件不存在')
                return
            
            # 验证文件内容
            test_codes = []
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if (line and 
                    not line.startswith('#') and 
                    self.is_valid_code(line)):
                    test_codes.append(line)
            
            if len(test_codes) < 5:
                self.show_message('警告', f'文件中只找到{len(test_codes)}个有效激活码，建议至少5个')
                return
            
            # 保存文件路径
            self.code_file_paths[days] = file_path
            self.save_code_file_paths()
            
            # 显示成功信息
            filename = os.path.basename(file_path)
            self.show_message('成功', f'已上传{days}天激活码文件:\n{filename}\n找到{len(test_codes)}个有效激活码')
            self.update_status(f'已上传{days}天激活码文件（{len(test_codes)}个）')
            
        except Exception as e:
            self.show_message('错误', f'上传文件失败：{str(e)}')
    
    
    def on_copy(self, instance):
        """复制内容到剪贴板（标记激活码为已使用）"""
        try:
            content = self.text_input.text
            if not content.strip():
                self.show_message('提示', '没有内容可复制')
                return
            
            # 根据复制上下文进行文本处理
            if self.copy_context == 'bulk':
                # 散装模式：保持原有格式
                processed_content = content
                # 标记散装激活码为已使用
                self.codes_used['bulk'] = True
                self.update_status('内容已复制到剪贴板（散装激活码已消耗）')
            else:
                # 单个模式：规范化空行
                processed_content = self.normalize_text_for_paste(content)
                # 检查并标记对应天数的激活码为已使用
                for days in ['30', '90', '365']:
                    if f'{days}天激活码：' in content:
                        self.codes_used[days] = True
                        self.update_status(f'内容已复制到剪贴板（{days}天激活码已消耗）')
                        break
                else:
                    self.update_status('内容已复制到剪贴板')
            
            Clipboard.copy(processed_content)
            
        except Exception as e:
            self.show_message('错误', f'复制失败：{str(e)}')
    
    def normalize_text_for_paste(self, text: str) -> str:
        """规范化文本中的空行"""
        import re
        # 将多个连续空行合并为单个空行
        normalized = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        return normalized.strip()
    
    def on_upload(self, instance):
        """统一上传按钮 - 显示上传类型选择"""
        try:
            # 创建深色主题的上传类型选择弹窗
            content = BoxLayout(orientation='vertical', padding=25, spacing=15)
            
            # 设置深色背景
            with content.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(0.05, 0.05, 0.1, 1)  # 深蓝黑背景，与主界面一致
                content.bg_rect = Rectangle(size=content.size, pos=content.pos)
            content.bind(size=lambda instance, size: setattr(content.bg_rect, 'size', size))
            content.bind(pos=lambda instance, pos: setattr(content.bg_rect, 'pos', pos))
            
            title_label = Label(
                text='选择要上传的文件类型',
                font_name='Chinese',
                font_size='20sp',
                size_hint_y=None,
                height='55dp',
                color=(0.9, 0.9, 0.9, 1)  # 浅色文字
            )
            content.add_widget(title_label)
            
            # 创建5个按钮的布局
            button_layout = BoxLayout(orientation='vertical', spacing=12)
            
            # 模板按钮 - 蓝色系，与主界面一致
            template_btn = Button(
                text='📄 模板文件',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='52dp',
                background_color=(0.2, 0.5, 0.8, 1),
                background_normal=''
            )
            template_btn.bind(on_press=lambda x: self._upload_template_file(popup))
            button_layout.add_widget(template_btn)
            
            # 1天激活码按钮 - 绿色系
            code1_btn = Button(
                text='🎯 1天激活码',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='52dp',
                background_color=(0.2, 0.7, 0.3, 1),
                background_normal=''
            )
            code1_btn.bind(on_press=lambda x: self._upload_activation_codes('1', popup))
            button_layout.add_widget(code1_btn)
            
            # 30天激活码按钮 - 橙色系
            code30_btn = Button(
                text='🎯 30天激活码',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='52dp',
                background_color=(0.8, 0.5, 0.2, 1),
                background_normal=''
            )
            code30_btn.bind(on_press=lambda x: self._upload_activation_codes('30', popup))
            button_layout.add_widget(code30_btn)
            
            # 90天激活码按钮 - 紫色系
            code90_btn = Button(
                text='🎯 90天激活码',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='52dp',
                background_color=(0.7, 0.3, 0.7, 1),
                background_normal=''
            )
            code90_btn.bind(on_press=lambda x: self._upload_activation_codes('90', popup))
            button_layout.add_widget(code90_btn)
            
            # 365天激活码按钮 - 红色系
            code365_btn = Button(
                text='🎯 365天激活码',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='52dp',
                background_color=(0.8, 0.3, 0.3, 1),
                background_normal=''
            )
            code365_btn.bind(on_press=lambda x: self._upload_activation_codes('365', popup))
            button_layout.add_widget(code365_btn)
            
            content.add_widget(button_layout)
            
            # 取消按钮 - 深灰色
            cancel_btn = Button(
                text='取消',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='48dp',
                background_color=(0.4, 0.4, 0.4, 1),
                background_normal=''
            )
            cancel_btn.bind(on_press=lambda x: popup.dismiss())
            content.add_widget(cancel_btn)
            
            popup = Popup(
                title='',  # 去掉默认标题
                content=content,
                size_hint=(0.85, 0.75),
                separator_color=(0.2, 0.2, 0.2, 1),  # 深色分割线
                title_size='0sp'  # 隐藏标题栏
            )
            
            popup.open()
            
        except Exception as e:
            self.show_message('错误', f'显示上传选项失败：{str(e)}')
    
    def _upload_template_file(self, parent_popup):
        """上传模板文件的具体实现"""
        parent_popup.dismiss()
        # 调用原来的上传模板逻辑，但不需要再显示弹窗
        self._show_template_file_chooser()
    
    def _upload_activation_codes(self, days, parent_popup):
        """上传激活码文件的具体实现"""
        parent_popup.dismiss()
        # 调用原来的上传激活码逻辑
        self._show_activation_code_file_chooser(days)

    def _show_template_file_chooser(self):
        """显示模板文件选择器"""
        try:
            # 创建文件选择弹窗
            content = BoxLayout(orientation='vertical', padding=20, spacing=15)
            
            title_label = Label(
                text='选择模板文件 (txt格式)',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='40dp'
            )
            content.add_widget(title_label)
            
            # 文件选择器
            if platform == 'android':
                # Android的主要外部存储路径
                initial_path = '/storage/emulated/0/'
            else:
                # 桌面环境使用用户主目录
                initial_path = os.path.expanduser('~')
            
            # 创建文件选择器
            filechooser = FileChooserListView(
                path=initial_path,
                filters=['*.txt'],
                size_hint=(1, 0.7)
            )
            content.add_widget(filechooser)
            
            # 导航按钮布局
            nav_layout = GridLayout(cols=4, spacing=5, size_hint_y=None, height='40dp')
            
            # 上一级按钮
            up_btn = Button(text='上一级', font_name='Chinese')
            def go_up(instance):
                parent_path = os.path.dirname(filechooser.path)
                if parent_path != filechooser.path:
                    filechooser.path = parent_path
            up_btn.bind(on_press=go_up)
            nav_layout.add_widget(up_btn)
            
            # 根目录按钮
            root_btn = Button(text='根目录', font_name='Chinese')
            def go_root(instance):
                if platform == 'android':
                    filechooser.path = '/storage/emulated/0/'
                else:
                    filechooser.path = os.path.expanduser('~')
            root_btn.bind(on_press=go_root)
            nav_layout.add_widget(root_btn)
            
            # Download目录按钮（Android）
            if platform == 'android':
                download_btn = Button(text='下载', font_name='Chinese')
                def go_download(instance):
                    download_path = '/storage/emulated/0/Download'
                    if os.path.exists(download_path):
                        filechooser.path = download_path
                download_btn.bind(on_press=go_download)
                nav_layout.add_widget(download_btn)
                
                # Documents目录按钮
                docs_btn = Button(text='文档', font_name='Chinese')
                def go_docs(instance):
                    docs_path = '/storage/emulated/0/Documents'
                    if os.path.exists(docs_path):
                        filechooser.path = docs_path
                docs_btn.bind(on_press=go_docs)
                nav_layout.add_widget(docs_btn)
            else:
                # 桌面环境的额外按钮
                nav_layout.add_widget(Label())  # 占位
                nav_layout.add_widget(Label())  # 占位
            
            content.add_widget(nav_layout)
            
            # 按钮布局
            button_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='50dp')
            
            # 确认按钮
            def upload_template_file(instance):
                if filechooser.selection:
                    file_path = filechooser.selection[0]
                    if file_path.lower().endswith('.txt'):
                        try:
                            # 读取模板文件内容
                            with open(file_path, 'r', encoding='utf-8') as f:
                                template_content = f.read().strip()
                            
                            if template_content:
                                # 保存模板文件路径
                                template_path = os.path.join(self.base_dir, 'sendGoodsMode.txt')
                                with open(template_path, 'w', encoding='utf-8') as f:
                                    f.write(template_content)
                                
                                # 更新当前显示内容
                                self.text_input.text = template_content
                                self.current_content = template_content
                                
                                popup.dismiss()
                                self.update_status(f'✅ 已上传自定义模板：{os.path.basename(file_path)}')
                            else:
                                self.show_message('错误', '模板文件内容为空')
                        except Exception as e:
                            self.show_message('错误', f'读取模板文件失败：{str(e)}')
                    else:
                        self.show_message('错误', '请选择txt格式的文件')
                else:
                    self.show_message('提示', '请选择一个文件')
            
            confirm_btn = Button(
                text='确认上传',
                font_name='Chinese',
                background_color=(0.2, 0.8, 0.2, 1)
            )
            confirm_btn.bind(on_press=upload_template_file)
            button_layout.add_widget(confirm_btn)
            
            # 取消按钮
            cancel_btn = Button(
                text='取消',
                font_name='Chinese',
                background_color=(0.8, 0.2, 0.2, 1)
            )
            cancel_btn.bind(on_press=lambda x: popup.dismiss())
            button_layout.add_widget(cancel_btn)
            
            content.add_widget(button_layout)
            
            popup = Popup(
                title='上传模板文件',
                content=content,
                size_hint=(0.9, 0.8)
            )
            
            popup.open()
            
        except Exception as e:
            self.show_message('错误', f'上传模板失败：{str(e)}')
    
    def _show_activation_code_file_chooser(self, days):
        """显示激活码文件选择器"""
        try:
            # 创建文件选择弹窗
            content = BoxLayout(orientation='vertical', padding=20, spacing=15)
            
            title_label = Label(
                text=f'选择{days}天激活码文件 (txt格式)',
                font_name='Chinese',
                font_size='16sp',
                size_hint_y=None,
                height='40dp'
            )
            content.add_widget(title_label)
            
            # 文件选择器
            if platform == 'android':
                # Android的主要外部存储路径
                initial_path = '/storage/emulated/0/'
            else:
                # 桌面环境使用用户主目录
                initial_path = os.path.expanduser('~')
            
            # 创建文件选择器
            filechooser = FileChooserListView(
                path=initial_path,
                filters=['*.txt'],
                size_hint=(1, 0.7)
            )
            content.add_widget(filechooser)
            
            # 导航按钮布局
            nav_layout = GridLayout(cols=4, spacing=5, size_hint_y=None, height='40dp')
            
            # 上一级按钮
            up_btn = Button(text='上一级', font_name='Chinese')
            def go_up(instance):
                parent_path = os.path.dirname(filechooser.path)
                if parent_path != filechooser.path:
                    filechooser.path = parent_path
            up_btn.bind(on_press=go_up)
            nav_layout.add_widget(up_btn)
            
            # 根目录按钮
            root_btn = Button(text='根目录', font_name='Chinese')
            def go_root(instance):
                if platform == 'android':
                    filechooser.path = '/storage/emulated/0/'
                else:
                    filechooser.path = os.path.expanduser('~')
            root_btn.bind(on_press=go_root)
            nav_layout.add_widget(root_btn)
            
            # Download目录按钮（Android）
            if platform == 'android':
                download_btn = Button(text='下载', font_name='Chinese')
                def go_download(instance):
                    download_path = '/storage/emulated/0/Download'
                    if os.path.exists(download_path):
                        filechooser.path = download_path
                download_btn.bind(on_press=go_download)
                nav_layout.add_widget(download_btn)
                
                # Documents目录按钮
                docs_btn = Button(text='文档', font_name='Chinese')
                def go_docs(instance):
                    docs_path = '/storage/emulated/0/Documents'
                    if os.path.exists(docs_path):
                        filechooser.path = docs_path
                docs_btn.bind(on_press=go_docs)
                nav_layout.add_widget(docs_btn)
            else:
                # 桌面环境的额外按钮
                nav_layout.add_widget(Label())  # 占位
                nav_layout.add_widget(Label())  # 占位
            
            content.add_widget(nav_layout)
            
            # 按钮布局
            button_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='50dp')
            
            # 确认按钮
            def upload_activation_codes_file(instance):
                if filechooser.selection:
                    file_path = filechooser.selection[0]
                    if file_path.lower().endswith('.txt'):
                        try:
                            # 验证文件内容
                            test_codes = []
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            
                            for line in lines:
                                line = line.strip()
                                if (line and 
                                    not line.startswith('#') and 
                                    self.is_valid_code(line)):
                                    test_codes.append(line)
                            
                            if len(test_codes) < 5:
                                self.show_message('警告', f'文件中只找到{len(test_codes)}个有效激活码，建议至少5个')
                                return
                            
                            # 保存文件路径
                            self.code_file_paths[days] = file_path
                            self.save_code_paths()
                            
                            # 显示成功信息
                            filename = os.path.basename(file_path)
                            popup.dismiss()
                            self.show_message('成功', f'已上传{days}天激活码文件:\n{filename}\n找到{len(test_codes)}个有效激活码')
                            self.update_status(f'已上传{days}天激活码文件（{len(test_codes)}个）')
                            
                        except Exception as e:
                            self.show_message('错误', f'读取激活码文件失败：{str(e)}')
                    else:
                        self.show_message('错误', '请选择txt格式的文件')
                else:
                    self.show_message('提示', '请选择一个文件')
            
            confirm_btn = Button(
                text='确认上传',
                font_name='Chinese',
                background_color=(0.2, 0.8, 0.2, 1)
            )
            confirm_btn.bind(on_press=upload_activation_codes_file)
            button_layout.add_widget(confirm_btn)
            
            # 取消按钮
            cancel_btn = Button(
                text='取消',
                font_name='Chinese',
                background_color=(0.8, 0.2, 0.2, 1)
            )
            cancel_btn.bind(on_press=lambda x: popup.dismiss())
            button_layout.add_widget(cancel_btn)
            
            content.add_widget(button_layout)
            
            popup = Popup(
                title=f'上传{days}天激活码文件',
                content=content,
                size_hint=(0.9, 0.8)
            )
            
            popup.open()
            
        except Exception as e:
            self.show_message('错误', f'上传{days}天激活码失败：{str(e)}')
    
    def on_edit(self, instance):
        """编辑按钮 - 简单的编辑/保存切换"""
        try:
            if not self.is_editing:
                # 启用编辑模式
                self.is_editing = True
                
                # 聚焦到文本输入框
                self.text_input.focus = True
                
                # 将光标移动到文本末尾
                if self.text_input.text:
                    self.text_input.cursor = (len(self.text_input.text), 0)
                
                # 更新按钮文本和颜色
                instance.text = '💾 保存'
                instance.background_color = (0.2, 0.8, 0.4, 1)  # 绿色
                
                self.update_status('✏️ 编辑模式已启用，再次点击保存')
                
            else:
                # 保存编辑
                self.is_editing = False
                
                # 手动保存草稿
                self.save_draft()
                
                # 移除焦点
                self.text_input.focus = False
                
                # 恢复按钮文本和颜色
                instance.text = '✏️ 编辑'
                instance.background_color = (0.8, 0.6, 0.2, 1)  # 橙色
                
                self.update_status('💾 内容已保存')
                
        except Exception as e:
            self.show_message('错误', f'编辑操作失败：{str(e)}')


if __name__ == '__main__':
    ShippingApp().run()
