#!/usr/bin/env python3
"""
将Whisper模型从缓存复制到项目models文件夹
"""

import os
import shutil
import whisper
from pathlib import Path

def copy_models():
    """将模型从缓存复制到项目文件夹"""
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("📁 正在复制Whisper模型到项目文件夹...")
    
    # 获取缓存目录
    cache_dir = os.path.expanduser("~/.cache/whisper")
    print(f"🔍 缓存目录: {cache_dir}")
    
    # 要复制的模型
    models_to_copy = {
        "base": "base.pt",
        "turbo": "large-v3-turbo.pt"
    }
    
    for model_name, filename in models_to_copy.items():
        try:
            # 源文件路径
            source_path = os.path.join(cache_dir, filename)
            # 目标文件路径
            target_path = models_dir / filename
            
            print(f"\n📥 处理 {model_name} 模型...")
            
            if os.path.exists(source_path):
                # 复制文件
                shutil.copy2(source_path, target_path)
                
                if target_path.exists():
                    size_mb = target_path.stat().st_size / (1024 * 1024)
                    print(f"✅ {model_name} 模型复制成功！({size_mb:.1f} MB)")
                else:
                    print(f"❌ {model_name} 模型复制失败")
            else:
                print(f"⚠️ 在缓存中未找到 {filename}")
                
                # 尝试下载模型
                print(f"🔄 正在下载 {model_name} 模型...")
                model = whisper.load_model(model_name)
                
                # 再次尝试复制
                if os.path.exists(source_path):
                    shutil.copy2(source_path, target_path)
                    size_mb = target_path.stat().st_size / (1024 * 1024)
                    print(f"✅ {model_name} 模型下载并复制成功！({size_mb:.1f} MB)")
                
        except Exception as e:
            print(f"❌ 处理 {model_name} 模型时出错: {str(e)}")
    
    # 检查最终结果
    print(f"\n📋 检查models文件夹内容:")
    if models_dir.exists():
        total_size = 0
        file_count = 0
        for file in models_dir.iterdir():
            if file.is_file() and file.suffix == '.pt':
                size_mb = file.stat().st_size / (1024 * 1024)
                total_size += size_mb
                file_count += 1
                print(f"   ✅ {file.name} ({size_mb:.1f} MB)")
        
        if file_count > 0:
            print(f"\n📊 总计: {file_count} 个模型文件，总大小 {total_size:.1f} MB")
        else:
            print("   ❌ 没有找到模型文件")
    
    print("\n🎉 模型复制完成！")

if __name__ == "__main__":
    copy_models()