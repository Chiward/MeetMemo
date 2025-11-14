#!/usr/bin/env python3
"""
重新下载Whisper turbo模型
"""

import whisper
import os
from pathlib import Path

def download_turbo():
    """下载turbo模型"""
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("📥 正在下载 turbo 模型...")
    
    try:
        # 清理可能的缓存
        cache_dir = os.path.expanduser("~/.cache/whisper")
        turbo_cache = os.path.join(cache_dir, "large-v3-turbo.pt")
        if os.path.exists(turbo_cache):
            os.remove(turbo_cache)
            print("🗑️ 清理了损坏的缓存文件")
        
        # 重新下载模型
        model = whisper.load_model("turbo", download_root=str(models_dir))
        print("✅ turbo 模型下载成功！")
        
        # 检查文件
        turbo_file = models_dir / "large-v3-turbo.pt"
        if turbo_file.exists():
            size_mb = turbo_file.stat().st_size / (1024 * 1024)
            print(f"📁 文件大小: {size_mb:.1f} MB")
        
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")

if __name__ == "__main__":
    download_turbo()