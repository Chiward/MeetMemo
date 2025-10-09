"""
Celery应用配置
"""

from celery import Celery
from app.core.config import settings

# 创建Celery应用实例
celery_app = Celery(
    "meetmemo",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.audio_processing",
        "app.tasks.ai_processing"
    ]
)

# Celery配置
celery_app.conf.update(
    # 任务序列化
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    
    # 时区设置
    timezone="UTC",
    enable_utc=True,
    
    # 任务路由
    task_routes={
        "app.tasks.audio_processing.*": {"queue": "audio"},
        "app.tasks.ai_processing.*": {"queue": "ai"},
    },
    
    # 任务超时设置
    task_time_limit=settings.TASK_TIMEOUT,
    task_soft_time_limit=settings.TASK_TIMEOUT - 60,
    
    # 工作进程设置
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # 结果过期时间
    result_expires=3600,
    
    # 任务重试设置
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # 监控设置
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# 队列配置
celery_app.conf.task_default_queue = "default"
celery_app.conf.task_queues = {
    "default": {
        "exchange": "default",
        "routing_key": "default",
    },
    "audio": {
        "exchange": "audio",
        "routing_key": "audio",
    },
    "ai": {
        "exchange": "ai", 
        "routing_key": "ai",
    },
}

if __name__ == "__main__":
    celery_app.start()