"""
简化的 Celery Worker 启动脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ.setdefault("PYTHONPATH", str(project_root))

if __name__ == "__main__":
    from app.core.celery_app import celery_app
    
    # 使用更简单的启动方式
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--concurrency=1',  # 减少并发数
        '--pool=solo',      # 使用 solo 池而不是 prefork
        '--hostname=worker@%h',
    ])