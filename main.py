#!/usr/bin/env python3
"""
图片压缩工具 - 主程序入口
macOS 原生应用
"""
import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("图片压缩工具")
    app.setOrganizationName("ImageCompressor")
    app.setApplicationVersion("1.0.0")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
