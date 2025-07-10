#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SpaceTransForMac启动脚本

检查依赖并启动SpaceTransForMac程序
"""

import sys
import subprocess
import importlib.util

def check_dependency(module_name):
    """
    检查是否已安装指定的Python模块
    """
    return importlib.util.find_spec(module_name) is not None


def install_dependencies():
    """
    安装requirements.txt中的依赖
    """
    print("正在安装依赖...")    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False


def check_config():
    """
    检查配置文件是否存在，API密钥是否已设置
    """
    try:
        # 导入配置管理模块
        from config_manager import load_config, get_config_path
        
        # 加载配置
        config = load_config()
        config_path = get_config_path()
        
        if not config["API_KEY"]:
            print(f"警告: API密钥未设置，请在{config_path}中设置API_KEY")
            return False
        return True
    except Exception as e:
        print(f"配置检查出错: {e}")
        return False


def check_pyinstaller():
    """
    检查是否已安装PyInstaller
    """
    return check_dependency("PyInstaller")


def install_pyinstaller():
    """
    安装PyInstaller
    """
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller安装失败: {e}")
        return False


def build_executable():
    """
    使用PyInstaller打包应用
    """
    print("=== 开始打包应用 ===")
    print("注意：打包后的应用程序不包含配置文件，首次运行时会自动创建配置文件")
    print("打包后的应用将包含GUI配置界面，可以通过界面设置和保存配置")
    print("应用将使用当前目录下的icon.icns作为图标")
    
    # 确保PyInstaller已安装
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("无法安装PyInstaller，打包失败")
            return False
    
    # 创建spec文件
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui.py'],  # 使用GUI作为入口点
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pynput.keyboard', 'pynput.mouse', 'tkinter', 'tkinter.scrolledtext', 'config_manager', 'main'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
plist = {
    'CFBundleName': 'SpaceTransForMac',
    'CFBundleDisplayName': 'SpaceTransForMac',
    'CFBundleGetInfoString': "SpaceTransForMac - 一个macOS下的即时翻译工具",
    'CFBundleIdentifier': "com.spacetrans.app",
    'CFBundleVersion': "1.0.0",
    'CFBundleShortVersionString': "1.0.0",
    'NSHumanReadableCopyright': "Copyright © 2025, SpaceTransForMac",
}
# 不将配置文件打包进应用程序

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SpaceTransForMac',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SpaceTransForMac',
)
app = BUNDLE(
    coll,
    name='SpaceTransForMac.app',
    icon='icon.icns',
    bundle_identifier=None,
    info_plist=plist,
)
'''
    
    with open('SpaceTransForMac.spec', 'w') as f:
        f.write(spec_content)
    
    # 运行PyInstaller
    try:
        print("正在打包应用，这可能需要几分钟时间...")
        subprocess.check_call(["pyinstaller", "SpaceTransForMac.spec"])
        print("\n打包完成！应用位于 dist/SpaceTransForMac.app")
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        return False


def main():
    """
    主函数
    """
    print("=== SpaceTransForMac启动器 ===")
    
    # 检查必要的依赖
    required_modules = ["pynput", "pyperclip", "requests", "tkinter"]
    missing_modules = [m for m in required_modules if not check_dependency(m)]
    
    if missing_modules:
        print(f"缺少必要的依赖: {', '.join(missing_modules)}")
        user_input = input("是否自动安装依赖？(y/n): ")
        if user_input.lower() == "y":
            if not install_dependencies():
                print("依赖安装失败，请手动运行: pip install -r requirements.txt")
                return
        else:
            print("请手动安装依赖: pip install -r requirements.txt")
            return
    
    # 检查配置
    # check_config()
    
    # 询问启动模式
    print("\n请选择启动模式:")
    print("1. 启动翻译程序 (无界面)")
    print("2. 启动配置界面")
    print("3. 打包为可执行应用")
    
    while True:
        user_input = input("请输入选项 (1/2/3): ")
        if user_input in ["1", "2", "3"]:
            break
        print("无效的选项，请重新输入")
    
    if user_input == "3":
        build_executable()
        return
    
    # 启动主程序或GUI
    try:
        if user_input == "1":
            print("正在启动SpaceTransForMac...")
            import main
            main.main()
        else:  # user_input == "2"
            print("正在启动配置界面...")
            import gui
            gui.main()
    except KeyboardInterrupt:
        print("\nSpaceTransForMac已退出")
    except Exception as e:
        print(f"程序启动失败: {e}")


if __name__ == "__main__":
    main()