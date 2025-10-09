import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Typography, 
  Space, 
  Alert, 
  Row, 
  Col,
  Statistic,
  Tag
} from 'antd';
import { 
  CloudUploadOutlined, 
  SoundOutlined, 
  FileTextOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';

import UploadComponent from '../components/UploadComponent';
import { ApiService } from '../services/api';
import { UploadResponse, SupportedFormatsResponse } from '../types';
import { formatFileSize } from '../utils';

const { Title, Paragraph, Text } = Typography;

const HomePage: React.FC = () => {
  const [supportedFormats, setSupportedFormats] = useState<SupportedFormatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSupportedFormats();
  }, []);

  const loadSupportedFormats = async () => {
    try {
      setLoading(true);
      const formats = await ApiService.getSupportedFormats();
      setSupportedFormats(formats);
      setError(null);
    } catch (err) {
      setError('获取支持格式失败，请检查后端服务是否正常运行');
      console.error('获取支持格式失败:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (response: UploadResponse) => {
    // 跳转到处理页面
    window.location.href = `/processing/${response.task_id}`;
  };

  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage);
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      {/* 欢迎区域 */}
      <Card 
        className="content-card" 
        style={{ 
          marginBottom: '24px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          border: 'none'
        }}
      >
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div style={{ textAlign: 'center' }}>
            <Title level={2} style={{ marginBottom: '16px', color: 'white' }}>
              <SoundOutlined style={{ color: '#fff', marginRight: '12px', fontSize: '32px' }} />
              欢迎使用 MeetMemo
            </Title>
            <Paragraph style={{ fontSize: '18px', color: 'rgba(255,255,255,0.9)', marginBottom: '24px' }}>
              🚀 AI智能会议纪要生成助手，快速将您的会议录音转换为结构化的专业纪要
            </Paragraph>
          </div>

          {/* 功能特点 */}
          <Row gutter={[24, 16]}>
            <Col xs={24} sm={8}>
              <Card 
                size="small" 
                style={{ 
                  textAlign: 'center', 
                  height: '140px',
                  background: 'rgba(255,255,255,0.15)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  backdropFilter: 'blur(10px)',
                  transition: 'all 0.3s ease'
                }}
                hoverable
              >
                <CloudUploadOutlined style={{ fontSize: '32px', color: '#fff', marginBottom: '8px' }} />
                <div>
                  <Text strong style={{ color: 'white', fontSize: '16px' }}>📤 简单上传</Text>
                  <br />
                  <Text style={{ fontSize: '13px', color: 'rgba(255,255,255,0.8)' }}>
                    支持多种音频格式
                  </Text>
                </div>
              </Card>
            </Col>
            <Col xs={24} sm={8}>
              <Card 
                size="small" 
                style={{ 
                  textAlign: 'center', 
                  height: '140px',
                  background: 'rgba(255,255,255,0.15)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  backdropFilter: 'blur(10px)',
                  transition: 'all 0.3s ease'
                }}
                hoverable
              >
                <SoundOutlined style={{ fontSize: '32px', color: '#fff', marginBottom: '8px' }} />
                <div>
                  <Text strong style={{ color: 'white', fontSize: '16px' }}>🎯 智能转录</Text>
                  <br />
                  <Text style={{ fontSize: '13px', color: 'rgba(255,255,255,0.8)' }}>
                    基于Whisper技术
                  </Text>
                </div>
              </Card>
            </Col>
            <Col xs={24} sm={8}>
              <Card 
                size="small" 
                style={{ 
                  textAlign: 'center', 
                  height: '140px',
                  background: 'rgba(255,255,255,0.15)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  backdropFilter: 'blur(10px)',
                  transition: 'all 0.3s ease'
                }}
                hoverable
              >
                <FileTextOutlined style={{ fontSize: '32px', color: '#fff', marginBottom: '8px' }} />
                <div>
                  <Text strong style={{ color: 'white', fontSize: '16px' }}>✨ AI摘要</Text>
                  <br />
                  <Text style={{ fontSize: '13px', color: 'rgba(255,255,255,0.8)' }}>
                    结构化会议纪要
                  </Text>
                </div>
              </Card>
            </Col>
          </Row>
        </Space>
      </Card>

      {/* 错误提示 */}
      {error && (
        <Alert
          message="错误"
          description={error}
          type="error"
          showIcon
          closable
          onClose={() => setError(null)}
          style={{ marginBottom: '24px' }}
        />
      )}

      {/* 上传区域 */}
      <Card className="content-card" title="上传会议录音">
        <UploadComponent
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
        />
      </Card>

      {/* 支持格式信息 */}
      {supportedFormats && (
        <Card className="content-card" title="支持的格式">
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12}>
              <Statistic
                title="最大文件大小"
                value={supportedFormats.max_file_size_mb}
                suffix="MB"
                prefix={<CloudUploadOutlined />}
              />
            </Col>
            <Col xs={24} sm={12}>
              <Statistic
                title="支持格式"
                value={supportedFormats.supported_formats.length}
                suffix="种"
                prefix={<CheckCircleOutlined />}
              />
            </Col>
          </Row>
          
          <div style={{ marginTop: '16px' }}>
            <Text strong>支持的音频格式：</Text>
            <div style={{ marginTop: '8px' }}>
              {supportedFormats.supported_formats.map((format: string) => (
                <Tag key={format} color="blue" style={{ margin: '2px' }}>
                  .{format}
                </Tag>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* 使用说明 */}
      <Card className="content-card" title="使用说明">
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <div>
            <Text strong>1. 上传音频文件</Text>
            <Paragraph style={{ marginLeft: '16px', marginBottom: '8px' }}>
              点击上传区域或拖拽音频文件到指定区域，支持 MP3、WAV、M4A 等常见格式
            </Paragraph>
          </div>
          
          <div>
            <Text strong>2. 设置会议信息</Text>
            <Paragraph style={{ marginLeft: '16px', marginBottom: '8px' }}>
              可选择设置会议标题和转录语言，系统支持自动语言检测
            </Paragraph>
          </div>
          
          <div>
            <Text strong>3. 等待处理完成</Text>
            <Paragraph style={{ marginLeft: '16px', marginBottom: '8px' }}>
              系统将自动进行语音转录和AI摘要生成，处理时间取决于音频长度
            </Paragraph>
          </div>
          
          <div>
            <Text strong>4. 查看和导出结果</Text>
            <Paragraph style={{ marginLeft: '16px', marginBottom: '8px' }}>
              处理完成后可查看转录文本和会议纪要，支持多种格式导出
            </Paragraph>
          </div>
        </Space>
      </Card>
    </div>
  );
};

export default HomePage;