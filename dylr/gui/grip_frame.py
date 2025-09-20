# coding=utf-8
"""
:author: Lyzen
:date: 2023.01.17
:brief: GUI中显示主播信息的网格布局
"""

import os
import subprocess
import sys
import tkinter as tk
import platform
from tkinter import messagebox
from functools import partial
from tkinter import ttk

from dylr.core import record_manager, config, monitor


class GripFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='📋 直播间录制列表', padding=15, style='Modern.TLabelframe')
        
        # 定义列宽
        self.column_widths = [120, 150, 120, 80, 80, 80, 150]
        
        # 创建表格头部
        self.create_header()
        
        # 配置列权重，让表格能正确对齐
        for i, width in enumerate(self.column_widths):
            self.grid_columnconfigure(i, minsize=width, weight=0)
        
        self._index = 0
        self.widgets = {}

    def get_system_font(self):
        """根据操作系统返回合适的字体"""
        system = platform.system()
        if system == 'Darwin':  # macOS
            return ('SF Pro Display', 12)
        elif system == 'Windows':
            return ('Microsoft YaHei', 12)
        else:  # Linux
            return ('DejaVu Sans', 12)

    def create_header(self):
        """创建表格头部"""
        headers = [
            ('🆔', '房间ID'),
            ('👤', '主播名'), 
            ('📡', '录制状态'),
            ('🎯', '监测直播'),
            ('💬', '录制弹幕'),
            ('⭐', '重要主播'),
            ('🛠️', '操作')
        ]
        
        for i, (icon, text) in enumerate(headers):
            header_frame = tk.Frame(self, bg='#34495e', width=self.column_widths[i], height=50)
            header_frame.grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
            header_frame.grid_propagate(False)
            
            # 图标
            icon_label = tk.Label(header_frame, text=icon, 
                                 bg='#34495e', fg='white', 
                                 font=('Arial', 12))
            icon_label.pack(pady=(5, 0))
            
            # 文字
            text_label = tk.Label(header_frame, text=text,
                                 bg='#34495e', fg='white',
                                 font=self.get_system_font())
            text_label.pack(pady=(0, 5))

    def append(self, web_rid, name, state, auto_record, record_danmu, important):
        self._index += 1
        
        # 行背景色交替
        row_bg = '#f8f9fa' if self._index % 2 == 0 else '#ffffff'
        
        # 创建每列的Frame来确保对齐
        cells = []
        
        # 房间ID
        cell1 = tk.Frame(self, bg=row_bg, width=self.column_widths[0], height=35)
        cell1.grid(row=self._index, column=0, sticky='nsew', padx=1, pady=1)
        cell1.grid_propagate(False)
        label1 = tk.Label(cell1, text=str(web_rid), bg=row_bg, fg='#2c3e50',
                         font=self.get_system_font(), anchor='center')
        label1.pack(expand=True)
        cells.append(cell1)

        # 主播名
        cell2 = tk.Frame(self, bg=row_bg, width=self.column_widths[1], height=35)
        cell2.grid(row=self._index, column=1, sticky='nsew', padx=1, pady=1)
        cell2.grid_propagate(False)
        label2 = tk.Label(cell2, text=str(name), bg=row_bg, fg='#2c3e50',
                         font=self.get_system_font() + ('bold',), anchor='center')
        label2.pack(expand=True)
        cells.append(cell2)

        # 录制状态
        cell3 = tk.Frame(self, bg=row_bg, width=self.column_widths[2], height=35)
        cell3.grid(row=self._index, column=2, sticky='nsew', padx=1, pady=1)
        cell3.grid_propagate(False)
        state_color = self._get_state_color(state)
        label3 = tk.Label(cell3, text=str(state), bg=row_bg, fg=state_color,
                         font=self.get_system_font() + ('bold',), anchor='center')
        label3.pack(expand=True)
        cells.append(cell3)

        # 监测直播
        cell4 = tk.Frame(self, bg=row_bg, width=self.column_widths[3], height=35)
        cell4.grid(row=self._index, column=3, sticky='nsew', padx=1, pady=1)
        cell4.grid_propagate(False)
        auto_text = '✅ 是' if auto_record else '❌ 否'
        fg_color = '#27ae60' if auto_record else '#e74c3c'
        label4 = tk.Label(cell4, text=auto_text, bg=row_bg, fg=fg_color,
                         font=self.get_system_font(), cursor='hand2', anchor='center')
        label4.pack(expand=True)
        label4.bind('<Double-Button-1>', func=partial(self._set_auto_record, web_rid))
        label4.bind('<Enter>', lambda e: cell4.config(bg='#e8f4fd'))
        label4.bind('<Leave>', lambda e: cell4.config(bg=row_bg))
        cells.append(cell4)

        # 录制弹幕
        cell5 = tk.Frame(self, bg=row_bg, width=self.column_widths[4], height=35)
        cell5.grid(row=self._index, column=4, sticky='nsew', padx=1, pady=1)
        cell5.grid_propagate(False)
        danmu_text = '✅ 是' if record_danmu else '❌ 否'
        fg_color = '#27ae60' if record_danmu else '#e74c3c'
        label5 = tk.Label(cell5, text=danmu_text, bg=row_bg, fg=fg_color,
                         font=self.get_system_font(), cursor='hand2', anchor='center')
        label5.pack(expand=True)
        label5.bind('<Double-Button-1>', func=partial(self._set_record_danmu, web_rid))
        label5.bind('<Enter>', lambda e: cell5.config(bg='#e8f4fd'))
        label5.bind('<Leave>', lambda e: cell5.config(bg=row_bg))
        cells.append(cell5)

        # 重要主播
        cell6 = tk.Frame(self, bg=row_bg, width=self.column_widths[5], height=35)
        cell6.grid(row=self._index, column=5, sticky='nsew', padx=1, pady=1)
        cell6.grid_propagate(False)
        important_text = '⭐ 是' if important else '🔘 否'
        fg_color = '#27ae60' if important else '#e74c3c'
        label6 = tk.Label(cell6, text=important_text, bg=row_bg, fg=fg_color,
                         font=self.get_system_font(), cursor='hand2', anchor='center')
        label6.pack(expand=True)
        label6.bind('<Double-Button-1>', func=partial(self._set_important, web_rid))
        label6.bind('<Enter>', lambda e: cell6.config(bg='#fff3cd'))
        label6.bind('<Leave>', lambda e: cell6.config(bg=row_bg))
        cells.append(cell6)

        # 操作按钮
        cell7 = tk.Frame(self, bg=row_bg, width=self.column_widths[6], height=35)
        cell7.grid(row=self._index, column=6, sticky='nsew', padx=1, pady=1)
        cell7.grid_propagate(False)
        
        btn_container = tk.Frame(cell7, bg=row_bg)
        btn_container.pack(expand=True)
        
        open_btn = tk.Button(btn_container, text='📁', 
                           bg='#17a2b8', fg='white',
                           font=('Arial', 10), width=3,
                           relief='flat', 
                           command=partial(self._open_explorer, 'download/' + name))
        open_btn.pack(side=tk.LEFT, padx=2)
        open_btn.bind('<Enter>', lambda e: open_btn.config(bg='#138496'))
        open_btn.bind('<Leave>', lambda e: open_btn.config(bg='#17a2b8'))
        
        remove_btn = tk.Button(btn_container, text='🗑️',
                             bg='#dc3545', fg='white', 
                             font=('Arial', 10), width=3,
                             relief='flat',
                             command=partial(self.request_remove, web_rid, name))
        remove_btn.pack(side=tk.LEFT, padx=2)
        remove_btn.bind('<Enter>', lambda e: remove_btn.config(bg='#c82333'))
        remove_btn.bind('<Leave>', lambda e: remove_btn.config(bg='#dc3545'))
        
        cells.append(cell7)
        
        # 保存引用，用于后续更新 - 现在保存的是label而不是cell
        self.widgets[web_rid] = [label1, label2, label3, label4, label5, label6, cells]

    def remove_all(self):
        for i in self.widgets.keys():
            self.remove(i)

    def remove(self, web_rid):
        if web_rid in self.widgets:
            # widgets[web_rid][6] 是包含所有cell的列表
            cells = self.widgets[web_rid][6] 
            for cell in cells:
                cell.grid_remove()
            del self.widgets[web_rid]

    def set(self, web_rid, text, color):
        if web_rid in self.widgets:
            # 更新录制状态列 (index 2)
            self.widgets[web_rid][2].config(text=text, fg=color)

    def request_remove(self, web_rid, name):
        """ 询问是否删除，避免误删 """
        res = messagebox.askokcancel('删除房间', f'确定要删除房间{name}({web_rid})吗？\n如果不想监测和录制可以将其设为不自动录制。')
        if not res:
            return
        self.remove(web_rid)
        room = record_manager.get_room(web_rid)
        if room is None:
            return
        record_manager.rooms.remove(room)
        config.save_rooms()
        recording = record_manager.get_recording(room)
        if recording is not None:
            recording.stop()

    def _set_auto_record(self, web_rid, event):
        room = record_manager.get_room(web_rid)
        if room is None:
            return
        room.auto_record = not room.auto_record
        if web_rid in self.widgets:
            auto_text = '✅ 是' if room.auto_record else '❌ 否'
            fg_color = '#27ae60' if room.auto_record else '#e74c3c'
            self.widgets[web_rid][3].config(text=auto_text, fg=fg_color)
        config.save_rooms()

    def _set_record_danmu(self, web_rid, event):
        room = record_manager.get_room(web_rid)
        if room is None:
            return
        room.record_danmu = not room.record_danmu
        if web_rid in self.widgets:
            danmu_text = '✅ 是' if room.record_danmu else '❌ 否'
            fg_color = '#27ae60' if room.record_danmu else '#e74c3c'
            self.widgets[web_rid][4].config(text=danmu_text, fg=fg_color)
        config.save_rooms()

    def _set_important(self, web_rid, event):
        room = record_manager.get_room(web_rid)
        if room is None:
            return
        room.important = not room.important
        if web_rid in self.widgets:
            important_text = '⭐ 是' if room.important else '🔘 否'
            fg_color = '#27ae60' if room.important else '#e74c3c'
            self.widgets[web_rid][5].config(text=important_text, fg=fg_color)
        config.save_rooms()

        if room.important and str(web_rid) not in monitor.important_room_threads:
            monitor.start_important_monitor_thread(room)

    def _get_state_color(self, state):
        """根据状态返回颜色"""
        state_lower = str(state).lower()
        if '录制' in state_lower or 'recording' in state_lower:
            return '#e74c3c'  # 红色
        elif '直播' in state_lower or 'live' in state_lower:
            return '#f39c12'  # 橙色
        elif '未直播' in state_lower or '未监测' in state_lower:
            return '#95a5a6'  # 灰色
        else:
            return '#2c3e50'  # 默认深色

    def _open_explorer(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.call(["open", path])
            elif sys.platform == 'linux':
                subprocess.call(["xdg-open", path])
            elif sys.platform == 'win32':  # Windows
                os.startfile(path.replace('/', '\\'))
            else:
                # 其他系统，尝试用默认程序打开
                subprocess.call(["xdg-open", path])
        except Exception as e:
            print(f"打开目录失败: {e}")
