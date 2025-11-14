#!/usr/bin/env python3
"""
测试Whisper模型加载和基本功能
"""

import whisper
import torch
from pathlib import Path
import time

def test_models():
    """测试模型加载和基本功能"""
    
    models_dir = Path("models")
    
    print("🧪 开始测试Whisper模型...")
    print(f"📁 模型目录: {models_dir.absolute()}")
    
    # 检查模型文件
    model_files = list(models_dir.glob("*.pt"))
    print(f"\n📋 发现 {len(model_files)} 个模型文件:")
    for file in model_files:
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"   - {file.name} ({size_mb:.1f} MB)")
    
    # 测试模型加载
    models_to_test = ["base", "turbo"]
    
    for model_name in models_to_test:
        print(f"\n🔍 测试 {model_name} 模型...")
        
        try:
            start_time = time.time()
            
            # 加载模型
            model = whisper.load_model(model_name)
            
            load_time = time.time() - start_time
            print(f"✅ {model_name} 模型加载成功！(耗时: {load_time:.2f}秒)")
            
            # 显示模型信息
            if hasattr(model, 'dims'):
                dims = model.dims
                print(f"   📊 模型参数:")
                print(f"      - 音频状态维度: {dims.n_audio_state}")
                print(f"      - 文本状态维度: {dims.n_text_state}")
                print(f"      - 词汇表大小: {dims.n_vocab}")
                print(f"      - 音频层数: {dims.n_audio_layer}")
                print(f"      - 文本层数: {dims.n_text_layer}")
            
            # 检查设备
            device = next(model.parameters()).device
            print(f"   🖥️ 运行设备: {device}")
            
            # 测试基本功能（使用虚拟音频数据）
            print(f"   🎵 测试基本转录功能...")
            
            # 创建虚拟音频数据（1秒的静音）
            sample_rate = 16000
            audio_data = torch.zeros(sample_rate, dtype=torch.float32)
            
            # 进行转录测试
            start_time = time.time()
            result = model.transcribe(audio_data.numpy(), language="zh")
            transcribe_time = time.time() - start_time
            
            print(f"   ✅ 转录测试完成！(耗时: {transcribe_time:.2f}秒)")
            print(f"   📝 转录结果: '{result['text'].strip()}'")
            
        except Exception as e:
            print(f"   ❌ {model_name} 模型测试失败: {str(e)}")
            continue
    
    print(f"\n🎉 模型测试完成！")
    
    # 显示使用建议
    print(f"\n💡 使用建议:")
    print(f"   - base模型: 适合快速转录，准确性较好")
    print(f"   - turbo模型: 最新优化版本，速度更快，准确性更高")
    print(f"   - 模型已保存在: {models_dir.absolute()}")

if __name__ == "__main__":
    test_models()