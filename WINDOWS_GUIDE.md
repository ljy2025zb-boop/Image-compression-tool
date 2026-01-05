# Windows 开发指南

## 问题说明

由于你在 Windows 环境下开发，但目标是打包为 macOS 的 .dmg 文件，这里提供几种解决方案。

## ⚠️ 重要提示

**macOS 应用（.app 和 .dmg）只能在 macOS 系统上打包**，因为：
- py2app 只能在 macOS 上运行
- .app 是 macOS 专有的应用包格式
- .dmg 是 macOS 专有的磁盘镜像格式
- 代码签名需要 macOS 和 Apple Developer 账号

## 🎯 推荐方案

### 方案 1：在 Windows 上开发，在 macOS 上打包（最佳）

#### 步骤 1：在 Windows 上开发和测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用（测试功能）
python main.py

# 命令行测试
python test_app.py C:\Users\YourName\Pictures
```

#### 步骤 2：将代码传输到 macOS

**方法 A：使用 Git**
```bash
# Windows 上
git init
git add .
git commit -m "Initial commit"
git push origin main

# macOS 上
git clone <your-repo-url>
```

**方法 B：使用云盘**
- 将整个项目文件夹上传到 OneDrive/Google Drive/Dropbox
- 在 macOS 上下载

**方法 C：使用 USB 或网络传输**
- 压缩项目文件夹
- 通过 USB 或网络传输到 macOS

#### 步骤 3：在 macOS 上打包

```bash
# 在 macOS 终端中
cd /path/to/project

# 安装依赖
pip3 install -r requirements.txt

# 打包
chmod +x build_dmg.sh
./build_dmg.sh
```

---

### 方案 2：使用虚拟机运行 macOS（技术方案）

在 Windows 上使用虚拟机运行 macOS：

#### 使用 VMware 或 VirtualBox

1. 安装虚拟机软件
2. 创建 macOS 虚拟机（需要 macOS 镜像）
3. 在虚拟机中打包应用

**注意**：
- 需要较高的硬件配置
- 可能违反 Apple 的许可协议（除非使用 Mac 硬件）
- 设置复杂

---

### 方案 3：使用云端 macOS 服务（付费方案）

使用云端 macOS 构建服务：

#### 选项 A：GitHub Actions（免费）

创建 `.github/workflows/build.yml`：

```yaml
name: Build macOS App

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Build app
      run: |
        python setup.py py2app
    
    - name: Create DMG
      run: |
        brew install create-dmg
        ./build_dmg.sh
    
    - name: Upload DMG
      uses: actions/upload-artifact@v3
      with:
        name: ImageCompressor-DMG
        path: dist/*.dmg
```

#### 选项 B：MacStadium 或 MacinCloud（付费）

- 租用云端 macOS 服务器
- 远程连接进行打包

---

### 方案 4：打包为 Windows 版本（替代方案）

如果主要用户是 Windows，可以打包为 Windows 应用：

#### 使用 PyInstaller（Windows）

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包为 Windows .exe
pyinstaller --name="图片压缩工具" ^
            --windowed ^
            --onefile ^
            --icon=icon.ico ^
            main.py
```

#### 使用 Inno Setup 创建安装程序

创建 Windows 安装包（.exe 安装程序）

---

## 🔨 Windows 开发环境配置

### 1. 安装 Python

```bash
# 检查 Python 版本
python --version

# 应该是 Python 3.8 或更高
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python main.py
```

### 4. 测试功能

```bash
# 命令行测试
python test_app.py "C:\Users\YourName\Pictures\test"

# 环境检查
python check_env.py
```

---

## 📝 Windows 特定注意事项

### 路径分隔符

Windows 使用反斜杠 `\`，macOS/Linux 使用正斜杠 `/`。

代码已经使用 `pathlib.Path`，会自动处理跨平台路径问题。

### 文件编码

确保所有 Python 文件使用 UTF-8 编码：

```python
# -*- coding: utf-8 -*-
```

### Shell 脚本

Windows 上无法直接运行 `.sh` 脚本，但可以：

1. 使用 Git Bash
2. 使用 WSL (Windows Subsystem for Linux)
3. 手动执行脚本中的命令

---

## 🎯 推荐工作流程

### 日常开发（Windows）

```bash
# 1. 修改代码
# 2. 测试功能
python main.py

# 3. 提交到 Git
git add .
git commit -m "Update features"
git push
```

### 打包发布（macOS）

```bash
# 1. 在 macOS 上拉取最新代码
git pull

# 2. 打包
./build_dmg.sh

# 3. 测试 DMG
open dist/ImageCompressor.dmg

# 4. 分发
# 上传到网盘或发布到 GitHub Releases
```

---

## 🔧 Windows 打包脚本

创建 `build_windows.bat`：

```batch
@echo off
echo ==========================================
echo 图片压缩工具 - Windows 打包脚本
echo ==========================================

echo.
echo 1. 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo 2. 安装 PyInstaller...
pip install pyinstaller

echo.
echo 3. 打包为 Windows 应用...
pyinstaller --name="ImageCompressor" ^
            --windowed ^
            --onefile ^
            --add-data "README.md;." ^
            main.py

echo.
echo ==========================================
echo 打包完成！
echo ==========================================
echo.
echo EXE 文件位置: dist\ImageCompressor.exe
echo.
pause
```

---

## 📦 跨平台打包总结

| 平台 | 开发 | 打包工具 | 输出格式 |
|------|------|---------|---------|
| Windows | ✅ 可以 | PyInstaller | .exe |
| macOS | ✅ 可以 | py2app | .app + .dmg |
| Linux | ✅ 可以 | PyInstaller | 可执行文件 |

**关键点**：
- ✅ 在 Windows 上开发和测试功能
- ✅ 代码是跨平台的（使用 pathlib）
- ❌ 无法在 Windows 上打包 macOS 应用
- ✅ 需要 macOS 环境进行最终打包

---

## 🚀 快速开始（Windows）

```bash
# 1. 检查环境
python check_env.py

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行应用
python main.py

# 4. 测试功能
python test_app.py "C:\Users\YourName\Pictures"
```

---

## ❓ 常见问题

### Q: 我没有 Mac，怎么打包 DMG？

A: 三个选择：
1. 借用朋友的 Mac
2. 使用 GitHub Actions（免费，推荐）
3. 租用云端 macOS 服务

### Q: 可以在 Windows 上打包 macOS 应用吗？

A: 不可以。macOS 应用必须在 macOS 上打包。

### Q: 我可以只提供 Python 源码吗？

A: 可以！用户需要：
```bash
pip install -r requirements.txt
python main.py
```

### Q: 如何同时支持 Windows 和 macOS？

A: 
- Windows: 使用 PyInstaller 打包 .exe
- macOS: 使用 py2app 打包 .dmg
- 或者：提供 Python 源码，让用户自行运行

---

## 📚 相关资源

- [PyInstaller 文档](https://pyinstaller.org/)
- [GitHub Actions 文档](https://docs.github.com/actions)
- [py2app 文档](https://py2app.readthedocs.io/)
