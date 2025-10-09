#!/usr/bin/env python3
"""
测试DeepSeek API功能
"""

import os
import sys
import asyncio

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tasks.ai_processing import test_deepseek_connection, generate_meeting_summary
from app.core.config import settings

def test_deepseek_api():
    """测试DeepSeek API功能"""
    print("🎯 测试DeepSeek API功能")
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
        try:
            # 使用Celery任务测试连接
            result = test_deepseek_connection.delay().get(timeout=30)
            if result.get('success'):
                print("✅ DeepSeek API连接成功")
                print(f"📝 响应: {result.get('response', '')}")
            else:
                print(f"❌ API连接失败: {result.get('error', '')}")
                return False
        except Exception as e:
            print(f"❌ API连接测试失败: {str(e)}")
            return False
        
        # 3. 测试摘要生成
        print("\n📝 测试摘要生成...")
        test_transcription = """
        大家好，今天我们开会讨论项目进展。
        首先，张三汇报了前端开发的进度，目前已经完成了用户界面的设计。
        然后，李四介绍了后端API的开发情况，数据库设计已经完成。
        最后，我们决定下周进行第一次系统测试。
        会议结束，谢谢大家。
        """
        
        try:
            summary_result = generate_meeting_summary.delay(
                transcription_text=test_transcription,
                meeting_title="项目进展讨论会议",
                language="zh"
            ).get(timeout=60)
            
            if summary_result.get('success'):
                print("✅ 摘要生成成功")
                print(f"📄 摘要内容:\n{summary_result.get('summary', '')}")
            else:
                print(f"❌ 摘要生成失败: {summary_result.get('error', '')}")
                return False
                
        except Exception as e:
            print(f"❌ 摘要生成测试失败: {str(e)}")
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
    success = test_deepseek_api()
    sys.exit(0 if success else 1)