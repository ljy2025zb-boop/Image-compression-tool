"""
图形界面模块
使用 PySide6 创建 macOS 原生风格界面
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from pathlib import Path
from compressor import ImageCompressor


class CompressorThread(QThread):
    """压缩线程"""
    progress = Signal(int, int, str)  # current, total, filename
    finished = Signal(int, int, list)  # success, fail, errors
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.compressor = ImageCompressor(progress_callback=self.on_progress)
    
    def on_progress(self, current, total, filename):
        """进度回调"""
        self.progress.emit(current, total, filename)
    
    def run(self):
        """执行压缩"""
        success, fail = self.compressor.process_folder(self.folder_path)
        self.finished.emit(success, fail, self.compressor.errors)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.folder_path = None
        self.compressor_thread = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("图片压缩工具")
        self.setMinimumSize(600, 500)
        
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("图片批量压缩工具")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 说明文字
        desc_label = QLabel(
            "支持 JPG, PNG, WEBP, BMP, TIFF 等格式\n"
            "自动压缩至 500KB 以内，输出为 PNG 格式"
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc_label)
        
        # 文件夹选择区域
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("未选择文件夹")
        self.folder_label.setStyleSheet(
            "padding: 10px; background: #f0f0f0; "
            "border-radius: 5px; color: #666;"
        )
        folder_layout.addWidget(self.folder_label, 1)
        
        self.select_btn = QPushButton("选择文件夹")
        self.select_btn.setMinimumHeight(40)
        self.select_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.select_btn)
        
        layout.addLayout(folder_layout)
        
        # 开始按钮
        self.start_btn = QPushButton("开始压缩")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet(
            "QPushButton { background: #007AFF; color: white; "
            "font-size: 16px; font-weight: bold; border-radius: 8px; }"
            "QPushButton:hover { background: #0051D5; }"
            "QPushButton:disabled { background: #ccc; }"
        )
        self.start_btn.clicked.connect(self.start_compression)
        layout.addWidget(self.start_btn)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("等待开始...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 日志区域
        log_label = QLabel("处理日志:")
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        layout.addStretch()
    
    def select_folder(self):
        """选择文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择包含图片的文件夹",
            str(Path.home())
        )
        
        if folder:
            self.folder_path = folder
            self.folder_label.setText(folder)
            self.folder_label.setStyleSheet(
                "padding: 10px; background: #e8f5e9; "
                "border-radius: 5px; color: #2e7d32;"
            )
            self.start_btn.setEnabled(True)
            self.log(f"已选择文件夹: {folder}")
    
    def start_compression(self):
        """开始压缩"""
        if not self.folder_path:
            return
        
        # 禁用按钮
        self.start_btn.setEnabled(False)
        self.select_btn.setEnabled(False)
        
        # 重置进度
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.log("开始扫描图片文件...")
        
        # 创建并启动线程
        self.compressor_thread = CompressorThread(self.folder_path)
        self.compressor_thread.progress.connect(self.on_progress)
        self.compressor_thread.finished.connect(self.on_finished)
        self.compressor_thread.start()
    
    def on_progress(self, current, total, filename):
        """更新进度"""
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"正在处理: {filename} ({current}/{total})")
        self.log(f"[{current}/{total}] {filename}")
    
    def on_finished(self, success, fail, errors):
        """压缩完成"""
        self.progress_bar.setValue(100)
        self.status_label.setText("处理完成！")
        
        # 显示结果
        result_msg = f"\n{'='*50}\n"
        result_msg += f"处理完成！\n"
        result_msg += f"成功: {success} 张\n"
        result_msg += f"失败: {fail} 张\n"
        
        if errors:
            result_msg += f"\n错误详情:\n"
            for error in errors:
                result_msg += f"  - {error}\n"
        
        result_msg += f"\n输出目录: {self.folder_path}/compressed_png/\n"
        result_msg += f"{'='*50}"
        
        self.log(result_msg)
        
        # 恢复按钮
        self.start_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        
        # 弹出完成提示
        QMessageBox.information(
            self,
            "处理完成",
            f"成功压缩 {success} 张图片\n"
            f"失败 {fail} 张\n\n"
            f"输出目录:\n{self.folder_path}/compressed_png/"
        )
    
    def log(self, message):
        """添加日志"""
        self.log_text.append(message)
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
