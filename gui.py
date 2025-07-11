#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SpaceTransForMac GUI界面

提供一个简单的图形界面，用于查看和修改配置
"""

import os
import json
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
from config_manager import load_config, get_config_path, DEFAULT_CONFIG

class ConfigGUI:
    """
    配置GUI类 - 提供图形界面查看和修改配置
    """
    def __init__(self, root):
        self.root = root
        self.root.title("SpaceTransForMac 配置")
        self.root.geometry("600x650")
        self.root.resizable(True, True)
        
        # 加载配置
        self.config = load_config()
        self.config_path = get_config_path()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """
        创建GUI组件
        """
        # 顶部标题
        title_frame = tk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(title_frame, text="SpaceTransForMac 配置", font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # 配置文件路径
        path_frame = tk.Frame(self.root)
        path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        path_label = tk.Label(path_frame, text=f"配置文件路径: {self.config_path}", font=("Arial", 10))
        path_label.pack(side=tk.LEFT)
        
        # 创建配置输入区域
        config_frame = tk.Frame(self.root)
        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建配置项
        self.config_entries = {}
        row = 0
        
        # API密钥
        tk.Label(config_frame, text="API密钥 (必填):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_entries["API_KEY"] = tk.Entry(config_frame, width=50)
        self.config_entries["API_KEY"].grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.config_entries["API_KEY"].insert(0, self.config.get("API_KEY", ""))
        row += 1
        
        # API HOST
        tk.Label(config_frame, text="API HOST:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_entries["API_HOST"] = tk.Entry(config_frame, width=50)
        self.config_entries["API_HOST"].grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.config_entries["API_HOST"].insert(0, self.config.get("API_HOST", DEFAULT_CONFIG["API_HOST"]))
        row += 1
        
        # 模型名称
        tk.Label(config_frame, text="模型名称:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_entries["MODEL"] = tk.Entry(config_frame, width=50)
        self.config_entries["MODEL"].grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.config_entries["MODEL"].insert(0, self.config.get("MODEL", DEFAULT_CONFIG["MODEL"]))
        row += 1
        
        # 空格超时时间
        tk.Label(config_frame, text="空格超时时间 (秒):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_entries["SPACE_TIMEOUT"] = tk.Entry(config_frame, width=50)
        self.config_entries["SPACE_TIMEOUT"].grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.config_entries["SPACE_TIMEOUT"].insert(0, str(self.config.get("SPACE_TIMEOUT", DEFAULT_CONFIG["SPACE_TIMEOUT"])))
        row += 1
        
        # 空格触发次数
        tk.Label(config_frame, text="空格触发次数:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_entries["SPACE_TRIGGER_COUNT"] = tk.Entry(config_frame, width=50)
        self.config_entries["SPACE_TRIGGER_COUNT"].grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.config_entries["SPACE_TRIGGER_COUNT"].insert(0, str(self.config.get("SPACE_TRIGGER_COUNT", DEFAULT_CONFIG["SPACE_TRIGGER_COUNT"])))
        row += 1
        
        # 温度
        tk.Label(config_frame, text="温度 (0-1):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_entries["TEMPERATURE"] = tk.Entry(config_frame, width=50)
        self.config_entries["TEMPERATURE"].grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.config_entries["TEMPERATURE"].insert(0, str(self.config.get("TEMPERATURE", DEFAULT_CONFIG["TEMPERATURE"])))
        row += 1
        
        # 系统提示词
        tk.Label(config_frame, text="系统提示词:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_entries["SYSTEM_PROMPT"] = scrolledtext.ScrolledText(config_frame, width=50, height=5)
        self.config_entries["SYSTEM_PROMPT"].grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        self.config_entries["SYSTEM_PROMPT"].insert(tk.END, self.config.get("SYSTEM_PROMPT", DEFAULT_CONFIG["SYSTEM_PROMPT"]))
        row += 1
        
        # 设置列权重，使其可以随窗口调整大小
        config_frame.columnconfigure(1, weight=1)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 保存按钮引用以便后续使用
        self.save_button = tk.Button(
            button_frame, 
            text="保存配置", 
            command=self.save_config, 
            width=15,
            cursor="hand2"
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = tk.Button(
            button_frame, 
            text="刷新配置", 
            command=self.refresh_config, 
            width=15,
            cursor="hand2"
        )
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        self.start_button = tk.Button(
            button_frame, 
            text="启动翻译程序", 
            command=self.start_translator, 
            width=15,
            cursor="hand2"
        )
        self.start_button.pack(side=tk.RIGHT, padx=5)
    
    def save_config(self):
        """
        保存配置到文件
        """
        # 获取所有配置项的值
        for key in self.config_entries:
            if key == "SYSTEM_PROMPT":
                self.config[key] = self.config_entries[key].get("1.0", tk.END).strip()
            else:
                self.config[key] = self.config_entries[key].get()
        
        # 转换数值类型
        try:
            self.config["SPACE_TIMEOUT"] = float(self.config["SPACE_TIMEOUT"])
            self.config["SPACE_TRIGGER_COUNT"] = int(self.config["SPACE_TRIGGER_COUNT"])
            self.config["TEMPERATURE"] = float(self.config["TEMPERATURE"])
        except ValueError as e:
            messagebox.showerror("错误", f"数值转换错误: {e}\n请确保数值字段输入正确的数字")
            return
        
        # 验证必填项
        if not self.config["API_KEY"].strip():
            messagebox.showerror("错误", "API密钥不能为空")
            return
        
        # 保存到文件
        try:
            config_dir = os.path.dirname(self.config_path)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            
            messagebox.showinfo("成功", f"配置已保存到 {self.config_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置文件出错: {e}")
    
    def refresh_config(self):
        """
        重新加载配置文件
        """
        try:
            self.config = load_config()
            
            # 更新界面
            for key in self.config_entries:
                if key in self.config:
                    if key == "SYSTEM_PROMPT":
                        self.config_entries[key].delete("1.0", tk.END)
                        self.config_entries[key].insert(tk.END, self.config[key])
                    else:
                        self.config_entries[key].delete(0, tk.END)
                        self.config_entries[key].insert(0, str(self.config[key]))
            
            messagebox.showinfo("成功", "配置已刷新")
        except Exception as e:
            messagebox.showerror("错误", f"刷新配置出错: {e}")
    
    def start_translator(self):
        """
        启动翻译程序
        """
        # 先保存配置
        self.save_config()
        
        try:
            # 导入main模块
            import main
            import threading
            
            # 移除旧的状态区域（如果存在）
            for widget in self.root.winfo_children():
                if hasattr(widget, 'status_container_tag'):
                    widget.destroy()
            
            # 禁用启动按钮
            self.start_button.config(state=tk.DISABLED, text="已经启动...")
            
            # 创建现代化的状态容器
            self.status_container = tk.Frame(self.root, bg='#f5f5f5')
            self.status_container.status_container_tag = True  # 添加标记
            self.status_container.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            # 状态卡片
            status_card = tk.Frame(
                self.status_container,
                bg='#ffffff',
                relief='flat',
                bd=0
            )
            status_card.pack(fill=tk.X, pady=5)
            
            # 添加阴影效果（通过多层Frame模拟）
            shadow_frame = tk.Frame(
                self.status_container,
                bg='#e0e0e0',
                height=2
            )
            shadow_frame.pack(fill=tk.X)
            
            # 状态内容区域
            content_frame = tk.Frame(status_card, bg='#ffffff', padx=25, pady=20)
            content_frame.pack(fill=tk.X)
            
            # 状态图标和文本容器
            status_info = tk.Frame(content_frame, bg='#ffffff')
            status_info.pack(fill=tk.X)
            
            # 状态图标
            self.status_icon = tk.Label(
                status_info,
                text="⏳",
                font=("Arial", 28),
                fg="#FF9800",
                bg='#ffffff'
            )
            self.status_icon.pack(side=tk.LEFT, padx=(0, 15))
            
            # 文本区域
            text_area = tk.Frame(status_info, bg='#ffffff')
            text_area.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 状态标题
            self.status_title = tk.Label(
                text_area,
                text="正在启动翻译程序",
                font=("SF Pro Display", 16, "bold"),
                fg="#1a1a1a",
                bg='#ffffff',
                anchor="w"
            )
            self.status_title.pack(fill=tk.X, pady=(0, 5))
            
            # 状态描述
            self.status_desc = tk.Label(
                text_area,
                text="正在初始化翻译服务，请稍候...",
                font=("SF Pro Display", 12),
                fg="#666666",
                bg='#ffffff',
                anchor="w",
                wraplength=400
            )
            self.status_desc.pack(fill=tk.X)
            
            # 按钮容器（初始隐藏）
            self.button_container = tk.Frame(content_frame, bg='#ffffff')
            
            # 更新GUI状态
            self.root.update()
            
            # 在单独的线程中启动翻译程序
            def run_translator():
                try:
                    # 启动翻译程序并保存实例
                    self.translator = main.main(from_gui=True)
                    print("翻译程序已在后台启动")
                    
                    # 在主线程中更新UI为成功状态
                    self.root.after(0, self.update_success_status)
                    
                except Exception as e:
                    error_msg = f"翻译程序启动失败: {e}"
                    print(error_msg)
                    
                    # 在主线程中显示错误状态
                    self.root.after(0, lambda: self.update_error_status(error_msg))
            
            # 启动线程
            translator_thread = threading.Thread(target=run_translator)
            translator_thread.daemon = True
            translator_thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动翻译程序失败: {e}")
    
    def stop_translator(self):
        """停止翻译程序"""
        if hasattr(self, 'translator') and self.translator:
            # 停止键盘监听器
            if hasattr(self.translator, 'keyboard_listener') and self.translator.keyboard_listener.is_alive():
                self.translator.keyboard_listener.stop()
            
            # 重置翻译器实例
            self.translator = None
            print("翻译程序已停止")
            return True
        return False
    
    def restart_translator(self):
        """重启翻译程序"""
        # 先停止当前运行的翻译程序
        self.stop_translator()
        
        # 清除状态容器
        for widget in self.root.winfo_children():
            if hasattr(widget, 'status_container_tag'):
                widget.destroy()
        
        # 重新启用启动按钮
        self.start_button.config(state=tk.NORMAL, text="启动翻译程序")
        
        # 重新启动翻译程序
        self.start_translator()
    
    def update_success_status(self):
        """更新为成功状态"""
        # 更新图标和颜色
        self.status_icon.config(text="🎉", fg="#4CAF50")
        
        # 更新标题
        self.status_title.config(
            text="启动成功！",
            fg="#4CAF50",
            font=("SF Pro Display", 16, "bold")
        )
        
        # 更新描述
        self.status_desc.config(
            text="现在您可以最小化此配置窗口，程序将继续在后台工作",
            font=("SF Pro Display", 12),
            fg="#666666"
        )
        
        # 更新启动按钮文本
        self.start_button.config(text="翻译程序已启动", state=tk.DISABLED)
        
        # 添加分隔线
        separator = tk.Frame(self.status_container, height=1, bg="#E0E0E0")
        separator.pack(fill=tk.X, pady=(15, 10))
        
        # 创建按钮容器
        button_container = tk.Frame(self.status_container)
        button_container.pack(fill=tk.X, pady=(0, 10))
        
        # 创建按钮样式
        button_style = {
            "font": ("SF Pro Display", 12, "bold"),
            "relief": "flat",
            "padx": 20,
            "pady": 12,
            "cursor": "hand2",
            "borderwidth": 0
        }
        
        # 创建重启按钮
        restart_button = tk.Button(
            button_container,
            text="🔄 重启翻译程序",
            command=self.restart_translator,
            bg="#FF9800",
            fg="black",
            activebackground="#F57C00",
            activeforeground="black",
            **button_style
        )
        restart_button.pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        
        # 创建关闭按钮
        close_button = tk.Button(
            button_container,
            text="✕ 关闭配置窗口",
            command=self.root.destroy,
            bg="#FF5722",
            fg="black",
            activebackground="#E64A19",
            activeforeground="black",
            **button_style
        )
        close_button.pack(side=tk.LEFT, padx=(5, 5), fill=tk.X, expand=True)
        
        # 创建最小化按钮
        minimize_button = tk.Button(
            button_container,
            text="⬇ 最小化到后台",
            command=self.root.iconify,
            bg="#2196F3",
            fg="black",
            activebackground="#1976D2",
            activeforeground="black",
            **button_style
        )
        minimize_button.pack(side=tk.RIGHT, padx=(5, 10), fill=tk.X, expand=True)
    
    def update_error_status(self, error_msg):
        """更新为错误状态"""
        # 更新图标和颜色
        self.status_icon.config(text="❌", fg="#F44336")
        
        # 更新标题
        self.status_title.config(
            text="启动失败",
            fg="#F44336"
        )
        
        # 更新描述
        self.status_desc.config(
            text=f"{error_msg}\n请检查配置并重试。"
        )
        
        # 重新启用启动按钮
        self.start_button.config(state=tk.NORMAL, text="启动翻译程序")


def main():
    """
    GUI主函数
    """
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()