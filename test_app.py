#!/usr/bin/env python3
"""
测试脚本 - 用于快速测试压缩功能
无需 GUI，直接命令行测试
"""
import sys
from pathlib import Path
from compressor import ImageCompressor


def test_compression(folder_path):
    """测试压缩功能"""
    print("=" * 60)
    print("图片压缩测试")
    print("=" * 60)
    print(f"\n测试文件夹: {folder_path}\n")
    
    def progress_callback(current, total, filename):
        """进度回调"""
        print(f"[{current}/{total}] 正在处理: {filename}")
    
    # 创建压缩器
    compressor = ImageCompressor(progress_callback=progress_callback)
    
    # 查找图片
    print("正在扫描图片文件...")
    images = compressor.find_images(folder_path)
    print(f"找到 {len(images)} 张图片\n")
    
    if len(images) == 0:
        print("未找到任何图片文件")
        return
    
    # 显示找到的图片
    print("图片列表:")
    for i, img in enumerate(images[:10], 1):  # 只显示前 10 个
        print(f"  {i}. {img.name}")
    if len(images) > 10:
        print(f"  ... 还有 {len(images) - 10} 张图片")
    
    print("\n开始压缩...\n")
    
    # 执行压缩
    success, fail = compressor.process_folder(folder_path)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("压缩完成！")
    print("=" * 60)
    print(f"成功: {success} 张")
    print(f"失败: {fail} 张")
    
    if compressor.errors:
        print(f"\n错误详情:")
        for error in compressor.errors:
            print(f"  - {error}")
    
    print(f"\n输出目录: {folder_path}/compressed_png/")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python test_app.py <文件夹路径>")
        print("\n示例:")
        print("  python test_app.py ~/Pictures/test")
        print("  python test_app.py /Users/username/Desktop/images")
        sys.exit(1)
    
    folder = sys.argv[1]
    
    if not Path(folder).exists():
        print(f"错误: 文件夹不存在: {folder}")
        sys.exit(1)
    
    if not Path(folder).is_dir():
        print(f"错误: 不是一个文件夹: {folder}")
        sys.exit(1)
    
    test_compression(folder)
