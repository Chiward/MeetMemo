import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, App as AntdApp } from 'antd';

// 组件导入
import { AppHeader, AppFooter } from './components';
import { HomePage, ProcessingPage, ResultPage } from './pages';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <AntdApp>
      <Router>
        <Layout className="app-layout" style={{ minHeight: '100vh' }}>
          <AppHeader />
          
          <Content className="app-content" style={{ padding: '24px', flex: 1 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/processing/:taskId" element={<ProcessingPage />} />
              <Route path="/result/:taskId" element={<ResultPage />} />
            </Routes>
          </Content>
          
          <AppFooter />
        </Layout>
      </Router>
    </AntdApp>
  );
};

export default App;