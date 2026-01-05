# 测试 GitHub Actions 构建

## 🚀 快速测试步骤

### 步骤 1：提交更新的文件

```bash
# 添加更新的文件
git add .github/workflows/build-macos.yml
git add setup.py
git add GITHUB_ACTIONS_故障排查.md
git commit -m "Fix GitHub Actions build configuration"

# 推送到 GitHub
git push origin main
```

**注意**：如果你的主分支是 `master` 而不是 `main`，使用：
```bash
git push origin master
```

### 步骤 2：查看构建状态

1. 访问你的 GitHub 仓库
2. 点击顶部的 **"Actions"** 标签
3. 你会看到一个新的 workflow run 正在运行
4. 点击进入查看详细进度

### 步骤 3：等待构建完成

构建通常需要 **6-10 分钟**，包括：
- ✅ 安装依赖（2-3 分钟）
- ✅ 构建应用（3-5 分钟）
- ✅ 创建 DMG（1-2 分钟）

### 步骤 4：下载构建产物

构建成功后：
1. 在 workflow run 页面向下滚动
2. 找到 **"Artifacts"** 部分
3. 点击 **"ImageCompressor-macOS"** 下载 DMG 文件

## 🔍 如果构建失败

### 查看错误日志

1. 点击失败的步骤（红色 ❌）
2. 展开查看详细错误信息
3. 记录错误信息

### 常见错误和解决方案

#### 错误 1：py2app 构建失败

**错误信息**：
```
error: [Errno 2] No such file or directory: 'dist/main.app'
```

**解决方案**：
使用简化版本的 workflow：

```bash
# 在 GitHub Actions 页面
# 选择 "Build macOS DMG (Simple)"
# 点击 "Run workflow" 按钮
```

#### 错误 2：依赖安装失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement
```

**解决方案**：
检查 `requirements.txt`，确保版本号正确：

```txt
Pillow>=10.0.0
PySide6>=6.5.0
py2app>=0.28.0
```

#### 错误 3：权限问题

**错误信息**：
```
Permission denied
```

**解决方案**：
这通常是 GitHub Actions 环境问题，已在配置中修复。

## 🧪 手动触发构建

如果你想手动触发构建（不推送代码）：

1. 访问 GitHub 仓库的 **Actions** 页面
2. 在左侧选择 **"Build macOS DMG"**
3. 点击右上角的 **"Run workflow"** 按钮
4. 选择分支（通常是 `main` 或 `master`）
5. 点击绿色的 **"Run workflow"** 按钮

## 📊 构建状态说明

### 🟢 成功（Success）
- 所有步骤都有绿色勾号 ✅
- 可以下载 DMG 文件
- 构建时间：6-10 分钟

### 🔴 失败（Failure）
- 某个步骤有红色叉号 ❌
- 查看该步骤的日志
- 参考 `GITHUB_ACTIONS_故障排查.md`

### 🟡 进行中（In Progress）
- 黄色圆圈动画
- 等待完成
- 可以实时查看日志

## 🎯 验证 DMG 文件

下载 DMG 后，在 Mac 上验证：

```bash
# 1. 双击打开 DMG
open ImageCompressor.dmg

# 2. 拖拽应用到 Applications 文件夹

# 3. 从 Applications 运行
open /Applications/ImageCompressor.app

# 4. 如果提示"无法打开"，右键点击 → 打开
```

## 🔄 更新配置后重新测试

如果修改了配置文件：

```bash
# 1. 修改文件
# 2. 提交更改
git add .github/workflows/build-macos.yml
git commit -m "Update build configuration"
git push

# 3. 等待新的构建运行
# 4. 查看结果
```

## 📝 调试技巧

### 技巧 1：查看完整日志

点击每个步骤可以展开查看详细输出：
- 依赖安装日志
- 构建过程日志
- 错误堆栈信息

### 技巧 2：使用简化版本

简化版本会上传构建日志：

```yaml
# .github/workflows/build-macos-simple.yml
- name: Upload build log
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: build-log
    path: build.log
```

下载 `build-log` artifact 查看详细信息。

### 技巧 3：本地模拟

在本地 Mac 上模拟 GitHub Actions 环境：

```bash
# 使用相同的 Python 版本
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 构建
python setup.py py2app

# 检查结果
ls -la dist/
```

## 🆘 如果持续失败

### 选项 1：使用 Issue 报告

在 GitHub 仓库创建 Issue，包含：
```
标题：GitHub Actions 构建失败

内容：
- 错误日志（复制粘贴）
- 使用的配置文件
- 已尝试的解决方案
```

### 选项 2：暂时禁用自动构建

如果不需要自动构建：

```yaml
# 修改 .github/workflows/build-macos.yml
on:
  # push:  # 注释掉自动触发
  #   branches: [ main, master ]
  workflow_dispatch:  # 只保留手动触发
```

### 选项 3：使用本地构建

如果有 Mac 电脑：
```bash
./build_dmg.sh
```

如果没有 Mac：
- 借用朋友的 Mac
- 使用云端 macOS 服务
- 只提供 Windows 版本

## ✅ 成功标志

构建成功后，你应该看到：

1. ✅ 所有步骤都是绿色
2. ✅ "Artifacts" 部分有 "ImageCompressor-macOS"
3. ✅ DMG 文件大小约 80-120 MB
4. ✅ 可以在 Mac 上正常安装和运行

## 📞 获取更多帮助

- 详细故障排查：`GITHUB_ACTIONS_故障排查.md`
- GitHub Actions 文档：https://docs.github.com/actions
- py2app 文档：https://py2app.readthedocs.io/

---

**提示**：首次构建可能需要更长时间，因为需要下载所有依赖。后续构建会更快。

**建议**：先尝试主配置文件，如果失败再使用简化版本进行调试。
