#!/usr/bin/env python3
"""
会议纪要生成脚本
使用DeepSeek API根据模板生成完整的会议纪要文档
"""

import os
import sys
import asyncio
import httpx
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

async def call_deepseek_api(prompt: str) -> dict:
    """
    调用DeepSeek API生成内容
    
    Args:
        prompt: 提示词
        
    Returns:
        API响应结果
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                settings.DEEPSEEK_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "system", 
                            "content": "你是一个专业的会议纪要生成助手，能够根据提供的模板格式生成完整、规范的会议纪要文档。请严格按照模板的结构和格式要求生成内容。"
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": 4000,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {"success": True, "content": content}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
                
    except Exception as e:
        return {"success": False, "error": str(e)}

def load_template() -> str:
    """加载会议纪要模板"""
    template_path = os.path.join(os.path.dirname(__file__), "会议纪要模板.md")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 无法加载模板文件: {str(e)}")
        return ""

async def generate_meeting_minutes(meeting_topic: str = None, meeting_type: str = None) -> str:
    """
    生成完整的会议纪要文档
    
    Args:
        meeting_topic: 会议主题
        meeting_type: 会议类型
        
    Returns:
        生成的会议纪要内容
    """
    # 加载模板
    template = load_template()
    if not template:
        return ""
    
    # 构建提示词
    if not meeting_topic:
        meeting_topic = "项目协调推进会议"
    if not meeting_type:
        meeting_type = "工程项目管理会议"
    
    prompt = f"""
请根据以下会议纪要模板，生成一份完整的{meeting_type}纪要文档。

会议主题：{meeting_topic}
会议类型：{meeting_type}

模板格式：
{template}

要求：
1. 严格按照模板的结构和格式生成内容
2. 将模板中的占位符（如[会议标题]、[时间]、[主持人]等）替换为具体的内容
3. 生成5个主要议题，每个议题包含3个具体要点
4. 内容要具体、专业，符合实际工程项目管理场景
5. 参会人员列表包含5-8人，职务和姓名要合理
6. 分送单位要包含相关的集团部门和公司
7. 保持原有的Markdown格式和层级结构
8. 内容要逻辑清晰，语言规范，符合正式会议纪要的要求

请生成完整的会议纪要文档：
"""
    
    print("🎯 正在生成会议纪要...")
    print(f"📋 会议主题: {meeting_topic}")
    print(f"📝 会议类型: {meeting_type}")
    print("⏳ 调用DeepSeek API生成内容...")
    
    # 调用API生成内容
    result = await call_deepseek_api(prompt)
    
    if result.get("success"):
        return result.get("content", "")
    else:
        print(f"❌ 生成失败: {result.get('error', '未知错误')}")
        return ""

async def save_generated_minutes(content: str, filename: str = None) -> str:
    """
    保存生成的会议纪要到文件
    
    Args:
        content: 会议纪要内容
        filename: 文件名（可选）
        
    Returns:
        保存的文件路径
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"会议纪要_{timestamp}.md"
    
    # 保存到backend目录
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 会议纪要已保存到: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ 保存失败: {str(e)}")
        return ""

async def main():
    """主函数"""
    print("🎯 会议纪要生成工具")
    print("=" * 50)
    
    # 检查API配置
    if not settings.DEEPSEEK_API_KEY:
        print("❌ DeepSeek API Key未配置，请检查.env文件")
        return False
    
    print(f"✅ API配置正常")
    
    # 检查命令行参数
    meeting_topic = "项目协调推进会议"
    meeting_type = "工程项目管理会议"
    
    if len(sys.argv) > 1:
        meeting_topic = sys.argv[1]
    if len(sys.argv) > 2:
        meeting_type = sys.argv[2]
    
    # 如果没有命令行参数且是交互式环境，则询问用户输入
    if len(sys.argv) == 1 and sys.stdin.isatty():
        print("\n📝 请输入会议信息（直接回车使用默认值）:")
        
        try:
            user_topic = input("会议主题 [项目协调推进会议]: ").strip()
            if user_topic:
                meeting_topic = user_topic
            
            user_type = input("会议类型 [工程项目管理会议]: ").strip()
            if user_type:
                meeting_type = user_type
        except (EOFError, KeyboardInterrupt):
            print("\n使用默认值继续...")
    
    print(f"\n📋 使用会议主题: {meeting_topic}")
    print(f"📝 使用会议类型: {meeting_type}")
    
    # 生成会议纪要
    content = await generate_meeting_minutes(meeting_topic, meeting_type)
    
    if content:
        print("\n✅ 会议纪要生成成功！")
        print("=" * 50)
        print(content)
        print("=" * 50)
        
        # 询问是否保存（仅在交互式环境下）
        should_save = True
        if sys.stdin.isatty():
            try:
                save_choice = input("\n💾 是否保存到文件？(y/n) [y]: ").strip().lower()
                should_save = save_choice != 'n'
            except (EOFError, KeyboardInterrupt):
                should_save = True
        
        if should_save:
            file_path = await save_generated_minutes(content)
            if file_path:
                print(f"📁 文件已保存: {file_path}")
        
        return True
    else:
        print("❌ 会议纪要生成失败")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 程序异常: {str(e)}")
        sys.exit(1)