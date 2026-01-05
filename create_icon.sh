#!/bin/bash
# 创建 macOS 应用图标 (.icns)
# 需要一个 1024x1024 的 PNG 图片作为源文件

echo "=========================================="
echo "macOS 图标生成脚本"
echo "=========================================="
echo ""
echo "使用说明:"
echo "1. 准备一个 1024x1024 的 PNG 图片，命名为 icon.png"
echo "2. 运行此脚本: ./create_icon.sh"
echo ""

# 检查是否存在源图片
if [ ! -f "icon.png" ]; then
    echo "错误: 未找到 icon.png 文件"
    echo ""
    echo "请准备一个 1024x1024 的 PNG 图片并命名为 icon.png"
    echo "或者跳过此步骤，应用将使用默认图标"
    exit 1
fi

# 创建临时目录
mkdir -p icon.iconset

# 生成各种尺寸的图标
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# 生成 .icns 文件
iconutil -c icns icon.iconset

# 清理临时文件
rm -rf icon.iconset

echo ""
echo "✅ 图标生成成功: icon.icns"
echo ""
