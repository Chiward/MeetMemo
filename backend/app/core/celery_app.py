"""
Celery应用配置
"""

from celery import Celery
from .config import settings

# 创建Celery应用实例
celery_app = Celery(
    "meetmemo",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.audio_processing", "app.tasks.ai_processing"]
)

# Celery配置
celery_app.conf.update(
    # 任务序列化
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    
    # 任务路由
    task_routes={
        "process_audio_task": {"queue": "audio_processing"},
        "generate_meeting_summary": {"queue": "ai_summary"},
        "cleanup_temp_files": {"queue": "default"},
        "test_deepseek_connection": {"queue": "default"},
    },
    
    # 任务超时设置
    task_time_limit=settings.TASK_TIMEOUT,
    task_soft_time_limit=settings.TASK_TIMEOUT - 60,
    
    # 工作进程配置
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    
    # 结果过期时间
    result_expires=3600,
    
    # 任务重试配置
    task_default_retry_delay=60,
    task_max_retries=3,
    
    # 监控配置
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # 队列配置
    task_default_queue="default",
    task_queues={
        "default": {
            "exchange": "default",
            "routing_key": "default",
        },
        "audio_processing": {
            "exchange": "audio_processing",
            "routing_key": "audio_processing",
        },
        "transcription": {
            "exchange": "transcription", 
            "routing_key": "transcription",
        },
        "ai_summary": {
            "exchange": "ai_summary",
            "routing_key": "ai_summary",
        },
    },
)

# 自动发现任务
celery_app.autodiscover_tasks(["app.tasks"])

if __name__ == "__main__":
    celery_app.start()