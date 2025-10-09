"""
应用配置管理
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """应用设置类"""
    
    # 基础配置
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "your_secret_key_here_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./meetmemo.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # DeepSeek API配置
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/chat/completions"
    DEEPSEEK_API_KEY: str = ""
    
    # Whisper配置
    WHISPER_MODEL: str = "base"
    WHISPER_DEVICE: str = "cpu"  # 'cuda' if GPU available
    WHISPER_MODELS_DIR: str = "./models"
    
    # 文件上传配置
    MAX_FILE_SIZE: int = 524288000  # 500MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "m4a", "flac", "ogg"]
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
    # 任务配置
    TASK_TIMEOUT: int = 3600  # 1小时
    MAX_CONCURRENT_TASKS: int = 3
    
    # 安全配置
    ENCRYPTION_KEY: str = ""  # 用于加密API Key
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 确保目录存在
        Path(self.UPLOAD_DIR).mkdir(exist_ok=True)
        Path(self.WHISPER_MODELS_DIR).mkdir(exist_ok=True)
        
        # 如果没有设置加密密钥，使用SECRET_KEY
        if not self.ENCRYPTION_KEY:
            self.ENCRYPTION_KEY = self.SECRET_KEY

# 创建全局设置实例
settings = Settings()

# 数据库配置
def get_database_url() -> str:
    """获取数据库连接URL"""
    return settings.DATABASE_URL

# Whisper模型配置
WHISPER_MODEL_SIZES = {
    "tiny": {"params": "39M", "vram": "~1GB", "speed": "~10x"},
    "base": {"params": "74M", "vram": "~1GB", "speed": "~7x"},
    "small": {"params": "244M", "vram": "~2GB", "speed": "~4x"},
    "medium": {"params": "769M", "vram": "~5GB", "speed": "~2x"},
    "large": {"params": "1550M", "vram": "~10GB", "speed": "1x"},
    "turbo": {"params": "809M", "vram": "~6GB", "speed": "~8x"}
}

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    "auto": "自动检测",
    "zh": "中文",
    "en": "英文",
    "ja": "日文",
    "ko": "韩文",
    "es": "西班牙文",
    "fr": "法文",
    "de": "德文",
    "ru": "俄文"
}

# 会议纪要模板
DEFAULT_MEETING_TEMPLATE = """# 会议纪要

**会议时间**: {meeting_time}
**会议主题**: [请根据转录内容总结会议的核心主题]
**参会人员**: [请根据转录内容列出参会人员]

## 主要议题
[请详细分点总结转录内容中的主要议题和各方观点]

## 重要决议
[请提炼转录内容中形成的所有明确决议]

## 行动项 (Action Items)
- [负责人] - [任务描述] - [截止日期]

## 其他要点
[补充重要信息和备注]

---
*本纪要由AI自动生成，请核对后使用*
"""