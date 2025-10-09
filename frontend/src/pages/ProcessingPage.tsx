import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Progress,
  Typography,
  Space,
  Button,
  Alert,
  Spin,
  Steps,
  Tag,
  Descriptions,
  Row,
  Col
} from 'antd';
import {
  LoadingOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  SoundOutlined,
  FileTextOutlined,
  BulbOutlined,
  HomeOutlined,
  ReloadOutlined
} from '@ant-design/icons';

import { ApiService } from '../services/api';
import { TaskStatusResponse, TaskStatus } from '../types';
import { formatTime, getErrorMessage, TASK_STATUS_MAP } from '../utils';

const { Title, Text, Paragraph } = Typography;
const { Step } = Steps;

const ProcessingPage: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  
  const [taskStatus, setTaskStatus] = useState<TaskStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [polling, setPolling] = useState(true);

  const fetchTaskStatus = useCallback(async () => {
    if (!taskId) return;

    try {
      const status = await ApiService.getTaskStatus(taskId);
      setTaskStatus(status);
      setError(null);

      // 如果任务完成或失败，停止轮询
      if (status.status === 'completed' || status.status === 'failed') {
        setPolling(false);
        
        // 如果成功，跳转到结果页面
        if (status.status === 'completed') {
          setTimeout(() => {
            navigate(`/result/${taskId}`);
          }, 2000);
        }
      }
    } catch (err) {
      console.error('获取任务状态失败:', err);
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [taskId, navigate]);

  useEffect(() => {
    if (!taskId) {
      setError('无效的任务ID');
      setLoading(false);
      return;
    }

    fetchTaskStatus();
  }, [fetchTaskStatus, taskId]);

  useEffect(() => {
    if (!polling || !taskId) return;

    const interval = setInterval(fetchTaskStatus, 3000);
    return () => clearInterval(interval);
  }, [polling, fetchTaskStatus, taskId]);

  const handleCancelTask = async () => {
    if (!taskId) return;

    try {
      await ApiService.cancelTask(taskId);
      setPolling(false);
      setTaskStatus(prev => prev ? { ...prev, status: 'REVOKED' as TaskStatus } : null);
    } catch (err) {
      console.error('取消任务失败:', err);
      setError(getErrorMessage(err));
    }
  };

  const handleRetry = () => {
    setLoading(true);
    setError(null);
    setPolling(true);
    fetchTaskStatus();
  };

  const getStepStatus = (stepIndex: number) => {
    if (!taskStatus) return 'wait';
    
    const { status, progress } = taskStatus;
    
    if (status === 'failed') {
      return stepIndex === getCurrentStep() ? 'error' : stepIndex < getCurrentStep() ? 'finish' : 'wait';
    }
    
    if (status === 'completed') {
      return 'finish';
    }
    
    if (stepIndex < getCurrentStep()) return 'finish';
    if (stepIndex === getCurrentStep()) return 'process';
    return 'wait';
  };

  const getCurrentStep = () => {
    if (!taskStatus) return 0;
    
    const { status } = taskStatus;
    
    if (status === 'pending') return 0;
    if (status === 'processing') {
      // 优先使用后端提供的 current_step
      const step = (taskStatus.current_step || '').toString();
      if (step.includes('转录') || step.toLowerCase().includes('transcribe')) return 1;
      if (step.includes('摘要') || step.toLowerCase().includes('summary') || step.toLowerCase().includes('ai')) return 2;
      // 根据进度百分比粗略映射步骤
      const percent = typeof taskStatus.progress === 'number'
        ? Math.round(taskStatus.progress as unknown as number)
        : Math.round((taskStatus.progress?.percentage || 0));
      if (percent >= 75) return 2;
      if (percent >= 25) return 1;
      return 0;
    }
    if (status === 'completed') return 3;
    if (status === 'failed') {
      const step = (taskStatus.current_step || '').toString();
      if (step.includes('摘要') || step.toLowerCase().includes('ai')) return 2;
      return 1;
    }
    
    return 0;
  };

  const getProgressPercent = () => {
    if (!taskStatus) return 0;
    
    const { status, progress } = taskStatus;
    
    if (status === 'completed') return 100;
    if (status === 'failed') return 0;
    if (status === 'pending') return 0;
    
    // 后端返回的 progress 可能是数字（百分比），也可能是对象
    if (typeof progress === 'number') {
      return Math.round(progress);
    }
    if (progress) {
      return Math.round(progress.percentage || progress.progress || 0);
    }
    
    return 0;
  };

  const getStatusText = () => {
    const rawKey = (taskStatus?.status || 'pending').toString().toLowerCase();
    return TASK_STATUS_MAP[rawKey as keyof typeof TASK_STATUS_MAP]?.text || '处理中';
  };

  if (loading && !taskStatus) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" />
        <div style={{ marginTop: '16px' }}>
          <Text>正在获取任务状态...</Text>
        </div>
      </div>
    );
  }

  if (error && !taskStatus) {
    return (
      <Card style={{ maxWidth: '600px', margin: '50px auto' }}>
        <Alert
          message="获取任务状态失败"
          description={error}
          type="error"
          showIcon
          action={
            <Space>
              <Button size="small" onClick={handleRetry}>
                重试
              </Button>
              <Button size="small" onClick={() => navigate('/')}>
                返回首页
              </Button>
            </Space>
          }
        />
      </Card>
    );
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      {/* 任务状态卡片 */}
      <Card className="content-card">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div style={{ textAlign: 'center' }}>
            <Title level={3}>
              <span>
                {taskStatus?.status === 'completed' ? (
                  <CheckCircleOutlined style={{ color: '#52c41a', marginRight: '8px' }} />
                ) : taskStatus?.status === 'failed' ? (
                  <CloseCircleOutlined style={{ color: '#ff4d4f', marginRight: '8px' }} />
                ) : (
                  <LoadingOutlined style={{ color: '#1890ff', marginRight: '8px' }} />
                )}
                {getStatusText()}
              </span>
            </Title>
            
            {taskStatus && (
              <Tag color={
              taskStatus.status === 'completed' ? 'green' :
              taskStatus.status === 'failed' ? 'red' :
                taskStatus.status === 'processing' ? 'blue' : 'default'
              }>
                {taskStatus.status}
              </Tag>
            )}
          </div>

          {/* 进度条 */}
          {taskStatus?.status === 'processing' && (
            <div>
              <Progress
                percent={getProgressPercent()}
                status="active"
                strokeColor={{
                  '0%': '#108ee9',
                  '100%': '#87d068',
                }}
              />
              <Text type="secondary" style={{ fontSize: '12px' }}>
                {(taskStatus.current_step && taskStatus.current_step.toString()) || '正在处理...'}
              </Text>
            </div>
          )}

          {/* 处理步骤 */}
          <Steps current={getCurrentStep()} direction="vertical" size="small">
            <Step
              title="任务排队"
              description="等待系统资源分配"
              icon={<LoadingOutlined />}
              status={getStepStatus(0)}
            />
            <Step
              title="语音转录"
              description="使用 Whisper 模型进行语音识别"
              icon={<SoundOutlined />}
              status={getStepStatus(1)}
            />
            <Step
              title="AI 摘要生成"
              description="使用 DeepSeek API 生成会议纪要"
              icon={<BulbOutlined />}
              status={getStepStatus(2)}
            />
            <Step
              title="处理完成"
              description="生成最终结果"
              icon={<FileTextOutlined />}
              status={getStepStatus(3)}
            />
          </Steps>
        </Space>
      </Card>

      {/* 任务详情 */}
      {taskStatus && (
        <Card className="content-card" title="任务详情">
          <Descriptions column={1} size="small">
            <Descriptions.Item label="任务ID">
              <Text code>{taskStatus.task_id}</Text>
            </Descriptions.Item>
            <Descriptions.Item label="创建时间">
              {taskStatus.created_at ? new Date(taskStatus.created_at).toLocaleString() : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="开始时间">
              {taskStatus.started_at ? new Date(taskStatus.started_at).toLocaleString() : '-'}
            </Descriptions.Item>
            {taskStatus.completed_at && (
              <Descriptions.Item label="完成时间">
                {new Date(taskStatus.completed_at).toLocaleString()}
              </Descriptions.Item>
            )}
            {taskStatus.progress && taskStatus.progress.estimated_time && (
              <Descriptions.Item label="预计剩余时间">
                {formatTime(taskStatus.progress.estimated_time)}
              </Descriptions.Item>
            )}
          </Descriptions>
        </Card>
      )}

      {/* 错误信息 */}
      {taskStatus?.status === 'failed' && taskStatus.error && (
        <Card className="content-card">
          <Alert
            message="处理失败"
            description={taskStatus.error}
            type="error"
            showIcon
          />
        </Card>
      )}

      {/* 操作按钮 */}
      <Card className="content-card">
        <Row gutter={16}>
          <Col span={12}>
            <Button
              icon={<HomeOutlined />}
              onClick={() => navigate('/')}
              block
            >
              返回首页
            </Button>
          </Col>
          <Col span={12}>
            {taskStatus?.status === 'processing' ? (
              <Button
                danger
                onClick={handleCancelTask}
                block
              >
                取消任务
              </Button>
            ) : taskStatus?.status === 'failed' ? (
              <Button
                icon={<ReloadOutlined />}
                onClick={handleRetry}
                block
              >
                重新检查
              </Button>
            ) : taskStatus?.status === 'completed' ? (
              <Button
                type="primary"
                onClick={() => navigate(`/result/${taskId}`)}
                block
              >
                查看结果
              </Button>
            ) : null}
          </Col>
        </Row>
      </Card>

      {/* 处理提示 */}
      <Card className="content-card">
        <Alert
          message="处理说明"
          description={
            <ul style={{ margin: 0, paddingLeft: '20px' }}>
              <li>语音转录阶段：系统使用 Whisper 模型将音频转换为文字</li>
              <li>AI 摘要生成阶段：使用 DeepSeek API 分析转录内容并生成结构化纪要</li>
              <li>处理时间取决于音频长度和系统负载</li>
              <li>您可以安全地关闭此页面，稍后通过任务ID查看结果</li>
            </ul>
          }
          type="info"
          showIcon
        />
      </Card>
    </div>
  );
};

export default ProcessingPage;