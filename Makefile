# Makefile for Image Compressor
# 简化常用命令

.PHONY: help install run test build clean icon

help:
	@echo "图片压缩工具 - 可用命令："
	@echo ""
	@echo "  make install    - 安装依赖"
	@echo "  make run        - 运行应用"
	@echo "  make test       - 运行测试（需要指定 FOLDER 参数）"
	@echo "  make build      - 打包为 DMG"
	@echo "  make icon       - 生成应用图标"
	@echo "  make clean      - 清理构建文件"
	@echo ""
	@echo "示例："
	@echo "  make test FOLDER=~/Pictures/test"
	@echo ""

install:
	@echo "安装 Python 依赖..."
	pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

run:
	@echo "启动应用..."
	python main.py

test:
	@echo "运行测试..."
	@if [ -z "$(FOLDER)" ]; then \
		echo "错误: 请指定 FOLDER 参数"; \
		echo "示例: make test FOLDER=~/Pictures/test"; \
		exit 1; \
	fi
	python test_app.py $(FOLDER)

build:
	@echo "开始打包..."
	chmod +x build_dmg.sh
	./build_dmg.sh
	@echo "✅ 打包完成: dist/ImageCompressor.dmg"

icon:
	@echo "生成应用图标..."
	@if [ ! -f "icon.png" ]; then \
		echo "错误: 未找到 icon.png 文件"; \
		echo "请准备一个 1024x1024 的 PNG 图片"; \
		exit 1; \
	fi
	chmod +x create_icon.sh
	./create_icon.sh
	@echo "✅ 图标生成完成: icon.icns"

clean:
	@echo "清理构建文件..."
	rm -rf build dist *.egg-info
	rm -rf __pycache__ */__pycache__
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".DS_Store" -delete
	@echo "✅ 清理完成"
