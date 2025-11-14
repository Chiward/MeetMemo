#!/usr/bin/env python3
"""
直接测试DeepSeek API功能（不依赖Celery）
"""

import os
import sys
import httpx
import json

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

async def test_deepseek_connection():
    """直接测试DeepSeek API连接"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.DEEPSEEK_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"
                },
                json={
                    "model": "deepseek-reasoner",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hello! Please respond with 'API connection successful'."}
                    ],
                    "max_tokens": 50,
                    "temperature": 0.1
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {"success": True, "response": content}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
                
    except Exception as e:
        return {"success": False, "error": str(e)}

async def test_meeting_summary():
    """直接测试会议摘要生成"""
    transcription_text = """
    大家好，今天我们开会讨论项目进展。
    首先，张三汇报了前端开发的进度，目前已经完成了用户界面的设计。
    然后，李四介绍了后端API的开发情况，数据库设计已经完成。
    最后，我们决定下周进行第一次系统测试。
    会议结束，谢谢大家。
    """
    
    meeting_title = "项目进展讨论会议"
    
    # 构建提示词
    prompt = f"""请根据以下会议转录内容，生成一份结构化的会议纪要：

会议主题：{meeting_title}

转录内容：
{transcription_text}

请按照以下格式生成会议纪要：

# 会议纪要

**会议主题**: {meeting_title}
**会议时间**: [请根据转录内容推断或标注为"未指定"]

## 主要议题
[请详细分点总结转录内容中的主要议题和各方观点]

## 决议事项
[请提炼转录内容中形成的所有明确决议]

## 行动计划
[请列出需要跟进的具体行动项目]
- [负责人] - [任务描述] - [截止日期]

## 备注
[补充重要信息和备注]

---
*本纪要由AI自动生成，请核对后使用*"""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                settings.DEEPSEEK_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"
                },
                json={
                    "model": "deepseek-reasoner",
                    "messages": [
                        {"role": "system", "content": "你是一个专业的会议纪要生成助手，能够根据会议转录内容生成结构化的会议纪要。"},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {"success": True, "summary": content}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
                
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    """主测试函数"""
    print("🎯 直接测试DeepSeek API功能")
    print("=" * 50)
    
    try:
        # 1. 检查API配置
        print("🔧 检查API配置...")
        if not settings.DEEPSEEK_API_KEY:
            print("❌ DeepSeek API Key未配置")
            return False
        
        print(f"✅ API URL: {settings.DEEPSEEK_API_URL}")
        print(f"✅ API Key: {settings.DEEPSEEK_API_KEY[:10]}...")
        
        # 2. 测试API连接
        print("\n🔗 测试API连接...")
        connection_result = await test_deepseek_connection()
        if connection_result.get('success'):
            print("✅ DeepSeek API连接成功")
            print(f"📝 响应: {connection_result.get('response', '')}")
        else:
            print(f"❌ API连接失败: {connection_result.get('error', '')}")
            return False
        
        # 3. 测试摘要生成
        print("\n📝 测试摘要生成...")
        summary_result = await test_meeting_summary()
        if summary_result.get('success'):
            print("✅ 摘要生成成功")
            print(f"📄 摘要内容:\n{summary_result.get('summary', '')}")
        else:
            print(f"❌ 摘要生成失败: {summary_result.get('error', '')}")
            return False
        
        print("\n🎉 DeepSeek API功能测试完成！")
        print("✅ API连接正常")
        print("✅ 摘要生成正常")
        print("✅ 系统已准备好处理AI摘要任务")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(main())
    sys.exit(0 if success else 1)