"""
API路由模块
"""

from fastapi import APIRouter
from .endpoints import upload, tasks, health

# 创建主API路由器
api_router = APIRouter()

# 注册各个端点路由
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

__all__ = ["api_router"]