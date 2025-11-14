#!/usr/bin/env python3
"""
Whisper模型下载脚本
下载base和turbo模型到models文件夹
"""

import os
import sys
import shutil
import whisper
from pathlib import Path
import torch

def download_models():
    """下载Whisper模型到models文件夹"""
    
    # 确保models文件夹存在
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("🚀 开始下载Whisper模型...")
    print(f"📁 模型保存目录: {models_dir.absolute()}")
    
    # 要下载的模型列表
    models_to_download = ["base", "turbo"]
    
    for model_name in models_to_download:
        try:
            print(f"\n📥 正在下载 {model_name} 模型...")
            
            # 下载模型到默认位置
            model = whisper.load_model(model_name)
            
            # 获取模型文件的实际路径
            model_filename = f"{model_name}.pt" if model_name != "turbo" else "large-v3-turbo.pt"
            
            # 查找模型文件
            import whisper
            cache_dir = os.path.expanduser("~/.cache/whisper")
            
            # 尝试不同的可能路径
            possible_paths = [
                os.path.join(cache_dir, model_filename),
                os.path.join(os.path.dirname(whisper.__file__), "assets", model_filename),
            ]
            
            # 检查模型是否已经在当前目录
            local_path = models_dir / model_filename
            
            # 如果模型已经存在，跳过
            if local_path.exists():
                size_mb = local_path.stat().st_size / (1024 * 1024)
                print(f"✅ {model_name} 模型已存在 ({size_mb:.1f} MB)")
                continue
            
            # 保存模型到指定目录
            torch.save(model.state_dict(), local_path)
            
            if local_path.exists():
                size_mb = local_path.stat().st_size / (1024 * 1024)
                print(f"✅ {model_name} 模型下载完成！({size_mb:.1f} MB)")
            else:
                print(f"❌ {model_name} 模型保存失败")
            
        except Exception as e:
            print(f"❌ 下载 {model_name} 模型时出错: {str(e)}")
            continue
    
    # 检查下载的文件
    print(f"\n📋 检查models文件夹内容:")
    if models_dir.exists():
        total_size = 0
        for file in models_dir.iterdir():
            if file.is_file():
                size_mb = file.stat().st_size / (1024 * 1024)
                total_size += size_mb
                print(f"   - {file.name} ({size_mb:.1f} MB)")
        
        if total_size > 0:
            print(f"\n📊 总大小: {total_size:.1f} MB")
        else:
            print("   (文件夹为空)")
    
    print("\n🎉 模型下载完成！")

def test_models():
    """测试模型加载"""
    print("\n🧪 测试模型加载...")
    
    models_dir = Path("models")
    
    for model_file in models_dir.glob("*.pt"):
        try:
            print(f"📝 测试加载: {model_file.name}")
            
            # 根据文件名确定模型名称
            if "turbo" in model_file.name:
                model_name = "turbo"
            else:
                model_name = model_file.stem
            
            # 尝试加载模型
            model = whisper.load_model(model_name)
            print(f"✅ {model_name} 模型加载成功")
            
        except Exception as e:
            print(f"❌ 加载 {model_file.name} 失败: {str(e)}")

if __name__ == "__main__":
    download_models()
    test_models()