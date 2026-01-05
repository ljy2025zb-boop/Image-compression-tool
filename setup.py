"""
py2app 配置文件
用于将 Python 应用打包为 macOS .app 格式
"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PySide6', 'PIL'],
    'iconfile': 'icon.icns',  # 如果有图标文件
    'plist': {
        'CFBundleName': '图片压缩工具',
        'CFBundleDisplayName': '图片压缩工具',
        'CFBundleIdentifier': 'com.imagecompressor.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2026',
        'NSHighResolutionCapable': True,
    }
}

setup(
    name='ImageCompressor',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
