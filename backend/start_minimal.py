#!/usr/bin/env python3
"""
MeetMemo 后端最小化启动脚本
只安装核心依赖，快速启动开发环境
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🎯 MeetMemo 后端最小化启动")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 创建必要的目录
    directories = ["uploads", "models", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 创建目录: {directory}")
    
    # 安装最小化依赖
    print("📦 安装最小化依赖...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements_minimal.txt"
        ], check=True)
        print("✅ 依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return
    
    # 启动后端服务
    print("🚀 启动后端服务...")
    print("📍 服务地址: http://localhost:8000")
    print("📍 API文档: http://localhost:8000/docs")
    print("📍 健康检查: http://localhost:8000/health")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")

if __name__ == "__main__":
    main()