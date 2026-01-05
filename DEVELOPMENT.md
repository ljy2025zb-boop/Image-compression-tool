# 开发文档

本文档面向想要修改或扩展此应用的开发者。

## 项目架构

### 核心模块

```
main.py          → 应用入口，初始化 Qt 应用
gui.py           → GUI 界面和用户交互逻辑
compressor.py    → 图片压缩核心算法
```

### 工作流程

```
用户选择文件夹
    ↓
GUI 创建压缩线程
    ↓
线程扫描图片文件
    ↓
逐个压缩图片
    ↓
实时更新进度
    ↓
显示完成结果
```

## 核心算法详解

### 智能压缩策略

`compressor.py` 中的 `compress_image()` 方法实现了三阶段压缩：

#### 阶段 1：直接保存测试

```python
# 先尝试直接保存，检查是否已经满足要求
img.save(buffer, format='PNG', optimize=True)
if file_size <= TARGET_SIZE:
    return  # 无需压缩
```

#### 阶段 2：渐进式缩放

```python
# 使用 0.9 的缩放因子逐步降低分辨率
for i in range(max_iterations):
    new_width = int(original_size[0] * (scale_factor ** (i + 1)))
    new_height = int(original_size[1] * (scale_factor ** (i + 1)))
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    # 检查文件大小...
```

#### 阶段 3：保底处理

```python
# 如果仍然超过限制，使用最小可接受尺寸
if new_width < 100 or new_height < 100:
    break
```

### 为什么选择这个策略？

1. **保留质量优先**：先尝试不压缩，已经符合要求就不动
2. **渐进式调整**：小步迭代，找到最佳平衡点
3. **LANCZOS 重采样**：最高质量的缩放算法
4. **透明度保留**：自动处理 RGBA 通道

## 修改指南

### 1. 修改目标文件大小

编辑 `compressor.py`：

```python
class ImageCompressor:
    TARGET_SIZE = 500 * 1024  # 改为你想要的大小
```

### 2. 调整压缩激进程度

编辑 `compressor.py` 的 `compress_image()` 方法：

```python
# 更激进的压缩（更小的文件，可能损失更多质量）
scale_factor = 0.85  # 从 0.9 改为 0.85

# 更保守的压缩（更好的质量，但文件可能更大）
scale_factor = 0.95  # 从 0.9 改为 0.95
```

### 3. 添加新的图片格式支持

编辑 `compressor.py`：

```python
SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif',
    '.heic',  # 添加 HEIC 支持（需要 pillow-heif 库）
}
```

然后在 `requirements.txt` 添加：

```
pillow-heif>=0.10.0
```

### 4. 修改输出格式

如果想输出为 JPEG 而不是 PNG，编辑 `compressor.py`：

```python
# 在 compress_image() 方法中
output_path = output_dir / (img_path.stem + '.jpg')  # 改为 .jpg

# 保存时
img_resized.save(output_path, format='JPEG', quality=85, optimize=True)
```

### 5. 自定义界面颜色

编辑 `gui.py` 的 `init_ui()` 方法：

```python
# 修改主按钮颜色
self.start_btn.setStyleSheet(
    "QPushButton { background: #FF6B6B; color: white; }"  # 改为红色
)

# 修改成功状态颜色
self.folder_label.setStyleSheet(
    "background: #e3f2fd; color: #1976d2;"  # 改为蓝色主题
)
```

### 6. 添加更多进度信息

编辑 `gui.py` 的 `on_progress()` 方法：

```python
def on_progress(self, current, total, filename):
    progress = int((current / total) * 100)
    self.progress_bar.setValue(progress)
    
    # 添加更多信息
    elapsed_time = time.time() - self.start_time
    avg_time = elapsed_time / current
    remaining = (total - current) * avg_time
    
    self.status_label.setText(
        f"正在处理: {filename} ({current}/{total})\n"
        f"预计剩余时间: {int(remaining)}秒"
    )
```

## 性能优化

### 当前性能

- 单张图片处理时间：0.5-2 秒（取决于原始大小）
- 内存占用：约 50-100MB
- CPU 使用：单线程处理

### 优化建议

#### 1. 多进程处理

```python
from multiprocessing import Pool

def process_batch(images):
    with Pool(processes=4) as pool:
        results = pool.map(compress_image, images)
    return results
```

#### 2. 使用更快的库

考虑使用 `pillow-simd`（SIMD 优化版本）：

```bash
pip uninstall pillow
pip install pillow-simd
```

#### 3. 缓存优化

```python
# 跳过已经处理过的文件
if output_path.exists():
    continue
```

## 调试技巧

### 1. 启用详细日志

在 `compressor.py` 添加：

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.debug(f"Processing {img_path}")
logger.debug(f"Original size: {img.size}, File size: {file_size}")
```

### 2. 测试单张图片

```python
from compressor import ImageCompressor
from pathlib import Path

comp = ImageCompressor()
result = comp.compress_image(
    Path("test.jpg"),
    Path("output.png")
)
print(f"Success: {result}")
```

### 3. 性能分析

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# 运行压缩
comp.process_folder("/path/to/folder")

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## 打包相关

### py2app 配置详解

`setup.py` 中的关键配置：

```python
OPTIONS = {
    'argv_emulation': False,        # 禁用参数模拟
    'packages': ['PySide6', 'PIL'], # 包含的包
    'iconfile': 'icon.icns',        # 应用图标
    'plist': {                      # Info.plist 配置
        'CFBundleName': '图片压缩工具',
        'CFBundleIdentifier': 'com.imagecompressor.app',
        # ...
    }
}
```

### 减小 DMG 大小

1. **排除不必要的文件**：

```python
OPTIONS = {
    'excludes': ['tkinter', 'matplotlib', 'numpy'],
}
```

2. **使用压缩**：

```bash
hdiutil create -format UDZO  # UDZO = 压缩格式
```

### 代码签名（可选）

如果要分发给其他用户，建议进行代码签名：

```bash
# 签名 .app
codesign --deep --force --sign "Developer ID Application: Your Name" \
    dist/图片压缩工具.app

# 公证（需要 Apple Developer 账号）
xcrun notarytool submit dist/ImageCompressor.dmg \
    --apple-id your@email.com \
    --password app-specific-password \
    --team-id TEAM_ID
```

## 测试

### 单元测试示例

创建 `tests/test_compressor.py`：

```python
import unittest
from pathlib import Path
from compressor import ImageCompressor

class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.comp = ImageCompressor()
    
    def test_find_images(self):
        images = self.comp.find_images("test_data")
        self.assertGreater(len(images), 0)
    
    def test_compress_image(self):
        result = self.comp.compress_image(
            Path("test_data/test.jpg"),
            Path("output/test.png")
        )
        self.assertTrue(result)
        
        # 检查文件大小
        output_size = Path("output/test.png").stat().st_size
        self.assertLessEqual(output_size, 500 * 1024)

if __name__ == '__main__':
    unittest.main()
```

运行测试：

```bash
python -m unittest discover tests
```

## 贡献指南

1. Fork 项目
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

## 常见问题

### Q: 如何支持 HEIC 格式？

A: 安装 `pillow-heif` 并在代码中注册：

```python
from pillow_heif import register_heif_opener
register_heif_opener()
```

### Q: 如何添加水印功能？

A: 在 `compress_image()` 中添加：

```python
from PIL import ImageDraw, ImageFont

draw = ImageDraw.Draw(img)
font = ImageFont.truetype("Arial.ttf", 36)
draw.text((10, 10), "Watermark", font=font, fill=(255, 255, 255, 128))
```

### Q: 如何批量重命名输出文件？

A: 修改输出路径生成逻辑：

```python
# 添加前缀
output_path = output_dir / f"compressed_{img_path.name}"

# 添加时间戳
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = output_dir / f"{img_path.stem}_{timestamp}.png"
```

## 资源链接

- [Pillow 文档](https://pillow.readthedocs.io/)
- [PySide6 文档](https://doc.qt.io/qtforpython/)
- [py2app 文档](https://py2app.readthedocs.io/)
- [create-dmg GitHub](https://github.com/create-dmg/create-dmg)
