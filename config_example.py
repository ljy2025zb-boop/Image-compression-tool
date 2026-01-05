"""
配置示例文件
展示如何自定义压缩参数和界面设置
"""

# ============================================
# 压缩配置
# ============================================

# 目标文件大小（字节）
TARGET_SIZE = 500 * 1024  # 500KB

# 支持的图片格式
SUPPORTED_FORMATS = {
    '.jpg', '.jpeg',  # JPEG 格式
    '.png',           # PNG 格式
    '.webp',          # WebP 格式
    '.bmp',           # BMP 格式
    '.tiff', '.tif',  # TIFF 格式
    '.gif',           # GIF 格式（可选）
}

# 压缩策略参数
COMPRESSION_CONFIG = {
    'scale_factor': 0.9,      # 缩放因子（0.8-0.95 推荐）
    'initial_quality': 95,    # 初始质量（85-95 推荐）
    'max_iterations': 20,     # 最大迭代次数
    'min_dimension': 100,     # 最小尺寸（像素）
}

# 输出目录名称
OUTPUT_DIR = 'compressed_png'

# ============================================
# 界面配置
# ============================================

# 窗口设置
WINDOW_CONFIG = {
    'title': '图片压缩工具',
    'min_width': 600,
    'min_height': 500,
}

# 颜色主题
COLOR_THEME = {
    'primary': '#007AFF',      # 主色调（蓝色）
    'primary_hover': '#0051D5', # 悬停颜色
    'success': '#2e7d32',      # 成功颜色（绿色）
    'error': '#d32f2f',        # 错误颜色（红色）
    'background': '#f0f0f0',   # 背景颜色
    'text': '#666',            # 文字颜色
}

# ============================================
# 使用说明
# ============================================

"""
如何应用这些配置：

1. 修改压缩参数：
   编辑 compressor.py，找到对应的常量并修改

2. 修改界面设置：
   编辑 gui.py，在 init_ui() 方法中修改对应的值

3. 示例：修改目标大小为 1MB
   在 compressor.py 中：
   TARGET_SIZE = 1024 * 1024  # 1MB

4. 示例：修改主题颜色
   在 gui.py 中找到按钮样式：
   "background: #007AFF"  改为  "background: #FF6B6B"
"""

# ============================================
# 高级配置示例
# ============================================

# 如果想添加更多图片格式支持
ADDITIONAL_FORMATS = {
    '.heic',  # iPhone 照片格式（需要额外库支持）
    '.svg',   # 矢量图（需要特殊处理）
}

# 如果想使用不同的压缩算法
RESAMPLING_METHODS = {
    'LANCZOS': 'Image.Resampling.LANCZOS',    # 最高质量（默认）
    'BICUBIC': 'Image.Resampling.BICUBIC',    # 高质量
    'BILINEAR': 'Image.Resampling.BILINEAR',  # 中等质量
    'NEAREST': 'Image.Resampling.NEAREST',    # 最快速度
}

# 如果想保存为不同格式
OUTPUT_FORMATS = {
    'PNG': {'format': 'PNG', 'optimize': True},
    'JPEG': {'format': 'JPEG', 'quality': 85, 'optimize': True},
    'WEBP': {'format': 'WEBP', 'quality': 80},
}
