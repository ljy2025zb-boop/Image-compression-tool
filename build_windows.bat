@echo off
REM Windows 打包脚本
REM 将 Python 应用打包为 Windows .exe 可执行文件

echo ==========================================
echo 图片压缩工具 - Windows 打包脚本
echo ==========================================

REM 清理旧的构建文件
echo.
echo 1. 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM 检查 PyInstaller
echo.
echo 2. 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
) else (
    echo PyInstaller 已安装
)

REM 打包应用
echo.
echo 3. 打包为 Windows 应用...
pyinstaller --name="ImageCompressor" ^
            --windowed ^
            --onefile ^
            --add-data "README.md;." ^
            --hidden-import=PySide6 ^
            --hidden-import=PIL ^
            --collect-all PySide6 ^
            --collect-all PIL ^
            main.py

REM 检查是否成功
if exist "dist\ImageCompressor.exe" (
    echo.
    echo ==========================================
    echo 打包成功！
    echo ==========================================
    echo.
    echo EXE 文件位置: dist\ImageCompressor.exe
    echo.
    echo 使用说明:
    echo 1. 双击运行 dist\ImageCompressor.exe
    echo 2. 或者将整个 dist 文件夹分发给其他用户
    echo.
) else (
    echo.
    echo ==========================================
    echo 打包失败！
    echo ==========================================
    echo.
    echo 请检查错误信息并重试
    echo.
)

pause
