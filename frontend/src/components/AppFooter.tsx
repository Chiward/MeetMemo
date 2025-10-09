import React from 'react';
import { Layout, Typography, Space, Divider } from 'antd';
import { GithubOutlined, HeartFilled } from '@ant-design/icons';

const { Footer } = Layout;
const { Text, Link } = Typography;

const AppFooter: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Footer 
      style={{ 
        textAlign: 'center',
        background: '#fafafa',
        borderTop: '1px solid #f0f0f0',
        padding: '24px 50px'
      }}
    >
      <Space direction="vertical" size="small">
        <Space split={<Divider type="vertical" />} size="large">
          <Text type="secondary">
            基于 Whisper + DeepSeek API 构建
          </Text>
          <Text type="secondary">
            支持多种音频格式转录
          </Text>
          <Text type="secondary">
            智能生成结构化会议纪要
          </Text>
        </Space>
        
        <Space size="middle">
          <Link 
            href="https://github.com/openai/whisper" 
            target="_blank"
            style={{ color: '#8c8c8c' }}
          >
            <GithubOutlined /> Whisper
          </Link>
          <Link 
            href="https://www.deepseek.com/" 
            target="_blank"
            style={{ color: '#8c8c8c' }}
          >
            DeepSeek API
          </Link>
        </Space>
        
        <Text type="secondary" style={{ fontSize: '12px' }}>
          © {currentYear} MeetMemo. Made with <HeartFilled style={{ color: '#ff4d4f' }} /> for better meetings.
        </Text>
      </Space>
    </Footer>
  );
};

export default AppFooter;