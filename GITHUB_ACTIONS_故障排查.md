# GitHub Actions 故障排查指南

## 问题：build-macos Process completed with exit code 1

这个错误表示 GitHub Actions 构建失败。以下是常见原因和解决方案。

## 🔍 常见问题和解决方案

### 问题 1：py2app 构建失败

**症状**：
```
error: [Errno 2] No such file or directory: 'dist/main.app'
```

**原因**：
- py2app 在 GitHub Actions 环境中可能遇到权限或依赖问题
- PySide6 的某些组件可能无法正确打包

**解决方案 A：使用更新的配置**

我已经更新了 `.github/workflows/build-macos.yml`，主要改进：

1. **使用 Python 3.11**（更稳定）
2. **添加验证步骤**（检查依赖是否正确安装）
3. **改进错误处理**（更详细的日志）
4. **简化 DMG 创建**（只使用 hdiutil，不依赖 create-dmg）

**解决方案 B：使用简化版本**

如果主配置仍然失败，使用 `build-macos-simple.yml`：

```yaml
# 在 GitHub 仓库的 Actions 页面
# 选择 "Build macOS DMG (Simple)"
# 点击 "Run workflow"
```

### 问题 2：依赖安装失败

**症状**：
```
ERROR: Could not find a version that satisfies the requirement PySide6
```

**解决方案**：

更新 `requirements.txt`，确保版本兼容：

```txt
Pillow>=10.0.0,<11.0.0
PySide6>=6.5.0,<7.0.0
py2app>=0.28.0
```

### 问题 3：中文文件名问题

**症状**：
```
mv: cannot stat 'dist/图片压缩工具.app': No such file or directory
```

**原因**：
- GitHub Actions 环境可能不支持中文文件名

**解决方案**：

已修改为使用英文文件名：
- `main.app` → `ImageCompressor.app`
- `图片压缩工具.dmg` → `ImageCompressor.dmg`

### 问题 4：权限问题

**症状**：
```
Permission denied
```

**解决方案**：

在构建步骤中添加权限设置：

```yaml
- name: Set permissions
  run: |
    chmod +x build_dmg.sh
```

## 🛠️ 调试步骤

### 步骤 1：查看构建日志

1. 访问 GitHub 仓库
2. 点击 "Actions" 标签
3. 点击失败的 workflow run
4. 查看详细日志，找到错误信息

### 步骤 2：本地测试

在本地 Mac 上测试构建：

```bash
# 安装依赖
pip install -r requirements.txt

# 测试 py2app
python setup.py py2app

# 检查输出
ls -la dist/
```

### 步骤 3：使用简化版本

如果主配置失败，尝试简化版本：

```bash
# 在 GitHub Actions 中
# 手动触发 "Build macOS DMG (Simple)" workflow
```

## 📝 更新后的配置说明

### 主配置文件：`.github/workflows/build-macos.yml`

**改进点**：

1. **更新 Python 版本**
   ```yaml
   python-version: '3.11'  # 从 3.9 升级到 3.11
   ```

2. **添加验证步骤**
   ```yaml
   - name: Verify installation
     run: |
       python -c "import PySide6; print('PySide6 version:', PySide6.__version__)"
   ```

3. **改进错误处理**
   ```yaml
   - name: Verify app creation
     run: |
       if [ -d "dist/main.app" ]; then
         echo "App created successfully"
       else
         echo "Error: App not created"
         exit 1
       fi
   ```

4. **使用英文文件名**
   ```yaml
   mv "dist/main.app" "dist/ImageCompressor.app"
   ```

5. **简化 DMG 创建**
   ```yaml
   hdiutil create -volname "ImageCompressor" \
     -srcfolder "dist/ImageCompressor.app" \
     -ov -format UDZO \
     "dist/ImageCompressor.dmg"
   ```

### 备用配置：`.github/workflows/build-macos-simple.yml`

**特点**：
- 更详细的日志输出
- 上传构建日志以便调试
- 手动触发（workflow_dispatch）

## 🔧 setup.py 改进

**更新内容**：

```python
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PySide6', 'PIL', 'pathlib'],
    'includes': ['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'scipy'],
    'plist': {
        'CFBundleName': 'ImageCompressor',  # 使用英文
        'CFBundleDisplayName': 'Image Compressor',
        # ...
    },
    'semi_standalone': False,
    'site_packages': True,
}
```

**改进点**：
1. 明确指定需要包含的 PySide6 模块
2. 排除不需要的大型库（减小体积）
3. 使用英文名称（避免编码问题）
4. 添加 `site_packages: True`（确保依赖正确打包）

## 🚀 推荐使用方法

### 方法 1：使用更新后的主配置（推荐）

```bash
# 1. 提交更新后的文件
git add .github/workflows/build-macos.yml setup.py
git commit -m "Fix GitHub Actions build"
git push

# 2. 等待自动构建
# 3. 在 Actions 页面下载 DMG
```

### 方法 2：使用简化版本（调试用）

```bash
# 1. 在 GitHub 仓库页面
# 2. 点击 "Actions" 标签
# 3. 选择 "Build macOS DMG (Simple)"
# 4. 点击 "Run workflow"
# 5. 查看详细日志
```

### 方法 3：本地构建（最可靠）

如果有 Mac 电脑：

```bash
# 1. 克隆仓库
git clone <your-repo-url>
cd <repo-name>

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 构建
chmod +x build_dmg.sh
./build_dmg.sh

# 4. 获取 DMG
# 文件位置：dist/ImageCompressor.dmg
```

## 📊 构建时间预估

| 步骤 | 预计时间 |
|------|---------|
| 安装依赖 | 2-3 分钟 |
| py2app 构建 | 3-5 分钟 |
| 创建 DMG | 1-2 分钟 |
| **总计** | **6-10 分钟** |

## ⚠️ 注意事项

1. **首次构建可能较慢**
   - GitHub Actions 需要下载和安装所有依赖
   - 后续构建会使用缓存，速度更快

2. **分支名称**
   - 确保你的主分支名称是 `main` 或 `master`
   - 配置文件中已包含两者：`branches: [ main, master ]`

3. **手动触发**
   - 两个配置文件都支持 `workflow_dispatch`
   - 可以在 Actions 页面手动触发构建

4. **构建日志**
   - 简化版本会上传构建日志
   - 可以下载查看详细错误信息

## 🆘 如果仍然失败

### 选项 1：查看详细日志

1. 在 GitHub Actions 页面查看完整日志
2. 找到具体的错误信息
3. 根据错误信息搜索解决方案

### 选项 2：使用 Issue 模板

创建一个 Issue，包含：
- 完整的错误日志
- 使用的配置文件
- Python 和依赖版本

### 选项 3：暂时使用本地构建

如果 GitHub Actions 持续失败：
1. 借用 Mac 电脑
2. 使用 `build_dmg.sh` 本地构建
3. 手动上传 DMG 到 GitHub Releases

### 选项 4：只提供 Windows 版本

如果无法获得 macOS 构建环境：
1. 使用 `build_windows.bat` 打包 Windows 版本
2. 提供 Python 源码，让 macOS 用户自行运行

## 📞 获取帮助

- 查看 GitHub Actions 文档：https://docs.github.com/actions
- 查看 py2app 文档：https://py2app.readthedocs.io/
- 搜索类似问题：https://github.com/search

## ✅ 验证构建成功

构建成功的标志：

1. ✅ 所有步骤显示绿色勾号
2. ✅ 可以下载 "ImageCompressor-macOS" artifact
3. ✅ DMG 文件大小约 80-120 MB
4. ✅ 可以在 Mac 上打开和安装

---

**最后更新**：2026-01-05

**状态**：配置已更新，应该可以正常工作

**建议**：先尝试更新后的主配置，如果失败再使用简化版本调试
