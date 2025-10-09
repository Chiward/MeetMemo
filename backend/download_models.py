#!/usr/bin/env python3
"""
下载Whisper模型脚本
"""

import os
import sys
import whisper
import torch
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def download_whisper_model(model_name: str):
    """
    下载指定的Whisper模型
    
    Args:
        model_name: 模型名称 (base, large, turbo)
    """
    try:
        print(f"🔄 开始下载 {model_name} 模型...")
        
        # 设置设备
        device = "cuda" if torch.cuda.is_available() and settings.WHISPER_DEVICE == "cuda" else "cpu"
        print(f"📱 使用设备: {device}")
        
        # 确保模型目录存在
        models_dir = Path(settings.WHISPER_MODELS_DIR)
        models_dir.mkdir(exist_ok=True)
        print(f"📁 模型目录: {models_dir}")
        
        # 下载并加载模型
        model = whisper.load_model(
            model_name,
            device=device,
            download_root=str(models_dir)
        )
        
        print(f"✅ {model_name} 模型下载完成！")
        
        # 显示模型信息
        model_info = {
            "base": {"params": "74M", "vram": "~1GB", "speed": "~7x"},
            "large": {"params": "1550M", "vram": "~10GB", "speed": "1x"},
            "turbo": {"params": "809M", "vram": "~6GB", "speed": "~8x"}
        }
        
        if model_name in model_info:
            info = model_info[model_name]
            print(f"📊 模型参数: {info['params']}, 显存需求: {info['vram']}, 相对速度: {info['speed']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 下载 {model_name} 模型失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🎯 Whisper模型下载工具")
    print("=" * 50)
    
    # 检查当前已有的模型
    models_dir = Path(settings.WHISPER_MODELS_DIR)
    if models_dir.exists():
        existing_models = list(models_dir.glob("*.pt"))
        if existing_models:
            print("📦 当前已有模型:")
            for model_file in existing_models:
                print(f"  - {model_file.name}")
        else:
            print("📦 当前没有已下载的模型")
    
    print("\n🔄 开始下载缺失的模型...")
    
    # 要下载的模型列表
    models_to_download = ["base", "large", "turbo"]
    
    success_count = 0
    total_count = len(models_to_download)
    
    for model_name in models_to_download:
        print(f"\n{'='*30}")
        if download_whisper_model(model_name):
            success_count += 1
        print(f"{'='*30}")
    
    print(f"\n🎉 模型下载完成！")
    print(f"✅ 成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎊 所有模型下载成功！现在可以在前端选择不同的Whisper模型了。")
    else:
        print("⚠️  部分模型下载失败，请检查网络连接或重试。")
    
    # 显示最终的模型目录内容
    print(f"\n📁 最终模型目录内容 ({models_dir}):")
    if models_dir.exists():
        for item in models_dir.iterdir():
            if item.is_file():
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"  - {item.name} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    main()