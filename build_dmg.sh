#!/bin/bash
# DMG 打包脚本
# 将 Python 应用打包为可分发的 .dmg 文件

set -e  # 遇到错误立即退出

echo "=========================================="
echo "图片压缩工具 - DMG 打包脚本"
echo "=========================================="

# 清理旧的构建文件
echo ""
echo "1. 清理旧的构建文件..."
rm -rf build dist

# 使用 py2app 构建 .app
echo ""
echo "2. 使用 py2app 构建 macOS 应用..."
python setup.py py2app

# 检查 .app 是否生成成功
if [ ! -d "dist/main.app" ]; then
    echo "错误: .app 文件生成失败"
    exit 1
fi

# 重命名 .app
echo ""
echo "3. 重命名应用..."
mv "dist/main.app" "dist/图片压缩工具.app"

# 创建 DMG
echo ""
echo "4. 创建 DMG 文件..."

# 检查是否安装了 create-dmg
if ! command -v create-dmg &> /dev/null; then
    echo "警告: 未安装 create-dmg，使用 hdiutil 创建简单 DMG"
    
    # 使用 hdiutil 创建 DMG
    hdiutil create -volname "图片压缩工具" \
        -srcfolder "dist/图片压缩工具.app" \
        -ov -format UDZO \
        "dist/ImageCompressor.dmg"
else
    # 使用 create-dmg 创建更专业的 DMG
    create-dmg \
        --volname "图片压缩工具" \
        --volicon "icon.icns" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "图片压缩工具.app" 175 120 \
        --hide-extension "图片压缩工具.app" \
        --app-drop-link 425 120 \
        --no-internet-enable \
        "dist/ImageCompressor.dmg" \
        "dist/图片压缩工具.app" || {
            echo "create-dmg 失败，使用 hdiutil 备用方案..."
            hdiutil create -volname "图片压缩工具" \
                -srcfolder "dist/图片压缩工具.app" \
                -ov -format UDZO \
                "dist/ImageCompressor.dmg"
        }
fi

echo ""
echo "=========================================="
echo "✅ 打包完成！"
echo "=========================================="
echo ""
echo "DMG 文件位置: dist/ImageCompressor.dmg"
echo ""
echo "安装说明:"
echo "1. 双击打开 ImageCompressor.dmg"
echo "2. 将应用拖拽到 Applications 文件夹"
echo "3. 从启动台或 Applications 文件夹启动应用"
echo ""
