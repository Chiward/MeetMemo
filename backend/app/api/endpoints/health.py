"""
健康检查API端点
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
import redis
import os
from datetime import datetime

from app.core.config import settings

router = APIRouter()

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """基础健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "MeetMemo Backend",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """详细健康检查，包含依赖服务状态"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "MeetMemo Backend",
        "version": "1.0.0",
        "dependencies": {}
    }
    
    # 检查Redis连接
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        health_status["dependencies"]["redis"] = {
            "status": "healthy",
            "url": settings.REDIS_URL.replace(settings.REDIS_URL.split('@')[0].split('//')[1] + '@', '***@') if '@' in settings.REDIS_URL else settings.REDIS_URL
        }
    except Exception as e:
        health_status["dependencies"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # 检查上传目录
    try:
        upload_dir = settings.UPLOAD_DIR
        if os.path.exists(upload_dir) and os.access(upload_dir, os.W_OK):
            health_status["dependencies"]["upload_directory"] = {
                "status": "healthy",
                "path": upload_dir,
                "writable": True
            }
        else:
            health_status["dependencies"]["upload_directory"] = {
                "status": "unhealthy",
                "path": upload_dir,
                "writable": False
            }
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["dependencies"]["upload_directory"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # 检查Whisper模型目录
    try:
        models_dir = settings.WHISPER_MODELS_DIR
        if os.path.exists(models_dir):
            health_status["dependencies"]["whisper_models"] = {
                "status": "healthy",
                "path": models_dir,
                "model": settings.WHISPER_MODEL
            }
        else:
            health_status["dependencies"]["whisper_models"] = {
                "status": "warning",
                "path": models_dir,
                "message": "Models directory not found, will be created on first use"
            }
    except Exception as e:
        health_status["dependencies"]["whisper_models"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # 检查DeepSeek API配置
    if settings.DEEPSEEK_API_KEY:
        health_status["dependencies"]["deepseek_api"] = {
            "status": "configured",
            "api_url": settings.DEEPSEEK_API_URL,
            "key_configured": True
        }
    else:
        health_status["dependencies"]["deepseek_api"] = {
            "status": "not_configured",
            "api_url": settings.DEEPSEEK_API_URL,
            "key_configured": False
        }
        health_status["status"] = "degraded"
    
    return health_status