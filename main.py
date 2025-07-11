#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SpaceTransForMac - 一个macOS下的即时翻译工具

通过连续按下三次空格键触发翻译功能，将选中的文本翻译并替换。
使用AI API进行翻译。
"""

import time
import threading
import requests
from pynput import keyboard
import pyperclip
import keyboard as newkeyboard
import py3langid

# 导入配置管理模块
from config_manager import load_config, get_config_path

# 加载配置
config = load_config()


class SpaceTranslator:
    """
    SpaceTranslator类 - 监听空格键并触发翻译
    """
    def __init__(self):
        # 从配置文件加载配置
        self.API_KEY = config["API_KEY"]
        self.API_HOST = config["API_HOST"]
        self.MODEL = config["MODEL"]
        
        # 空格键监听相关变量
        self.space_count = 0
        self.last_space_time = 0
        self.SPACE_TIMEOUT = config["SPACE_TIMEOUT"]
        self.SPACE_TRIGGER_COUNT = config["SPACE_TRIGGER_COUNT"]
        
        # 创建键盘监听器
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        # 翻译状态
        self.is_translating = False
        self.original_text = ""
        
        print(f"SpaceTransForMac已启动，配置文件位置: {get_config_path()}")
        print(f"连续按下{self.SPACE_TRIGGER_COUNT}次空格键即可触发翻译")
    
    def start(self, from_gui=False):
        """
        启动监听器
        
        Args:
            from_gui: 是否从GUI启动，如果是则不阻塞主线程
        """
        # 确保监听器已启动
        if not self.keyboard_listener.is_alive():
            self.keyboard_listener.start()
        
        # 如果不是从GUI启动，则阻塞主线程以保持程序运行
        if not from_gui:
            try:
                self.keyboard_listener.join()
            except Exception as e:
                print(f"监听器异常: {e}")
                # 尝试重新启动监听器
                self.keyboard_listener = keyboard.Listener(
                    on_press=self.on_key_press,
                    on_release=self.on_key_release
                )
                self.keyboard_listener.start()
                self.keyboard_listener.join()
    
    def on_key_press(self, key):
        """
        按键按下事件处理
        """
        try:
            # 检测空格键
            if key == keyboard.Key.space:
                current_time = time.time()
                
                # 检查是否在超时时间内
                if current_time - self.last_space_time < self.SPACE_TIMEOUT:
                    self.space_count += 1
                else:
                    self.space_count = 1
                
                self.last_space_time = current_time
                
                # 如果连续按下指定次数的空格
                if self.space_count == self.SPACE_TRIGGER_COUNT and not self.is_translating:
                    # 重置计数器
                    self.space_count = 0
                    
                    # 启动翻译线程
                    threading.Thread(target=self.translate_selected_text).start()
                    return True
            else:
                # 其他键重置空格计数
                self.space_count = 0
        except Exception as e:
            print(f"按键处理错误: {e}")
        
        return True
    
    def on_key_release(self, key):
        """
        按键释放事件处理
        """
        # if key == keyboard.Key.esc:
        #     print("SpaceTransForMac已退出")
        #     return False
        
        return True
    
    def get_selected_text(self):
        """
        获取当前选中的文本
        """
        # 保存当前剪贴板内容
        old_clipboard = pyperclip.paste()
        
        # 模拟Command+C复制选中文本
        newkeyboard.press_and_release('cmd+c')
        
        # 等待剪贴板更新
        time.sleep(0.1)
        
        # 获取选中的文本
        selected_text = pyperclip.paste()
        
        # 恢复原始剪贴板内容
        if (type(old_clipboard) == str):
            pyperclip.copy(old_clipboard)
        
        return selected_text
    
    def replace_selected_text(self, new_text):
        """
        替换选中的文本
        """
        print("替换选中的文本")
        # 保存当前剪贴板内容
        old_clipboard = pyperclip.paste()
        # 复制新文本到剪贴板
        pyperclip.copy(new_text)
        # 模拟Command+V粘贴
        newkeyboard.press_and_release('cmd+v')
        # 恢复原始剪贴板内容
        pyperclip.copy(old_clipboard)
    
    def translate_text(self, text):
        """
        调用AI API翻译文本
        """
        if not self.API_KEY:
            return "错误：请先设置API_KEY"
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.API_KEY}"
            }
            
            payload = {
                "model": self.MODEL,
                "messages": [
                    {"role": "system", "content": config["SYSTEM_PROMPT"]},
                    {"role": "user", "content": text}
                ],
                "temperature": config["TEMPERATURE"]
            }
            
            response = requests.post(f"{self.API_HOST}/v1/chat/completions", headers=headers, json=payload)
            response_data = response.json()
            
            if response.status_code == 200 and "choices" in response_data:
                translated_text = response_data["choices"][0]["message"]["content"]
                return translated_text.strip()
            else:
                error_message = response_data.get("error", {}).get("message", "未知错误")
                return f"翻译失败: {error_message}"
        
        except Exception as e:
            return f"翻译出错: {str(e)}"
    
    def translate_selected_text(self):
        """
        翻译选中的文本并替换
        """
        if self.is_translating:
            return
        
        self.is_translating = True
        
        try:
            # 先模拟按下Command+A全选文本
            newkeyboard.press_and_release('cmd+a')
            
            # 短暂延迟确保全选完成
            time.sleep(0.1)
            
            # 获取选中的文本
            selected_text = self.get_selected_text()
            
            if not selected_text or selected_text.isspace():
                print("没有选中文本或选中的是空白文本")
                self.is_translating = False
                return
            
            self.original_text = selected_text
            print(f"正在翻译: {selected_text[:30]}...")
            selected_text = selected_text[:-3]
            # 识别内容语言，补充文本
            lang , trust_level = py3langid.classify(selected_text)
            print(lang,trust_level)
            if lang == "zh":
                selected_text = f"Translate into English: {selected_text}"
            else:
                selected_text = f"Translate into Simplified Chinese: {selected_text}"

            # 调用API翻译文本
            translated_text = self.translate_text(selected_text) # 去掉3个空格
            
            # 替换选中的文本
            if translated_text and translated_text != "错误：请先设置API_KEY":
                # 确保文本已被选中
                self.replace_selected_text(translated_text)
                print(f"翻译完成: {translated_text[:30]}...")
            else:
                print(f"翻译失败: {translated_text}")
        
        except Exception as e:
            print(f"翻译过程出错: {e}")
        
        finally:
            self.is_translating = False


def main(from_gui=False):
    """
    主函数
    
    Args:
        from_gui: 是否从GUI启动，如果是则不捕获KeyboardInterrupt
    """
    try:
        translator = SpaceTranslator()
        translator.start(from_gui=from_gui)
        if from_gui:
            # 如果从GUI启动，返回translator实例以便GUI可以控制它
            return translator
    except KeyboardInterrupt:
        if not from_gui:
            print("\nSpaceTransForMac已退出")
    except Exception as e:
        print(f"程序出错: {e}")
        if from_gui:
            raise  # 从GUI启动时，向上传递异常以便GUI可以显示错误


if __name__ == "__main__":
    main()