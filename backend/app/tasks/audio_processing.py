"""
音频处理任务
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any
from celery import current_task
from datetime import datetime
import json

from app.core.celery_app import celery_app
from app.core.config import settings
from app.tasks.ai_processing import generate_meeting_summary

@celery_app.task(bind=True, name="process_audio_task")
def process_audio_task(self, file_path: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理音频文件的主任务
    
    Args:
        file_path: 音频文件路径
        file_info: 文件信息
        
    Returns:
        处理结果
    """
    try:
        # 更新任务状态
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 10,
                'current_step': '初始化音频处理',
                'total_steps': 4
            }
        )
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"音频文件不存在: {file_path}")

        # 检查 ffmpeg 是否可用（Whisper 依赖 ffmpeg）
        if shutil.which("ffmpeg") is None:
            raise Exception(
                "未检测到 ffmpeg，可执行文件不在 PATH。请安装 ffmpeg 并添加到系统 PATH 后重试。"
            )
        
        # 加载Whisper模型
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 25,
                'current_step': '加载Whisper模型',
                'total_steps': 4
            }
        )
        
        # 使用用户选择的模型，如果没有指定则使用默认模型
        whisper_model = file_info.get('whisper_model', settings.WHISPER_MODEL)
        model = load_whisper_model(whisper_model)
        
        # 执行语音转录
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 50,
                'current_step': '执行语音转录',
                'total_steps': 4
            }
        )
        
        transcription_result = transcribe_audio(
            model=model,
            file_path=file_path,
            language=file_info.get('language', 'auto')
        )
        
        # 生成AI摘要
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 75,
                'current_step': '生成AI摘要',
                'total_steps': 4
            }
        )
        
        # 调用AI处理逻辑（同步执行，避免在任务内调用 .get() 阻塞）
        summary_result = generate_meeting_summary.run(
            transcription_text=transcription_result['text'],
            meeting_title=file_info.get('meeting_title', '会议录音'),
            language=file_info.get('language', 'auto')
        )
        
        # 完成处理
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 100,
                'current_step': '处理完成',
                'total_steps': 4
            }
        )
        
        # 保存结果到文件
        result_data = {
            "file_info": file_info,
            "transcription": transcription_result,
            "summary": summary_result,
            "processing_time": datetime.utcnow().isoformat(),
            "task_id": self.request.id
        }
        
        # 保存结果文件
        result_file_path = save_processing_result(file_info['file_id'], result_data)
        
        return {
            "success": True,
            "file_id": file_info['file_id'],
            "transcription": transcription_result,
            "summary": summary_result,
            "result_file": result_file_path,
            "processing_completed_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        # 记录错误并返回失败状态
        error_msg = f"音频处理失败: {str(e)}"
        # 不要使用 update_state 设置 FAILURE，直接抛出异常让 Celery 正确记录失败信息
        raise Exception(error_msg)

def load_whisper_model(model_name: str = "base"):
    """
    加载Whisper模型
    
    Args:
        model_name: 模型名称
        
    Returns:
        加载的模型
    """
    try:
        # 导入whisper和torch（延迟导入）
        import whisper
        import torch
        
        # 设置设备
        # 优先使用配置的设备，如果配置为cuda但不可用则回退到cpu
        if settings.WHISPER_DEVICE == "cuda" and torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        
        # 确保模型目录存在
        models_dir = Path(settings.WHISPER_MODELS_DIR)
        models_dir.mkdir(exist_ok=True)
        
        # 加载模型
        model = whisper.load_model(
            model_name,
            device=device,
            download_root=str(models_dir)
        )
        
        return model
        
    except Exception as e:
        raise Exception(f"加载Whisper模型失败: {str(e)}")

def transcribe_audio(model, file_path: str, language: str = "auto") -> Dict[str, Any]:
    """
    转录音频文件
    
    Args:
        model: Whisper模型
        file_path: 音频文件路径
        language: 语言代码
        
    Returns:
        转录结果
    """
    try:
        # 检查模型设备
        device = next(model.parameters()).device
        is_cuda = device.type == "cuda"

        # 设置转录选项
        options = {
            "fp16": is_cuda,  # 在GPU上使用fp16，CPU上使用fp32
            "language": None if language == "auto" else language,
            "task": "transcribe"
        }
        
        # 执行转录
        result = model.transcribe(file_path, **options)
        
        # 格式化结果
        transcription_result = {
            "text": result["text"].strip(),
            "language": result.get("language", "unknown"),
            "segments": [
                {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                }
                for segment in result.get("segments", [])
            ],
            "duration": result.get("segments", [])[-1]["end"] if result.get("segments") else 0
        }
        
        return transcription_result
        
    except Exception as e:
        raise Exception(f"音频转录失败: {str(e)}")

def save_processing_result(file_id: str, result_data: Dict[str, Any]) -> str:
    """
    保存处理结果到文件
    
    Args:
        file_id: 文件ID
        result_data: 结果数据
        
    Returns:
        结果文件路径
    """
    try:
        # 创建结果目录
        results_dir = Path(settings.UPLOAD_DIR) / "results"
        results_dir.mkdir(exist_ok=True)
        
        # 保存结果文件
        result_file_path = results_dir / f"{file_id}_result.json"
        
        with open(result_file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        return str(result_file_path)
        
    except Exception as e:
        raise Exception(f"保存处理结果失败: {str(e)}")

@celery_app.task(name="cleanup_temp_files")
def cleanup_temp_files(file_path: str, keep_result: bool = True) -> Dict[str, Any]:
    """
    清理临时文件
    
    Args:
        file_path: 要清理的文件路径
        keep_result: 是否保留结果文件
        
    Returns:
        清理结果
    """
    try:
        cleaned_files = []
        
        # 删除原始音频文件
        if os.path.exists(file_path):
            os.remove(file_path)
            cleaned_files.append(file_path)
        
        # 如果不保留结果，也删除结果文件
        if not keep_result:
            file_id = Path(file_path).stem.split('_')[0]
            result_file = Path(settings.UPLOAD_DIR) / "results" / f"{file_id}_result.json"
            if result_file.exists():
                result_file.unlink()
                cleaned_files.append(str(result_file))
        
        return {
            "success": True,
            "cleaned_files": cleaned_files,
            "cleanup_time": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "cleanup_time": datetime.utcnow().isoformat()
        }