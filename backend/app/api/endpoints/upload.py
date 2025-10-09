"""
文件上传API端点
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from typing import Dict, Any
import os
import uuid
from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.tasks.audio_processing import process_audio_task

router = APIRouter()

def validate_audio_file(file: UploadFile) -> bool:
    """验证音频文件格式"""
    # 检查文件扩展名
    file_extension = Path(file.filename).suffix.lower().lstrip('.')
    if file_extension not in settings.ALLOWED_AUDIO_FORMATS:
        return False
    
    return True

def get_file_type(file_path: str) -> str:
    """获取文件MIME类型"""
    try:
        # 简单的基于扩展名的MIME类型检测
        file_extension = Path(file_path).suffix.lower()
        mime_types = {
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.flac': 'audio/flac',
            '.m4a': 'audio/mp4',
            '.aac': 'audio/aac',
            '.ogg': 'audio/ogg',
            '.wma': 'audio/x-ms-wma'
        }
        return mime_types.get(file_extension, "audio/unknown")
    except:
        return "unknown"

@router.post("/audio")
async def upload_audio_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    meeting_title: str = Form(None),
    language: str = Form("auto"),
    whisper_model: str = Form("base")
) -> Dict[str, Any]:
    """
    上传音频文件并启动处理任务
    
    Args:
        file: 音频文件
        meeting_title: 会议标题（可选）
        language: 转录语言（默认自动检测）
        whisper_model: Whisper模型类型（base/large/turbo，默认base）
    
    Returns:
        包含任务ID和文件信息的响应
    """
    
    # 验证文件
    if not file.filename:
        raise HTTPException(status_code=400, detail="未选择文件")
    
    if not validate_audio_file(file):
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件格式。支持的格式: {', '.join(settings.ALLOWED_AUDIO_FORMATS)}"
        )
    
    # 检查文件大小
    file_content = await file.read()
    if len(file_content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"文件过大。最大允许大小: {settings.MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
        )
    
    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix.lower()
    unique_filename = f"{file_id}{file_extension}"
    file_path = Path(settings.UPLOAD_DIR) / unique_filename
    
    try:
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # 获取文件信息
        file_info = {
            "file_id": file_id,
            "original_filename": file.filename,
            "file_path": str(file_path),
            "file_size": len(file_content),
            "file_type": get_file_type(str(file_path)),
            "upload_time": datetime.utcnow().isoformat(),
            "meeting_title": meeting_title or f"会议录音_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "language": language,
            "whisper_model": whisper_model
        }
        
        # 检查是否为最小化模式（没有Celery）
        try:
            # 尝试启动后台处理任务
            task_result = process_audio_task.delay(
                file_path=str(file_path),
                file_info=file_info
            )
            
            return {
                "success": True,
                "message": "文件上传成功，正在处理中",
                "task_id": task_result.id,
                "file_info": {
                    "file_id": file_id,
                    "original_filename": file.filename,
                    "file_size": len(file_content),
                    "meeting_title": file_info["meeting_title"],
                    "language": language,
                    "upload_time": file_info["upload_time"]
                }
            }
        except Exception as celery_error:
            # Celery不可用，返回最小化响应
            return {
                "success": True,
                "message": "文件上传成功（最小化模式）",
                "task_id": f"minimal_{file_id}",
                "file_info": {
                    "file_id": file_id,
                    "original_filename": file.filename,
                    "file_size": len(file_content),
                    "meeting_title": file_info["meeting_title"],
                    "language": language,
                    "upload_time": file_info["upload_time"]
                },
                "note": "当前为最小化模式，音频处理功能需要完整部署才能使用"
            }
        
    except Exception as e:
        # 清理已上传的文件
        if file_path.exists():
            file_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"文件处理失败: {str(e)}"
        )

@router.delete("/audio/{file_id}")
async def delete_audio_file(file_id: str) -> Dict[str, Any]:
    """删除上传的音频文件"""
    
    # 查找文件
    upload_dir = Path(settings.UPLOAD_DIR)
    file_pattern = f"{file_id}.*"
    
    matching_files = list(upload_dir.glob(file_pattern))
    
    if not matching_files:
        raise HTTPException(status_code=404, detail="文件未找到")
    
    try:
        # 删除文件
        for file_path in matching_files:
            file_path.unlink()
        
        return {
            "success": True,
            "message": "文件删除成功",
            "file_id": file_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件删除失败: {str(e)}"
        )

@router.get("/formats")
async def get_supported_formats() -> Dict[str, Any]:
    """获取支持的音频格式列表"""
    return {
        "supported_formats": settings.ALLOWED_AUDIO_FORMATS,
        "max_file_size": settings.MAX_FILE_SIZE,
        "max_file_size_mb": round(settings.MAX_FILE_SIZE / 1024 / 1024, 1)
    }