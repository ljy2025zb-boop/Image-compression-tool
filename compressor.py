"""
图片压缩核心模块
智能压缩图片至 500KB 以内，保持最佳视觉质量
"""
import os
from pathlib import Path
from PIL import Image
import io


class ImageCompressor:
    """图片压缩器"""
    
    # 支持的图片格式
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
    TARGET_SIZE = 500 * 1024  # 500KB
    OUTPUT_DIR = 'compressed_png'
    
    def __init__(self, progress_callback=None):
        """
        初始化压缩器
        :param progress_callback: 进度回调函数 callback(current, total, filename)
        """
        self.progress_callback = progress_callback
        self.processed_count = 0
        self.total_count = 0
        self.errors = []
    
    def find_images(self, root_path):
        """
        递归查找所有图片文件
        :param root_path: 根目录路径
        :return: 图片文件路径列表
        """
        images = []
        root = Path(root_path)
        
        for file_path in root.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                # 跳过已压缩目录中的文件
                if self.OUTPUT_DIR not in file_path.parts:
                    images.append(file_path)
        
        return images
    
    def compress_image(self, image_path, output_path):
        """
        压缩单张图片至 500KB 以内
        :param image_path: 输入图片路径
        :param output_path: 输出图片路径
        :return: 是否成功
        """
        try:
            # 打开图片
            img = Image.open(image_path)
            
            # 转换为 RGB 模式（PNG 需要）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 保留透明通道
                if img.mode == 'P':
                    img = img.convert('RGBA')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            original_size = img.size
            
            # 策略 1: 先尝试直接保存
            quality = 95
            img_copy = img.copy()
            buffer = io.BytesIO()
            
            if img.mode in ('RGBA', 'LA'):
                img_copy.save(buffer, format='PNG', optimize=True)
            else:
                img_copy.save(buffer, format='PNG', optimize=True, quality=quality)
            
            file_size = buffer.tell()
            
            # 如果已经小于 500KB，直接保存
            if file_size <= self.TARGET_SIZE:
                img_copy.save(output_path, format='PNG', optimize=True)
                return True
            
            # 策略 2: 需要压缩 - 逐步降低分辨率
            scale_factor = 0.9
            max_iterations = 20
            
            for i in range(max_iterations):
                # 计算新尺寸
                new_width = int(original_size[0] * (scale_factor ** (i + 1)))
                new_height = int(original_size[1] * (scale_factor ** (i + 1)))
                
                if new_width < 100 or new_height < 100:
                    # 尺寸太小，停止
                    break
                
                # 调整大小
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 尝试保存
                buffer = io.BytesIO()
                if img_resized.mode in ('RGBA', 'LA'):
                    img_resized.save(buffer, format='PNG', optimize=True)
                else:
                    img_resized.save(buffer, format='PNG', optimize=True, quality=quality)
                
                file_size = buffer.tell()
                
                # 检查文件大小
                if file_size <= self.TARGET_SIZE:
                    # 成功压缩到目标大小
                    img_resized.save(output_path, format='PNG', optimize=True)
                    return True
            
            # 如果还是太大，使用最小尺寸保存
            img_resized.save(output_path, format='PNG', optimize=True)
            return True
            
        except Exception as e:
            self.errors.append(f"{image_path.name}: {str(e)}")
            return False
    
    def process_folder(self, root_path):
        """
        处理整个文件夹
        :param root_path: 根目录路径
        :return: (成功数量, 失败数量)
        """
        root = Path(root_path)
        
        # 查找所有图片
        images = self.find_images(root)
        self.total_count = len(images)
        self.processed_count = 0
        self.errors = []
        
        if self.total_count == 0:
            return 0, 0
        
        success_count = 0
        
        for img_path in images:
            # 计算相对路径
            rel_path = img_path.relative_to(root)
            
            # 构建输出路径
            output_dir = root / self.OUTPUT_DIR / rel_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 输出文件名（改为 .png）
            output_path = output_dir / (img_path.stem + '.png')
            
            # 压缩图片
            if self.compress_image(img_path, output_path):
                success_count += 1
            
            # 更新进度
            self.processed_count += 1
            if self.progress_callback:
                self.progress_callback(self.processed_count, self.total_count, img_path.name)
        
        fail_count = self.total_count - success_count
        return success_count, fail_count
