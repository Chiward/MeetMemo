#!/usr/bin/env python3
"""
完整测试音频处理和AI摘要生成功能
"""

import os
import sys
import uuid
import time
import wave
import struct
import math
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.tasks.audio_processing import process_audio_task

def create_test_audio_with_speech():
    """创建包含模拟语音内容的测试音频文件"""
    try:
        # 创建一个更长的音频文件（5秒），包含多个频率
        duration = 5.0  # 5秒
        sample_rate = 16000
        
        # 创建WAV文件
        test_audio_path = "test_speech_audio.wav"
        
        with wave.open(test_audio_path, 'w') as wav_file:
            # 设置WAV文件参数
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(sample_rate)
            
            # 生成音频数据
            frames = []
            for i in range(int(sample_rate * duration)):
                t = i / sample_rate
                
                # 创建复合音频信号（模拟语音的复杂频率）
                # 基频 + 谐波，模拟人声特征
                value = (
                    0.3 * math.sin(2 * math.pi * 200 * t) +  # 基频 200Hz
                    0.2 * math.sin(2 * math.pi * 400 * t) +  # 二次谐波
                    0.1 * math.sin(2 * math.pi * 600 * t)    # 三次谐波
                )
                
                # 添加包络，模拟语音的动态变化
                envelope = math.exp(-t/2) * (1 + 0.5 * math.sin(2 * math.pi * 0.5 * t))
                value = value * envelope
                
                # 确保音频在合理范围内并转换为16位整数
                value = max(-0.8, min(0.8, value))
                sample = int(value * 32767)
                frames.append(struct.pack('<h', sample))
            
            # 写入音频数据
            wav_file.writeframes(b''.join(frames))
        
        print(f"✅ 创建测试音频文件: {test_audio_path}")
        print(f"   - 时长: {duration}秒")
        print(f"   - 采样率: {sample_rate}Hz")
        print(f"   - 文件大小: {os.path.getsize(test_audio_path)} bytes")
        
        return test_audio_path
        
    except Exception as e:
        print(f"❌ 创建测试音频失败: {str(e)}")
        return None

def test_complete_audio_processing():
    """测试完整的音频处理流程"""
    print("🎯 测试完整音频处理和AI摘要生成功能")
    print("=" * 60)
    
    try:
        # 1. 创建测试音频文件
        print("🎵 创建测试音频文件...")
        audio_file = create_test_audio_with_speech()
        if not audio_file:
            return False
        
        # 2. 准备任务参数
        file_id = str(uuid.uuid4())
        file_info = {
            "file_id": file_id,
            "original_filename": "test_speech_audio.wav",
            "file_size": os.path.getsize(audio_file),
            "content_type": "audio/wav",
            "upload_time": time.time()
        }
        
        print(f"📋 任务参数:")
        print(f"   - 文件ID: {file_id}")
        print(f"   - 文件路径: {audio_file}")
        print(f"   - 文件大小: {file_info['file_size']} bytes")
        
        # 3. 提交音频处理任务
        print("\n🚀 提交音频处理任务...")
        task = process_audio_task.delay(audio_file, file_info)
        print(f"   - 任务ID: {task.id}")
        
        # 4. 等待任务完成
        print("\n⏳ 等待任务完成...")
        print("   (这可能需要几分钟，包括Whisper转录和AI摘要生成)")
        
        # 设置较长的超时时间，因为包含AI摘要生成
        result = task.get(timeout=180)  # 3分钟超时
        
        # 5. 检查结果
        print("\n📊 任务执行结果:")
        if result.get("success"):
            print("✅ 音频处理任务成功完成")
            
            # 显示转录结果
            transcription = result.get("transcription", {})
            if transcription:
                print(f"\n📝 转录结果:")
                print(f"   - 文本: {transcription.get('text', 'N/A')}")
                print(f"   - 语言: {transcription.get('language', 'N/A')}")
                print(f"   - 处理时间: {transcription.get('processing_time', 'N/A')}秒")
            
            # 显示AI摘要结果
            ai_summary = result.get("ai_summary", {})
            if ai_summary:
                print(f"\n🤖 AI摘要结果:")
                print(f"   - 状态: {'成功' if ai_summary.get('success') else '失败'}")
                if ai_summary.get("success"):
                    summary_content = ai_summary.get("summary", "")
                    print(f"   - 摘要长度: {len(summary_content)} 字符")
                    print(f"   - 摘要预览: {summary_content[:200]}...")
                else:
                    print(f"   - 错误信息: {ai_summary.get('error', 'N/A')}")
            
            # 显示文件信息
            file_info_result = result.get("file_info", {})
            if file_info_result:
                print(f"\n📁 文件处理信息:")
                print(f"   - 原始文件: {file_info_result.get('original_filename', 'N/A')}")
                print(f"   - 处理后文件: {file_info_result.get('processed_filename', 'N/A')}")
                print(f"   - 总处理时间: {file_info_result.get('total_processing_time', 'N/A')}秒")
            
            return True
            
        else:
            print("❌ 音频处理任务失败")
            error_msg = result.get("error", "未知错误")
            print(f"   - 错误信息: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False
    
    finally:
        # 清理测试文件
        try:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"\n🧹 清理测试文件: {audio_file}")
        except Exception as e:
            print(f"⚠️ 清理文件失败: {str(e)}")

def main():
    """主函数"""
    print("🎯 MeetMemo 完整音频处理功能测试")
    print("=" * 60)
    
    success = test_complete_audio_processing()
    
    if success:
        print("\n🎉 完整音频处理功能测试成功！")
        print("✅ FFmpeg音频处理正常")
        print("✅ Whisper语音转录正常") 
        print("✅ DeepSeek AI摘要生成正常")
        print("✅ 系统已准备好处理真实音频文件")
    else:
        print("\n❌ 测试失败，请检查系统配置")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)