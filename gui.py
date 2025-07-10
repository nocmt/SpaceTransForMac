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
        self.root.geometry("600x500")
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
        
        save_button = tk.Button(button_frame, text="保存配置", command=self.save_config, width=15)
        save_button.pack(side=tk.LEFT, padx=5)
        
        refresh_button = tk.Button(button_frame, text="刷新配置", command=self.refresh_config, width=15)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        start_button = tk.Button(button_frame, text="启动翻译程序", command=self.start_translator, width=15)
        start_button.pack(side=tk.RIGHT, padx=5)
    
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
            
            # 检查是否已有状态标签，如果有则移除
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame) and widget.winfo_children() and \
                   isinstance(widget.winfo_children()[0], tk.Label) and \
                   "翻译程序已启动" in widget.winfo_children()[0].cget("text"):
                    widget.destroy()
            
            # 创建状态标签
            status_frame = tk.Frame(self.root, bg="#e6f7ff", padx=10, pady=10)
            status_frame.pack(fill=tk.X, padx=10, pady=10)
            
            status_label = tk.Label(
                status_frame, 
                text="翻译程序正在启动...", 
                font=("Arial", 12),
                fg="#0066cc",
                bg="#e6f7ff",
                padx=10,
                pady=10
            )
            status_label.pack(fill=tk.X)
            
            # 禁用启动按钮
            start_button = None
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button) and child.cget("text") == "启动翻译程序":
                            child.config(state=tk.DISABLED)
                            start_button = child
            
            # 更新GUI状态
            self.root.update()
            
            # 在单独的线程中启动翻译程序
            def run_translator():
                try:
                    translator = main.main(from_gui=True)
                    print("翻译程序已在后台启动")
                    
                    # 在主线程中更新UI
                    self.root.after(0, lambda: status_label.config(
                        text="✅ 翻译程序已启动！按下空格键3次可触发翻译。\n程序在后台运行中，可以关闭此窗口。"
                    ))
                    
                    # 添加一个关闭窗口的按钮
                    self.root.after(0, lambda: tk.Button(
                        status_frame, 
                        text="关闭配置窗口", 
                        command=self.root.destroy,
                        bg="#4CAF50",
                        fg="white",
                        padx=10,
                        pady=5
                    ).pack(pady=10))
                    
                except Exception as e:
                    error_msg = f"翻译程序启动失败: {e}"
                    print(error_msg)
                    # 在主线程中显示错误
                    self.root.after(0, lambda: status_label.config(
                        text=f"❌ {error_msg}",
                        fg="#cc0000"
                    ))
                    # 重新启用启动按钮
                    if start_button:
                        self.root.after(0, lambda: start_button.config(state=tk.NORMAL))
            
            # 启动线程
            translator_thread = threading.Thread(target=run_translator)
            translator_thread.daemon = True  # 设置为守护线程，这样主程序退出时线程也会退出
            translator_thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动翻译程序失败: {e}")


def main():
    """
    GUI主函数
    """
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()