"""
MeetMemo Backend - FastAPI Application
AI智能会议纪要生成助手后端服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from pathlib import Path

from app.core.config import settings
from app.api import api_router

# 创建FastAPI应用实例
app = FastAPI(
    title="MeetMemo API",
    description="AI智能会议纪要生成助手 - 后端API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(exist_ok=True)

# 挂载静态文件服务
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# 注册API路由
app.include_router(api_router, prefix="/api")

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "MeetMemo Backend",
        "version": "1.0.0"
    }

# 根路径
@app.get("/")
async def root():
    """根路径信息"""
    return {
        "message": "MeetMemo API Server",
        "docs": "/docs",
        "health": "/health"
    }

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )