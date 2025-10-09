"""
任务处理模块
包含音频处理和AI处理任务
"""

from app.core.celery_app import celery_app
from .audio_processing import process_audio_task, cleanup_temp_files
from .ai_processing import generate_meeting_summary, test_deepseek_connection

__all__ = [
    "celery_app",
    "process_audio_task", 
    "cleanup_temp_files",
    "generate_meeting_summary",
    "test_deepseek_connection"
]