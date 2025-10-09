import React from 'react';
import { Layout, Typography, Space, Button } from 'antd';
import { SoundOutlined, HomeOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header } = Layout;
const { Title } = Typography;

const AppHeader: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleGoHome = () => {
    navigate('/');
  };

  const handleShowInfo = () => {
    // 可以显示应用信息模态框
    console.log('显示应用信息');
  };

  return (
    <Header 
      style={{ 
        background: '#fff', 
        padding: '0 24px',
        borderBottom: '1px solid #f0f0f0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}
    >
      <Space align="center" size="large">
        <div 
          style={{ 
            display: 'flex', 
            alignItems: 'center', 
            cursor: 'pointer' 
          }}
          onClick={handleGoHome}
        >
          <SoundOutlined 
            style={{ 
              fontSize: '24px', 
              color: '#1890ff', 
              marginRight: '12px' 
            }} 
          />
          <Title 
            level={3} 
            style={{ 
              margin: 0, 
              color: '#262626',
              fontWeight: 600
            }}
          >
            MeetMemo
          </Title>
        </div>
        <Typography.Text type="secondary" style={{ fontSize: '14px' }}>
          AI智能会议纪要生成助手
        </Typography.Text>
      </Space>

      <Space>
        {location.pathname !== '/' && (
          <Button 
            type="text" 
            icon={<HomeOutlined />}
            onClick={handleGoHome}
          >
            首页
          </Button>
        )}
        <Button 
          type="text" 
          icon={<InfoCircleOutlined />}
          onClick={handleShowInfo}
        >
          关于
        </Button>
      </Space>
    </Header>
  );
};

export default AppHeader;