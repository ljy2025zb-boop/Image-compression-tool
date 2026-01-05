# 快速启动指南

## 第一次使用

### 1. 安装依赖（只需一次）

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python main.py
```

### 3. 使用应用

1. 点击"选择文件夹"
2. 选择包含图片的文件夹
3. 点击"开始压缩"
4. 等待完成

压缩后的图片会保存在 `原文件夹/compressed_png/` 目录中。

## 命令行测试（可选）

如果想快速测试压缩功能，无需打开 GUI：

```bash
python test_app.py /path/to/your/images
```

## 打包为 DMG（分发给其他人）

### 前提条件

确保已安装 create-dmg（可选，脚本会自动使用备用方案）：

```bash
brew install create-dmg
```

### 执行打包

```bash
# 赋予执行权限（只需一次）
chmod +x build_dmg.sh

# 打包
./build_dmg.sh
```

打包完成后，`dist/ImageCompressor.dmg` 就是可分发的安装包。

## 自定义图标（可选）

```bash
# 1. 准备 icon.png (1024x1024)
# 2. 生成 .icns
chmod +x create_icon.sh
./create_icon.sh
```

## 常见问题

### 提示缺少模块？

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS 提示"无法打开应用"？

打包后的 .app 首次运行时，右键点击 → 打开，然后选择"打开"。

### 想修改压缩大小限制？

编辑 `compressor.py`，修改：

```python
TARGET_SIZE = 500 * 1024  # 改为你想要的大小（字节）
```

## 项目文件说明

- `main.py` - 主程序入口
- `gui.py` - 图形界面
- `compressor.py` - 压缩核心逻辑
- `setup.py` - 打包配置
- `build_dmg.sh` - 打包脚本
- `test_app.py` - 命令行测试工具

## 下一步

- 阅读完整文档：`README.md`
- 修改压缩策略：编辑 `compressor.py`
- 自定义界面：编辑 `gui.py`
