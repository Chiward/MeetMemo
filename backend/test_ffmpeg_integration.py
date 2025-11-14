#!/usr/bin/env python3
"""
测试ffmpeg集成和音频处理功能
"""

import os
import sys
import subprocess
import tempfile
import numpy as np
import wave
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_ffmpeg_availability():
    """测试ffmpeg是否可用"""
    print("🔍 测试ffmpeg可用性...")
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ ffmpeg可用: {version_line}")
            return True
        else:
            print(f"❌ ffmpeg执行失败: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ ffmpeg未找到，请检查PATH设置")
        return False
    except subprocess.TimeoutExpired:
        print("❌ ffmpeg执行超时")
        return False
    except Exception as e:
        print(f"❌ ffmpeg测试异常: {str(e)}")
        return False

def create_test_audio():
    """创建测试音频文件"""
    print("\n🎵 创建测试音频文件...")
    
    # 生成1秒的440Hz正弦波（A音）
    sample_rate = 44100
    duration = 1.0
    frequency = 440.0
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # 转换为16位整数
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # 创建临时WAV文件
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    
    with wave.open(temp_file.name, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"✅ 测试音频文件创建: {temp_file.name}")
    return temp_file.name

def test_ffmpeg_conversion(input_file):
    """测试ffmpeg音频转换"""
    print(f"\n🔄 测试ffmpeg音频转换...")
    
    output_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    output_file.close()
    
    try:
        # 使用ffmpeg转换音频格式
        cmd = [
            "ffmpeg", 
            "-i", input_file,
            "-ar", "16000",  # 采样率16kHz
            "-ac", "1",      # 单声道
            "-y",            # 覆盖输出文件
            output_file.name
        ]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if result.returncode == 0:
            # 检查输出文件是否存在且有内容
            if os.path.exists(output_file.name) and os.path.getsize(output_file.name) > 0:
                print(f"✅ ffmpeg转换成功: {output_file.name}")
                print(f"   输入文件大小: {os.path.getsize(input_file)} bytes")
                print(f"   输出文件大小: {os.path.getsize(output_file.name)} bytes")
                return output_file.name
            else:
                print("❌ 转换后文件为空或不存在")
                return None
        else:
            print(f"❌ ffmpeg转换失败:")
            print(f"   错误信息: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ ffmpeg转换超时")
        return None
    except Exception as e:
        print(f"❌ ffmpeg转换异常: {str(e)}")
        return None

def test_audio_processing_task():
    """测试音频处理任务"""
    print(f"\n🧪 测试音频处理任务...")
    
    try:
        from app.tasks.audio_processing import process_audio_task
        from celery import current_app
        import uuid
        
        # 创建测试音频
        test_audio_file = create_test_audio()
        
        if not test_audio_file:
            print("❌ 无法创建测试音频文件")
            return False
        
        print(f"📤 提交音频处理任务...")
        
        # 创建测试文件信息
        file_info = {
            'file_id': str(uuid.uuid4()),
            'filename': 'test_audio.wav',
            'meeting_title': '测试会议',
            'language': 'auto',
            'whisper_model': 'base'
        }
        
        # 提交任务到Celery
        task_result = process_audio_task.delay(test_audio_file, file_info)
        
        print(f"   任务ID: {task_result.id}")
        print(f"   任务状态: {task_result.status}")
        
        # 等待任务完成（最多60秒，因为需要加载模型）
        try:
            result = task_result.get(timeout=60)
            print(f"✅ 音频处理任务完成!")
            print(f"   结果: {result}")
            return True
            
        except Exception as e:
            print(f"❌ 音频处理任务失败: {str(e)}")
            return False
        
        finally:
            # 清理测试文件
            try:
                os.unlink(test_audio_file)
                print(f"🗑️ 清理测试文件: {test_audio_file}")
            except:
                pass
                
    except ImportError as e:
        print(f"❌ 无法导入音频处理模块: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 音频处理任务测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始ffmpeg集成测试...\n")
    
    # 测试1: ffmpeg可用性
    if not test_ffmpeg_availability():
        print("\n❌ ffmpeg不可用，测试终止")
        return False
    
    # 测试2: 创建和转换音频
    test_audio_file = create_test_audio()
    if not test_audio_file:
        print("\n❌ 无法创建测试音频，测试终止")
        return False
    
    converted_file = test_ffmpeg_conversion(test_audio_file)
    
    # 清理测试文件
    try:
        os.unlink(test_audio_file)
        if converted_file:
            os.unlink(converted_file)
    except:
        pass
    
    if not converted_file:
        print("\n❌ ffmpeg转换失败，测试终止")
        return False
    
    # 测试3: 音频处理任务
    if not test_audio_processing_task():
        print("\n❌ 音频处理任务测试失败")
        return False
    
    print(f"\n🎉 所有测试通过！ffmpeg集成正常工作")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)