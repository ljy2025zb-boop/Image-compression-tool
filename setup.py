"""
py2app 配置文件
用于将 Python 应用打包为 macOS .app 格式
"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PySide6', 'PIL', 'pathlib'],
    'includes': ['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'scipy'],
    'plist': {
        'CFBundleName': 'ImageCompressor',
        'CFBundleDisplayName': 'Image Compressor',
        'CFBundleIdentifier': 'com.imagecompressor.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2026',
        'NSHighResolutionCapable': True,
    },
    'semi_standalone': False,
    'site_packages': True,
}

setup(
    name='ImageCompressor',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
