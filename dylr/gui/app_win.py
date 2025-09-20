# coding=utf-8
"""
:author: Lyzen
:date: 2023.01.17
:brief: 主窗口
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog, messagebox
import platform

from dylr.gui import grip_frame
from dylr.core import version, record_manager, app, add_room_manager


class ApplicationWin(ttk.Frame):
    def __init__(self):
        app.win = self
        ttk.Frame.__init__(self, None, border=2)
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_styles()
        self.init_win()
        self.reload_all()
        self.mainloop()

    def setup_styles(self):
        """设置现代化的GUI样式"""
        style = ttk.Style()
        
        # 设置主题
        try:
            style.theme_use('clam')  # 使用clam主题，在所有平台上都可用
        except:
            pass
        
        # 配置按钮样式
        style.configure('Modern.TButton',
                       padding=(20, 10),
                       font=('Arial', 12))
        
        # 配置标签框样式
        style.configure('Modern.TLabelframe',
                       borderwidth=2,
                       relief='solid')
        
        style.configure('Modern.TLabelframe.Label',
                       font=('Arial', 14, 'bold'),
                       foreground='#2c3e50')

    def get_system_font(self):
        """根据操作系统返回合适的字体"""
        system = platform.system()
        if system == 'Darwin':  # macOS
            return ('SF Pro Display', 14)
        elif system == 'Windows':
            return ('Microsoft YaHei', 14)
        else:  # Linux
            return ('DejaVu Sans', 14)

    def init_win(self):
        """ 初始化窗口 """
        self.topwin = self.winfo_toplevel()
        self.topwin.title(f'🎬 抖音直播录制工具 v{version} by Lyzen')
        self.topwin.protocol('WM_DELETE_WINDOW', self.on_close)
        self.topwin.configure(bg='#f8f9fa')
        
        # 设置窗口大小
        self.topwin.geometry('1000x600')
        self.topwin.minsize(900, 500)
        
        # 主容器
        main_container = tk.Frame(self, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部标题区域
        title_frame = tk.Frame(main_container, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text='📺 抖音直播录制管理器', 
                              font=self.get_system_font(),
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame,
                                 text='自动监测直播状态，一键录制高质量视频',
                                 font=('Arial', 10),
                                 fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()

        # 底部按钮区域
        footer_frame = tk.Frame(main_container, bg='#f8f9fa', height=80)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        button_frame = tk.Frame(footer_frame, bg='#f8f9fa')
        button_frame.pack(expand=True)
        
        add_room_btn = ttk.Button(button_frame, 
                                 text='➕ 添加主播', 
                                 style='Modern.TButton',
                                 command=self._request_add_room)
        add_room_btn.grid(row=0, column=0, padx=10, pady=10)
        
        refresh_btn = ttk.Button(button_frame,
                               text='🔄 刷新列表',
                               style='Modern.TButton', 
                               command=self.reload_all)
        refresh_btn.grid(row=0, column=1, padx=10, pady=10)
        
        info_label = tk.Label(button_frame, 
                             text='💡 提示：双击表格中的"是"或"否"可以快速修改设置',
                             font=('Arial', 10),
                             fg='#7f8c8d', bg='#f8f9fa')
        info_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # 主内容区域 - 可滚动的房间列表
        content_frame = tk.Frame(main_container, bg='#ffffff', relief='solid', borderwidth=1)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Canvas和Scrollbar
        canvas = tk.Canvas(content_frame, bg='#ffffff', highlightthickness=0)
        room_list_frame = tk.Frame(canvas, bg='#ffffff')
        
        # 样式化的滚动条
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=room_list_frame, anchor="nw")
        
        # 绑定滚动事件
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        room_list_frame.bind("<Configure>", configure_scroll_region)
        
        # 鼠标滚轮绑定
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux

        self.grip_frame = grip_frame.GripFrame(room_list_frame)
        self.grip_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def reload_all(self):
        self.grip_frame.remove_all()
        for room in record_manager.get_rooms():
            self.grip_frame.append(room.room_id, room.room_name, '未直播' if room.auto_record else '未监测',
                                   room.auto_record, room.record_danmu, room.important)

    def set_state(self, room, text, color='#000000'):
        self.grip_frame.set(room.room_id, text, color)

    def add_room(self, room):
        self.grip_frame.append(room.room_id, room.room_name, '未直播' if room.auto_record else '未监测',
                               room.auto_record, room.record_danmu, room.important)

    def remove_room(self, web_rid):
        self.grip_frame.remove(web_rid)

    def _request_add_room(self):
        res = simpledialog.askstring(
            title='📺 添加主播', 
            prompt='请输入房间地址，支持以下格式：\n\n'
                   '🔹 房间ID：123456\n'
                   '🔹 直播间地址：https://live.douyin.com/123456\n'
                   '🔹 分享短链：https://v.douyin.com/AbCDef\n\n'
                   '💡 提示：分享短链最稳定，可在手机端直播间点击分享获取'
        )
        if res:
            add_room_manager.try_add_room(res)

    def on_close(self):
        if messagebox.askokcancel("🚪 关闭程序", "确定要关闭抖音直播录制工具吗？"):
            self.quit()
