# 图片压缩工具 (Image Compressor)

一个 macOS 原生应用，用于批量压缩图片并转换为 PNG 格式（≤ 500KB）。

## 功能特性

- 🖼️ 支持多种图片格式：JPG, JPEG, PNG, WEBP, BMP, TIFF 等
- 📁 递归遍历文件夹及子文件夹
- 🎯 智能压缩：自动调整分辨率和质量，确保输出 ≤ 500KB
- 📂 保持原始目录结构，输出到 `compressed_png/` 子目录
- 🎨 macOS 原生外观界面（PySide6）
- 📊 实时进度显示和日志输出
- ⚡ 多线程处理，界面不卡顿

## 系统要求

### 运行要求
- Python 3.8 或更高版本
- Windows 10/11 或 macOS 10.13+

### 打包要求
- **Windows 打包**：Windows 系统 + PyInstaller
- **macOS 打包**：macOS 系统 + py2app（或使用 GitHub Actions）

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 create-dmg 工具（用于打包，可选）
brew install create-dmg
```

### 2. 运行程序

```bash
python main.py
```

### 3. 使用应用

1. 点击"选择文件夹"按钮，选择包含图片的文件夹
2. 点击"开始压缩"按钮
3. 等待处理完成
4. 压缩后的图片保存在 `原文件夹/compressed_png/` 目录中

## 打包为可执行文件

### Windows 打包（在 Windows 上）

```bash
# 运行打包脚本
build_windows.bat
```

打包完成后，`dist/ImageCompressor.exe` 就是可执行文件。

### macOS 打包（在 macOS 上）

```bash
# 赋予执行权限
chmod +x build_dmg.sh

# 执行打包脚本
./build_dmg.sh
```

打包完成后，会在 `dist/` 目录下生成 `ImageCompressor.dmg` 文件。

### 使用 GitHub Actions 自动打包（推荐）

如果你在 Windows 上开发但需要 macOS 的 .dmg 文件：

1. 将代码推送到 GitHub
2. GitHub Actions 会自动在 macOS 环境中打包
3. 在 Actions 页面下载生成的 DMG 文件

详见 `.github/workflows/build-macos.yml`

**注意**：
- Windows 打包只能生成 .exe（使用 PyInstaller）
- macOS 打包只能生成 .dmg（使用 py2app）
- 跨平台打包需要对应的操作系统环境

## 自定义应用图标（可选）

如果想使用自定义图标：

```bash
# 1. 准备一个 1024x1024 的 PNG 图片，命名为 icon.png
# 2. 赋予脚本执行权限
chmod +x create_icon.sh

# 3. 生成 .icns 图标文件
./create_icon.sh
```

生成的 `icon.icns` 会在打包时自动使用。

## 项目结构

```
.
├── main.py                          # 主程序入口
├── compressor.py                    # 图片压缩核心逻辑
├── gui.py                           # GUI 界面（PySide6）
├── requirements.txt                 # Python 依赖
├── setup.py                         # py2app 配置（macOS）
├── build_dmg.sh                     # DMG 打包脚本（macOS）
├── build_windows.bat                # EXE 打包脚本（Windows）
├── create_icon.sh                   # 图标生成脚本
├── test_app.py                      # 命令行测试工具
├── check_env.py                     # 环境检查脚本
├── .github/workflows/build-macos.yml # GitHub Actions 自动打包
├── WINDOWS_GUIDE.md                 # Windows 开发指南
└── README.md                        # 说明文档
```

## 技术实现

### 智能压缩策略

1. **直接保存检测**：首先尝试直接保存，如果已经 ≤ 500KB，直接输出
2. **渐进式缩放**：使用 0.9 的缩放因子逐步降低分辨率
3. **质量优化**：使用 LANCZOS 重采样算法保持最佳视觉质量
4. **透明度保留**：自动处理 RGBA 和透明通道

### 技术栈

- **GUI 框架**: PySide6 (Qt for Python) - macOS 原生外观
- **图像处理**: Pillow (PIL) - 强大的图像处理库
- **多线程**: QThread - 避免界面卡顿
- **打包工具**: py2app + create-dmg / hdiutil

## 常见问题

### Q: 我在 Windows 上开发，如何打包 macOS 的 .dmg？

A: 有三种方法：
1. **使用 GitHub Actions**（推荐）：将代码推送到 GitHub，自动在 macOS 环境打包
2. **借用 Mac**：将代码传输到 Mac 上执行 `./build_dmg.sh`
3. **云端 macOS**：使用 MacStadium 等服务

详见 `WINDOWS_GUIDE.md`

### Q: 可以在 Windows 上打包为 .exe 吗？

A: 可以！运行 `build_windows.bat` 即可打包为 Windows 可执行文件。

### Q: 打包时提示找不到 create-dmg？

A: 有两种解决方案：
1. 安装 create-dmg：`brew install create-dmg`
2. 脚本会自动使用 hdiutil 作为备用方案（macOS 自带）

### Q: 运行时提示缺少依赖？

A: 确保已安装所有依赖：`pip install -r requirements.txt`

### Q: 压缩后图片质量不满意？

A: 可以修改 `compressor.py` 中的 `TARGET_SIZE` 和 `scale_factor` 参数来调整压缩策略。

### Q: 如何在其他 Mac 上分发？

A: 将生成的 `.dmg` 文件发送给其他用户，他们双击打开后拖拽到 Applications 文件夹即可安装。

## 开发说明

### 修改目标文件大小

编辑 `compressor.py`：

```python
TARGET_SIZE = 500 * 1024  # 修改为你想要的大小（字节）
```

### 修改压缩策略

编辑 `compressor.py` 中的 `compress_image` 方法，调整：
- `scale_factor`: 缩放因子（默认 0.9）
- `quality`: 质量参数（默认 95）
- `max_iterations`: 最大迭代次数（默认 20）

### 修改界面样式

编辑 `gui.py` 中的 `init_ui` 方法，自定义颜色、字体、布局等。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
