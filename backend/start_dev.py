#!/usr/bin/env python3
"""
开发环境启动脚本
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_redis_connection():
    """检查Redis连接"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis连接成功")
        return True
    except Exception as e:
        print(f"❌ Redis连接失败: {e}")
        print("请参考 REDIS_SETUP.md 安装Redis")
        return False

def install_dependencies():
    """安装依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def create_directories():
    """创建必要的目录"""
    directories = ["uploads", "models", "logs"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 创建目录: {dir_name}")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    try:
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ]
        # 仅在开发环境下启用 reload，打包环境下禁用
        if os.environ.get("MEETMEMO_ENV") == "development":
             cmd.append("--reload")
             
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 服务启动失败: {e}")

def main():
    """主函数"""
    print("🎯 MeetMemo 后端开发环境启动")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 安装依赖 (已由start_app.bat处理，此处跳过以加快启动速度)
    # if not install_dependencies():
    #     sys.exit(1)
    
    # 检查Redis（可选）
    redis_available = check_redis_connection()
    if not redis_available:
        print("⚠️  Redis未启动，Celery任务功能将不可用")
        print("   基本API功能仍可正常使用")
        time.sleep(2)
    
    # 启动服务
    start_backend()

if __name__ == "__main__":
    main()