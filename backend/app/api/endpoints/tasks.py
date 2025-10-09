"""
任务状态查询API端点
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from celery.result import AsyncResult
from datetime import datetime

from app.core.config import settings
from app.core.celery_app import celery_app

router = APIRouter()

@router.get("/{task_id}")
async def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    获取任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        任务状态信息
    """
    try:
        # 检查是否为最小化模式的任务ID
        if task_id.startswith("minimal_"):
            return {
                "task_id": task_id,
                "status": "completed",
                "message": "文件上传完成（最小化模式）",
                "result": {
                    "status": "minimal_mode",
                    "message": "当前为最小化模式，音频处理功能需要完整部署才能使用",
                    "file_uploaded": True
                }
            }
        
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state == 'PENDING':
            response = {
                "task_id": task_id,
                "status": "pending",
                "message": "任务等待处理中"
            }
        elif task_result.state == 'PROGRESS':
            response = {
                "task_id": task_id,
                "status": "processing",
                "message": "任务处理中",
                "progress": task_result.info.get('progress', 0),
                "current_step": task_result.info.get('current_step', ''),
                "total_steps": task_result.info.get('total_steps', 0)
            }
        elif task_result.state == 'SUCCESS':
            result = task_result.result
            response = {
                "task_id": task_id,
                "status": "completed",
                "message": "任务完成",
                "result": result
            }
        elif task_result.state == 'FAILURE':
            response = {
                "task_id": task_id,
                "status": "failed",
                "message": "任务失败",
                "error": str(task_result.info)
            }
        else:
            response = {
                "task_id": task_id,
                "status": task_result.state.lower(),
                "message": f"任务状态: {task_result.state}"
            }
            
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取任务状态失败: {str(e)}"
        )

@router.delete("/{task_id}")
async def cancel_task(task_id: str) -> Dict[str, Any]:
    """
    取消任务
    
    Args:
        task_id: 任务ID
        
    Returns:
        取消结果
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state in ['PENDING', 'PROGRESS']:
            task_result.revoke(terminate=True)
            return {
                "task_id": task_id,
                "status": "cancelled",
                "message": "任务已取消"
            }
        else:
            return {
                "task_id": task_id,
                "status": task_result.state.lower(),
                "message": f"任务无法取消，当前状态: {task_result.state}"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"取消任务失败: {str(e)}"
        )

@router.get("/")
async def list_active_tasks() -> Dict[str, Any]:
    """
    获取活跃任务列表
    
    Returns:
        活跃任务列表
    """
    try:
        # 获取活跃任务
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        
        if not active_tasks:
            return {
                "active_tasks": [],
                "total_count": 0
            }
        
        # 格式化任务信息
        formatted_tasks = []
        for worker, tasks in active_tasks.items():
            for task in tasks:
                formatted_tasks.append({
                    "task_id": task["id"],
                    "task_name": task["name"],
                    "worker": worker,
                    "args": task.get("args", []),
                    "kwargs": task.get("kwargs", {}),
                    "time_start": task.get("time_start")
                })
        
        return {
            "active_tasks": formatted_tasks,
            "total_count": len(formatted_tasks)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取任务列表失败: {str(e)}"
        )

@router.get("/stats/summary")
async def get_task_stats() -> Dict[str, Any]:
    """
    获取任务统计信息
    
    Returns:
        任务统计数据
    """
    try:
        inspect = celery_app.control.inspect()
        
        # 获取各种任务状态
        active_tasks = inspect.active() or {}
        scheduled_tasks = inspect.scheduled() or {}
        reserved_tasks = inspect.reserved() or {}
        
        # 计算统计数据
        active_count = sum(len(tasks) for tasks in active_tasks.values())
        scheduled_count = sum(len(tasks) for tasks in scheduled_tasks.values())
        reserved_count = sum(len(tasks) for tasks in reserved_tasks.values())
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "active_tasks": active_count,
            "scheduled_tasks": scheduled_count,
            "reserved_tasks": reserved_count,
            "total_pending": active_count + scheduled_count + reserved_count,
            "workers": list(active_tasks.keys()) if active_tasks else []
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取任务统计失败: {str(e)}"
        )