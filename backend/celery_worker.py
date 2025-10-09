#!/usr/bin/env python3
"""
Celery Worker启动脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.celery_app import celery_app

if __name__ == "__main__":
    # 设置环境变量
    os.environ.setdefault("CELERY_APP", "app.core.celery_app:celery_app")
    
    # 启动Celery worker
    celery_app.worker_main([
        "worker",
        "--loglevel=info",
        "--concurrency=2",
        "--queues=default,audio_processing,transcription,ai_summary",
        "--hostname=worker@%h"
    ])