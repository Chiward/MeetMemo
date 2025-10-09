import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Typography,
  Space,
  Button,
  Alert,
  Spin,
  Tabs,
  Tag,
  Descriptions,
  Row,
  Col,
  Modal,
  App
} from 'antd';
import {
  FileTextOutlined,
  SoundOutlined,
  DownloadOutlined,
  CopyOutlined,
  HomeOutlined,
  ShareAltOutlined,
  DeleteOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';

import { ApiService } from '../services/api';
import { TaskStatusResponse, ProcessingResult, ExportFormat } from '../types';
import { 
  formatTime, 
  formatDateTime, 
  getErrorMessage, 
  exportFile, 
  copyToClipboard,
  EXPORT_FORMAT_OPTIONS,
  getLanguageDisplayName
} from '../utils';

const { Title, Text, Paragraph } = Typography;

const ResultPage: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const { message } = App.useApp();
  
  const [taskStatus, setTaskStatus] = useState<TaskStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exporting, setExporting] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) {
      setError('无效的任务ID');
      setLoading(false);
      return;
    }

    fetchTaskResult();
  }, [taskId]);

  const fetchTaskResult = async () => {
    if (!taskId) return;

    try {
      const status = await ApiService.getTaskStatus(taskId);
      
      // 检查是否为minimal模式
      if (status.result?.status === 'minimal_mode') {
        setTaskStatus(status);
        setError(null);
        setLoading(false);
        return;
      }
      
      if (status.status !== 'completed') {
        setError('任务尚未完成或处理失败');
        setLoading(false);
        return;
      }

      setTaskStatus(status);
      setError(null);
    } catch (err) {
      console.error('获取任务结果失败:', err);
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format: ExportFormat) => {
    if (!taskStatus?.result) return;

    try {
      setExporting(format);
      
      const result = taskStatus?.result;
      const title = result.transcription?.text?.substring(0, 20) || `会议纪要_${taskId}`;
      
      let content = '';
      if (format === 'markdown') {
        content = generateMarkdownContent(result);
      } else if (format === 'txt') {
        content = generateTextContent(result);
      }
      
      await exportFile(content, title, format);
      message.success('导出成功');
    } catch (err) {
      console.error('导出失败:', err);
      message.error('导出失败: ' + getErrorMessage(err));
    } finally {
      setExporting(null);
    }
  };

  const handleCopy = async (content: string, type: string) => {
    try {
      await copyToClipboard(content);
      message.success(`${type}已复制到剪贴板`);
    } catch (err) {
      message.error('复制失败');
    }
  };

  const handleDelete = () => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个任务的结果吗？此操作不可撤销。',
      okText: '确认删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: async () => {
        try {
          if (taskStatus?.result?.file_info?.file_id) {
            await ApiService.deleteAudioFile(taskStatus.result.file_info.file_id);
          }
          message.success('删除成功');
          navigate('/');
        } catch (err) {
          message.error('删除失败: ' + getErrorMessage(err));
        }
      }
    });
  };

  const generateMarkdownContent = (result: ProcessingResult): string => {
    const { transcription, summary, file_info } = result;
    
    let content = '';
    
    // 如果有DeepSeek生成的完整摘要，直接使用
    if (summary && summary.summary) {
      content += summary.summary;
      content += '\n\n---\n\n';
    }
    
    // 添加文件信息
    if (file_info) {
      content += `## 文件信息\n\n`;
      content += `- **文件名**: ${file_info.original_name}\n`;
      content += `- **文件大小**: ${(file_info.file_size / 1024 / 1024).toFixed(2)} MB\n`;
      content += `- **音频时长**: ${formatTime(file_info.duration || 0)}\n`;
      content += `- **处理时间**: ${formatDateTime(file_info.created_at)}\n`;
      if (summary) {
        content += `- **AI模型**: ${summary.model_used}\n`;
        content += `- **Token使用**: ${summary.tokens_used?.total_tokens || 0}\n`;
      }
      content += '\n';
    }
    
    // 如果没有DeepSeek摘要，使用传统格式
    if (!summary || !summary.summary) {
      content += `# 会议纪要\n\n`;
      
      if (summary) {
        content += `## 会议摘要\n\n`;
        content += `### 会议主题\n${summary.title || summary.meeting_title || '未指定'}\n\n`;
        content += `### 主要内容\n${summary.main_points?.join('\n') || '无'}\n\n`;
        content += `### 决策事项\n${summary.decisions?.join('\n') || '无'}\n\n`;
        content += `### 行动项\n${summary.action_items?.join('\n') || '无'}\n\n`;
        if (summary.participants && summary.participants.length > 0) {
          content += `### 参与人员\n${summary.participants.join(', ')}\n\n`;
        }
      }
    }
    
    // 添加完整转录
    if (transcription) {
      content += `## 完整转录\n\n`;
      if (transcription.segments && transcription.segments.length > 0) {
        transcription.segments.forEach((segment, index) => {
          const startTime = formatTime(segment.start);
          const endTime = formatTime(segment.end);
          if (segment.text.trim()) {
            content += `**[${startTime} - ${endTime}]** ${segment.text}\n\n`;
          }
        });
      } else {
        content += transcription.text || '转录内容为空';
      }
    }
    
    return content;
  };

  const generateTextContent = (result: ProcessingResult): string => {
    const { transcription, summary, file_info } = result;
    
    let content = '';
    
    // 如果有DeepSeek生成的完整摘要，先转换为纯文本格式
    if (summary && summary.summary) {
      // 将Markdown格式转换为纯文本
      const plainTextSummary = summary.summary
        .replace(/^#+\s*/gm, '') // 移除标题标记
        .replace(/\*\*(.*?)\*\*/g, '$1') // 移除粗体标记
        .replace(/\*(.*?)\*/g, '$1') // 移除斜体标记
        .replace(/`(.*?)`/g, '$1') // 移除代码标记
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // 移除链接，保留文本
        .replace(/^\s*[-*+]\s+/gm, '• ') // 将列表标记转换为项目符号
        .replace(/\n{3,}/g, '\n\n'); // 减少多余的空行
      
      content += plainTextSummary;
      content += '\n\n' + '='.repeat(50) + '\n\n';
    }
    
    // 添加文件信息
    if (file_info) {
      content += `文件信息:\n`;
      content += `文件名: ${file_info.original_name}\n`;
      content += `文件大小: ${(file_info.file_size / 1024 / 1024).toFixed(2)} MB\n`;
      content += `音频时长: ${formatTime(file_info.duration || 0)}\n`;
      content += `处理时间: ${formatDateTime(file_info.created_at)}\n`;
      if (summary) {
        content += `AI模型: ${summary.model_used}\n`;
        content += `Token使用: ${summary.tokens_used?.total_tokens || 0}\n`;
      }
      content += '\n';
    }
    
    // 如果没有DeepSeek摘要，使用传统格式
    if (!summary || !summary.summary) {
      content += `会议纪要\n${'='.repeat(50)}\n\n`;
      
      if (summary) {
        content += `会议摘要:\n${'-'.repeat(30)}\n`;
        content += `会议主题: ${summary.title || summary.meeting_title || '未指定'}\n\n`;
        content += `主要内容:\n${summary.main_points?.join('\n') || '无'}\n\n`;
        content += `决策事项:\n${summary.decisions?.join('\n') || '无'}\n\n`;
        content += `行动项:\n${summary.action_items?.join('\n') || '无'}\n\n`;
        if (summary.participants && summary.participants.length > 0) {
          content += `参与人员: ${summary.participants.join(', ')}\n\n`;
        }
      }
    }
    
    // 添加完整转录
    if (transcription) {
      content += `完整转录:\n${'-'.repeat(30)}\n`;
      if (transcription.segments && transcription.segments.length > 0) {
        transcription.segments.forEach((segment) => {
          const startTime = formatTime(segment.start);
          const endTime = formatTime(segment.end);
          if (segment.text.trim()) {
            content += `[${startTime} - ${endTime}] ${segment.text}\n\n`;
          }
        });
      } else {
        content += transcription.text || '转录内容为空';
      }
    }
    
    return content;
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" />
        <div style={{ marginTop: '16px' }}>
          <Text>正在加载结果...</Text>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Card style={{ maxWidth: '600px', margin: '50px auto' }}>
        <Alert
          message="加载失败"
          description={error}
          type="error"
          showIcon
          action={
            <Space>
              <Button size="small" onClick={fetchTaskResult}>
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

  const result = taskStatus?.result;
  
  // 处理minimal模式
  if (result?.status === 'minimal_mode') {
    return (
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <Card className="content-card">
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            <div style={{ textAlign: 'center' }}>
              <Title level={2}>
                <FileTextOutlined style={{ color: '#1890ff', marginRight: '8px' }} />
                文件上传成功
              </Title>
              <Tag color="blue">最小化模式</Tag>
            </div>
            
            <Alert
              message="当前为最小化模式"
              description={
                <div>
                  <p>您的音频文件已成功上传，但当前系统运行在最小化模式下。</p>
                  <p><strong>要获得完整的音频转录和AI摘要功能，需要：</strong></p>
                  <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                    <li>启动完整的后端服务（包含 Celery worker）</li>
                    <li>安装完整的依赖包（Whisper 模型、DeepSeek API 等）</li>
                  </ul>
                  <p style={{ marginTop: '12px' }}>
                    <strong>文件ID：</strong> <Text code>{taskId}</Text>
                  </p>
                </div>
              }
              type="info"
              showIcon
            />

            <Card title="上传信息" size="small">
              <Descriptions column={1} size="small">
                <Descriptions.Item label="任务ID">
                  <Text code>{taskStatus?.task_id}</Text>
                </Descriptions.Item>
                <Descriptions.Item label="状态">
                  <Tag color="green">文件已上传</Tag>
                </Descriptions.Item>
                <Descriptions.Item label="模式">
                  <Tag color="blue">最小化模式</Tag>
                </Descriptions.Item>
              </Descriptions>
            </Card>

            <Card title="下一步操作" size="small">
              <Space direction="vertical" style={{ width: '100%' }}>
                <Alert
                  message="启动完整模式"
                  description="要处理您的音频文件，请按照部署文档启动完整的后端服务"
                  type="warning"
                  showIcon
                />
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
                    <Button
                      type="primary"
                      onClick={() => window.open('/DEPLOYMENT.md', '_blank')}
                      block
                    >
                      查看部署文档
                    </Button>
                  </Col>
                </Row>
              </Space>
            </Card>
          </Space>
        </Card>
      </div>
    );
  }
  
  if (!result) {
    return (
      <Card style={{ maxWidth: '600px', margin: '50px auto' }}>
        <Alert
          message="无结果数据"
          description="任务可能尚未完成或结果已被删除"
          type="warning"
          showIcon
          action={
            <Button onClick={() => navigate('/')}>
              返回首页
            </Button>
          }
        />
      </Card>
    );
  }

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      {/* 结果概览 */}
      <Card className="content-card">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div style={{ textAlign: 'center' }}>
            <Title level={2}>
              <FileTextOutlined style={{ color: '#52c41a', marginRight: '8px' }} />
              处理完成
            </Title>
            <Tag color="green">已完成</Tag>
          </div>

          {/* 文件信息 */}
          {result.file_info && (
            <Descriptions title="文件信息" column={2} size="small">
              <Descriptions.Item label="文件名">
                {result.file_info.original_name}
              </Descriptions.Item>
              <Descriptions.Item label="文件大小">
                {(result.file_info.file_size / 1024 / 1024).toFixed(2)} MB
              </Descriptions.Item>
              <Descriptions.Item label="音频时长">
                <ClockCircleOutlined style={{ marginRight: '4px' }} />
                {formatTime(result.file_info.duration || 0)}
              </Descriptions.Item>
              <Descriptions.Item label="处理时间">
                {formatDateTime(result.file_info.created_at)}
              </Descriptions.Item>
            </Descriptions>
          )}

          {/* 操作按钮 */}
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={6}>
              <Button
                icon={<HomeOutlined />}
                onClick={() => navigate('/')}
                block
              >
                返回首页
              </Button>
            </Col>
            <Col xs={24} sm={6}>
              <Button
                icon={<ShareAltOutlined />}
                onClick={() => handleCopy(window.location.href, '分享链接')}
                block
              >
                分享结果
              </Button>
            </Col>
            <Col xs={24} sm={6}>
              <Button
                type="primary"
                icon={<DownloadOutlined />}
                onClick={() => handleExport('markdown')}
                loading={exporting === 'markdown'}
                block
              >
                导出 Markdown
              </Button>
            </Col>
            <Col xs={24} sm={6}>
              <Button
                danger
                icon={<DeleteOutlined />}
                onClick={handleDelete}
                block
              >
                删除结果
              </Button>
            </Col>
          </Row>
        </Space>
      </Card>

      {/* 结果内容 */}
      <Card className="content-card">
        <Tabs 
          defaultActiveKey="summary" 
          size="large"
          items={[
            {
              key: 'summary',
              label: (
                <span>
                  <FileTextOutlined />
                  会议摘要
                </span>
              ),
              children: result.summary ? (
                <Space direction="vertical" size="large" style={{ width: '100%' }}>
                  <div style={{ textAlign: 'right' }}>
                    <Space>
                      <Button
                        size="small"
                        icon={<CopyOutlined />}
                        onClick={() => handleCopy(
                          result.summary.summary || generateTextContent(result),
                          '会议摘要'
                        )}
                      >
                        复制摘要
                      </Button>
                      {EXPORT_FORMAT_OPTIONS.map(option => (
                        <Button
                          key={option.value}
                          size="small"
                          icon={<DownloadOutlined />}
                          loading={exporting === option.value}
                          onClick={() => handleExport(option.value as ExportFormat)}
                        >
                          {option.label}
                        </Button>
                      ))}
                    </Space>
                  </div>

                  {/* 如果有DeepSeek生成的完整摘要，直接显示 */}
                  {result.summary.summary ? (
                    <Card size="small">
                      <div 
                        className="summary-content"
                        style={{
                          whiteSpace: 'pre-wrap',
                          lineHeight: '1.8',
                          fontSize: '14px'
                        }}
                        dangerouslySetInnerHTML={{
                          __html: result.summary.summary
                            .replace(/\n/g, '<br/>')
                            .replace(/^# (.+)$/gm, '<h1>$1</h1>')
                            .replace(/^## (.+)$/gm, '<h2>$1</h2>')
                            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
                            .replace(/^\*\*(.+)\*\*:/gm, '<strong>$1:</strong>')
                            .replace(/^- (.+)$/gm, '<li>$1</li>')
                            .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')
                            .replace(/<\/ul>\s*<ul>/g, '')
                        }}
                      />
                    </Card>
                  ) : (
                    /* 如果没有完整摘要，使用结构化显示 */
                    <>
                      <Card size="small" title="会议主题">
                        <Text>{result.summary.title || result.summary.meeting_title || '未指定'}</Text>
                      </Card>

                      <Card size="small" title="主要内容">
                        {result.summary.main_points && result.summary.main_points.length > 0 ? (
                          <ul>
                            {result.summary.main_points.map((point: string, index: number) => (
                              <li key={index}>{point}</li>
                            ))}
                          </ul>
                        ) : (
                          <Text type="secondary">无</Text>
                        )}
                      </Card>

                      <Card size="small" title="决策事项">
                        {result.summary.decisions && result.summary.decisions.length > 0 ? (
                          <ul>
                            {result.summary.decisions.map((decision: string, index: number) => (
                              <li key={index}>{decision}</li>
                            ))}
                          </ul>
                        ) : (
                          <Text type="secondary">无</Text>
                        )}
                      </Card>

                      <Card size="small" title="行动项">
                        {result.summary.action_items && result.summary.action_items.length > 0 ? (
                          <ul>
                            {result.summary.action_items.map((item: any, index: number) => (
                              <li key={index}>
                                {typeof item === 'string' ? item : `${item.task}${item.assignee ? ` (负责人: ${item.assignee})` : ''}${item.deadline ? ` (截止: ${item.deadline})` : ''}`}
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <Text type="secondary">无</Text>
                        )}
                      </Card>

                      {result.summary.participants && result.summary.participants.length > 0 && (
                        <Card size="small" title="参与人员">
                          <Space wrap>
                            {result.summary.participants.map((participant: string, index: number) => (
                              <Tag key={index} color="blue">{participant}</Tag>
                            ))}
                          </Space>
                        </Card>
                      )}
                    </>
                  )}
                </Space>
              ) : (
                <Alert
                  message="无摘要数据"
                  description="AI 摘要生成失败或数据丢失"
                  type="warning"
                  showIcon
                />
              )
            },
            {
              key: 'transcription',
              label: (
                <span>
                  <SoundOutlined />
                  完整转录
                </span>
              ),
              children: result.transcription ? (
                <Space direction="vertical" size="large" style={{ width: '100%' }}>
                  <div style={{ textAlign: 'right' }}>
                    <Button
                      size="small"
                      icon={<CopyOutlined />}
                      onClick={() => handleCopy(
                        result.transcription?.text || '',
                        '转录文本'
                      )}
                    >
                      复制转录
                    </Button>
                  </div>

                  <Card size="small">
                    <Descriptions size="small" column={3}>
                      <Descriptions.Item label="语言">
                        {getLanguageDisplayName(result.transcription.language || 'unknown')}
                      </Descriptions.Item>
                      <Descriptions.Item label="总时长">
                        {formatTime(result.transcription.duration || 0)}
                      </Descriptions.Item>
                      <Descriptions.Item label="片段数">
                        {result.transcription.segments?.length || 0}
                      </Descriptions.Item>
                    </Descriptions>
                  </Card>

                  {result.transcription.segments && result.transcription.segments.length > 0 ? (
                    <div>
                      {result.transcription.segments.map((segment: any, index: number) => (
                        <Card key={index} size="small" style={{ marginBottom: '8px' }}>
                          <Space direction="vertical" size="small" style={{ width: '100%' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                              <Tag color="blue">
                                {formatTime(segment.start)} - {formatTime(segment.end)}
                              </Tag>
                              <Text type="secondary" style={{ fontSize: '12px' }}>
                                #{index + 1}
                              </Text>
                            </div>
                            <Paragraph style={{ margin: 0 }}>
                              {segment.text}
                            </Paragraph>
                          </Space>
                        </Card>
                      ))}
                    </div>
                  ) : (
                    <Card size="small">
                      <Paragraph>
                        {result.transcription.text || '转录内容为空'}
                      </Paragraph>
                    </Card>
                  )}
                </Space>
              ) : (
                <Alert
                  message="无转录数据"
                  description="语音转录失败或数据丢失"
                  type="warning"
                  showIcon
                />
              )
            }
          ]}
        />
      </Card>
    </div>
  );
};

export default ResultPage;