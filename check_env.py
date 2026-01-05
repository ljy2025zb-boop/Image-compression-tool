#!/usr/bin/env python3
"""
环境检查脚本
验证所有依赖是否正确安装
"""
import sys
import platform


def check_python_version():
    """检查 Python 版本"""
    print("检查 Python 版本...")
    version = sys.version_info
    print(f"  当前版本: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ❌ 需要 Python 3.8 或更高版本")
        return False
    else:
        print("  ✅ Python 版本符合要求")
        return True


def check_platform():
    """检查操作系统"""
    print("\n检查操作系统...")
    system = platform.system()
    print(f"  当前系统: {system}")
    
    if system != "Darwin":
        print("  ⚠️  警告: 此应用专为 macOS 设计")
        print("  在其他系统上可能无法正常打包为 DMG")
    else:
        print("  ✅ macOS 系统")
    
    return True


def check_module(module_name, import_name=None):
    """检查模块是否安装"""
    if import_name is None:
        import_name = module_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', '未知')
        print(f"  ✅ {module_name}: {version}")
        return True
    except ImportError:
        print(f"  ❌ {module_name}: 未安装")
        return False


def check_dependencies():
    """检查所有依赖"""
    print("\n检查依赖包...")
    
    modules = [
        ('Pillow', 'PIL'),
        ('PySide6', 'PySide6'),
        ('py2app', 'py2app'),
    ]
    
    all_ok = True
    for module_name, import_name in modules:
        if not check_module(module_name, import_name):
            all_ok = False
    
    return all_ok


def check_optional_tools():
    """检查可选工具"""
    print("\n检查可选工具...")
    
    import subprocess
    
    # 检查 create-dmg
    try:
        result = subprocess.run(
            ['which', 'create-dmg'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  ✅ create-dmg: 已安装")
        else:
            print("  ⚠️  create-dmg: 未安装（可选）")
            print("     安装命令: brew install create-dmg")
    except Exception:
        print("  ⚠️  create-dmg: 未安装（可选）")
    
    # 检查 brew
    try:
        result = subprocess.run(
            ['which', 'brew'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  ✅ Homebrew: 已安装")
        else:
            print("  ⚠️  Homebrew: 未安装（推荐）")
    except Exception:
        print("  ⚠️  Homebrew: 未安装（推荐）")


def check_project_files():
    """检查项目文件"""
    print("\n检查项目文件...")
    
    from pathlib import Path
    
    required_files = [
        'main.py',
        'gui.py',
        'compressor.py',
        'setup.py',
        'requirements.txt',
        'build_dmg.sh',
    ]
    
    all_ok = True
    for filename in required_files:
        if Path(filename).exists():
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename}: 文件不存在")
            all_ok = False
    
    return all_ok


def main():
    """主函数"""
    print("=" * 60)
    print("图片压缩工具 - 环境检查")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_platform(),
        check_dependencies(),
        check_project_files(),
    ]
    
    check_optional_tools()
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("✅ 所有检查通过！")
        print("\n下一步:")
        print("  1. 运行应用: python main.py")
        print("  2. 打包 DMG: ./build_dmg.sh")
    else:
        print("❌ 部分检查未通过")
        print("\n请先解决以下问题:")
        print("  1. 安装缺失的依赖: pip install -r requirements.txt")
        print("  2. 确保所有项目文件完整")
    
    print("=" * 60)
    
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
