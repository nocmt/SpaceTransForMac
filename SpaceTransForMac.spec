
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['gui.py'],  # 使用GUI作为入口点
    pathex=[],
    binaries=[],
    datas=[
        ('Release.entitlements', '.'),
        ('model.plzma','./py3langid/data/')
    ],
    hiddenimports=[
        'pynput.keyboard', 
        'pynput.mouse', 
        'pynput._util.darwin',
        'tkinter', 
        'tkinter.scrolledtext', 
        'tkinter.messagebox',
        'config_manager', 
        'main',
        'threading',
        'json',
        'os',
        'sys'
    ],
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
    'LSUIElement': True,  # 不在Dock中显示图标
    'NSAppleEventsUsageDescription': '此应用需要访问系统事件以监听键盘输入',
    'NSAccessibilityUsageDescription': '此应用需要辅助功能权限以监听全局键盘事件和获取选中文本',
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
    entitlements_file="Release.entitlements",
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
    bundle_identifier='com.spacetrans.app',
    info_plist=plist,
)
