"""
AI处理任务
"""

import httpx
import json
from typing import Dict, Any
from celery import current_task
from datetime import datetime

from app.core.celery_app import celery_app
from app.core.config import settings

@celery_app.task(bind=True, name="generate_meeting_summary")
def generate_meeting_summary(
    self, 
    transcription_text: str, 
    meeting_title: str = "会议录音",
    language: str = "auto"
) -> Dict[str, Any]:
    """
    使用DeepSeek API生成会议摘要
    
    Args:
        transcription_text: 转录文本
        meeting_title: 会议标题
        language: 语言
        
    Returns:
        生成的摘要结果
    """
    try:
        # 更新任务状态
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 20,
                'current_step': '准备AI摘要请求',
                'total_steps': 3
            }
        )
        
        # 构建提示词
        prompt = build_summary_prompt(transcription_text, meeting_title, language)
        
        # 调用DeepSeek API
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 60,
                'current_step': '调用DeepSeek API',
                'total_steps': 3
            }
        )
        
        summary_response = call_deepseek_api(prompt)
        
        # 处理响应
        current_task.update_state(
            state='PROGRESS',
            meta={
                'progress': 90,
                'current_step': '处理AI响应',
                'total_steps': 3
            }
        )
        
        summary_result = {
            "meeting_title": meeting_title,
            "summary": summary_response["content"],
            "model_used": summary_response.get("model", "deepseek-chat"),
            "tokens_used": summary_response.get("usage", {}),
            "generated_at": datetime.utcnow().isoformat(),
            "language": language,
            "original_text_length": len(transcription_text)
        }
        
        return summary_result
        
    except Exception as e:
        error_msg = f"AI摘要生成失败: {str(e)}"
        # 不要使用 update_state 设置 FAILURE，直接抛出异常让 Celery 正确记录失败信息
        raise Exception(error_msg)

def build_summary_prompt(transcription_text: str, meeting_title: str, language: str) -> str:
    """
    构建AI摘要提示词
    
    Args:
        transcription_text: 转录文本
        meeting_title: 会议标题
        language: 语言
        
    Returns:
        构建的提示词
    """
    
    # 根据语言选择提示词模板
    if language in ["zh", "auto"] or any(ord(char) > 127 for char in transcription_text[:100]):
        # 中文提示词 - 使用详细的会议纪要模板格式
        prompt = f"""请根据以下会议录音转录内容，生成一份专业的会议纪要。请严格按照提供的模板格式进行输出。

会议标题：{meeting_title}

转录内容：
{transcription_text}

请按照以下模板格式生成会议纪要：

# {meeting_title}

## 会议基本信息

- [时间]，[主持人]在[地点]主持召开{meeting_title}会议，会议主要内容为：[会议主要内容]。有[参会单位列表]参加会议。会议纪要如下：

## 会议纪要

### 一、[第一主要点标题]

- 一是[第一个要点的详细内容]
- 二是[第二个要点的详细内容]
- 三是[第三个要点的详细内容]

### 二、[第二主要点标题]

- 一是[第一个要点的详细内容]
- 二是[第二个要点的详细内容]
- 三是[第三个要点的详细内容]

### 三、[第三主要点标题]

- 一是[第一个要点的详细内容]
- 二是[第二个要点的详细内容]
- 三是[第三个要点的详细内容]

### 四、[第四主要点标题]

- 一是[第一个要点的详细内容]
- 二是[第二个要点的详细内容]
- 三是[第三个要点的详细内容]

### 五、[第五主要点标题]

[内容总结段落]

## 参会人员

- [姓名1]
- [姓名2]
- [姓名3]
- （可根据实际参会人员继续添加）

## 分送

- [集团领导]
- [部门1]
- [部门2]
- [公司1]

要求：
1. 严格按照上述模板格式输出，保持结构完整
2. 根据转录内容的实际情况，合理分配主要点（可以是3-5个主要点）
3. 每个主要点下的要点数量可以根据内容调整（1-5个要点）
4. 如果转录内容信息不足，请在相应位置标注"[待确认]"或"[信息不足]"
5. 保持内容的准确性和客观性
6. 使用正式的会议纪要语言风格
"""
    else:
        # 英文提示词 - 使用结构化的会议纪要模板格式
        prompt = f"""Please generate a professional meeting minutes based on the following meeting transcription. Please strictly follow the provided template format.

Meeting Title: {meeting_title}

Transcription Content:
{transcription_text}

Please generate the meeting minutes according to the following template format:

# {meeting_title}

## Meeting Basic Information

- [Time], [Chairperson] chaired the {meeting_title} meeting at [Location]. The main content of the meeting was: [Main meeting content]. [List of participating units] attended the meeting. The meeting minutes are as follows:

## Meeting Minutes

### I. [First Main Point Title]

- First: [Detailed content of the first point]
- Second: [Detailed content of the second point]
- Third: [Detailed content of the third point]

### II. [Second Main Point Title]

- First: [Detailed content of the first point]
- Second: [Detailed content of the second point]
- Third: [Detailed content of the third point]

### III. [Third Main Point Title]

- First: [Detailed content of the first point]
- Second: [Detailed content of the second point]
- Third: [Detailed content of the third point]

### IV. [Fourth Main Point Title]

- First: [Detailed content of the first point]
- Second: [Detailed content of the second point]
- Third: [Detailed content of the third point]

### V. [Fifth Main Point Title]

[Summary paragraph content]

## Participants

- [Name 1]
- [Name 2]
- [Name 3]
- (Add more participants as needed)

## Distribution

- [Group Leadership]
- [Department 1]
- [Department 2]
- [Company 1]

Requirements:
1. Strictly follow the above template format and maintain complete structure
2. Reasonably allocate main points based on actual transcription content (3-5 main points)
3. Adjust the number of sub-points under each main point according to content (1-5 points)
4. If transcription information is insufficient, mark as "[To be confirmed]" or "[Insufficient information]"
5. Maintain accuracy and objectivity of content
6. Use formal meeting minutes language style
"""
    
    return prompt

def call_deepseek_api(prompt: str) -> Dict[str, Any]:
    """
    调用DeepSeek API
    
    Args:
        prompt: 提示词
        
    Returns:
        API响应结果
    """
    try:
        # 检查API密钥
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("DeepSeek API密钥未配置")
        
        # 构建请求数据
        request_data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.3,
            "top_p": 0.9,
            "stream": False
        }
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"
        }
        
        # 发送请求
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                settings.DEEPSEEK_API_URL,
                json=request_data,
                headers=headers
            )
            
            response.raise_for_status()
            
            # 解析响应
            response_data = response.json()
            
            if "choices" not in response_data or not response_data["choices"]:
                raise ValueError("API响应格式错误：缺少choices字段")
            
            choice = response_data["choices"][0]
            if "message" not in choice:
                raise ValueError("API响应格式错误：缺少message字段")
            
            return {
                "content": choice["message"]["content"],
                "model": response_data.get("model", "deepseek-chat"),
                "usage": response_data.get("usage", {}),
                "finish_reason": choice.get("finish_reason", "unknown")
            }
            
    except httpx.HTTPStatusError as e:
        error_detail = f"HTTP错误 {e.response.status_code}"
        try:
            error_response = e.response.json()
            if "error" in error_response:
                error_detail += f": {error_response['error'].get('message', '未知错误')}"
        except:
            pass
        raise Exception(f"DeepSeek API调用失败: {error_detail}")
        
    except httpx.TimeoutException:
        raise Exception("DeepSeek API调用超时")
        
    except Exception as e:
        raise Exception(f"DeepSeek API调用失败: {str(e)}")

@celery_app.task(name="test_deepseek_connection")
def test_deepseek_connection() -> Dict[str, Any]:
    """
    测试DeepSeek API连接
    
    Returns:
        连接测试结果
    """
    try:
        test_prompt = "请回复'连接测试成功'"
        result = call_deepseek_api(test_prompt)
        
        return {
            "success": True,
            "message": "DeepSeek API连接正常",
            "response": result["content"],
            "model": result.get("model", "unknown"),
            "test_time": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"DeepSeek API连接失败: {str(e)}",
            "test_time": datetime.utcnow().isoformat()
        }