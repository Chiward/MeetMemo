import React, { useState, useCallback } from 'react';
import {
  Upload,
  Button,
  Form,
  Input,
  Select,
  Space,
  Typography,
  Progress,
  Alert,
  Card,
  Tooltip
} from 'antd';
import {
  InboxOutlined,
  CloudUploadOutlined,
  LoadingOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import type { UploadProps, UploadFile } from 'antd';

import { ApiService } from '../services/api';
import { UploadComponentProps, LanguageOption, WhisperModelOption } from '../types';
import { validateAudioFile, formatFileSize, LANGUAGE_OPTIONS, WHISPER_MODEL_OPTIONS } from '../utils';

const { Dragger } = Upload;
const { Text } = Typography;
const { Option } = Select;

const UploadComponent: React.FC<UploadComponentProps> = ({
  onUploadSuccess,
  onUploadError
}) => {
  const [form] = Form.useForm();
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const handleUpload = useCallback(async () => {
    if (fileList.length === 0) {
      onUploadError('请选择要上传的音频文件');
      return;
    }

    try {
      await form.validateFields();
      const values = form.getFieldsValue();
      const file = fileList[0].originFileObj as File;

      setUploading(true);
      setUploadProgress(0);

      const response = await ApiService.uploadAudio({
        file: file,
        meeting_title: values.title || file.name,
        language: values.language || 'auto',
        whisper_model: values.whisper_model || 'base'
      });

      onUploadSuccess(response);
      
      // 重置表单
      form.resetFields();
      setFileList([]);
      setUploadProgress(0);
      
    } catch (error: any) {
      console.error('上传失败:', error);
      onUploadError(error.message || '上传失败，请重试');
    } finally {
      setUploading(false);
    }
  }, [fileList, form, onUploadSuccess, onUploadError]);

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    fileList,
    beforeUpload: (file: File) => {
      const validation = validateAudioFile(file);
      if (!validation.isValid) {
        onUploadError(validation.error || '文件格式不支持');
        return false;
      }
      
      setFileList([{
        uid: file.name + Date.now(),
        name: file.name,
        status: 'done',
        originFileObj: file as any
      }]);
      return false; // 阻止自动上传
    },
    onRemove: () => {
      setFileList([]);
    },
    showUploadList: {
      showRemoveIcon: true,
      showPreviewIcon: false,
      showDownloadIcon: false
    }
  };

  return (
    <Card>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 文件上传区域 */}
        <Dragger 
          {...uploadProps} 
          disabled={uploading}
          style={{
            background: uploading ? '#f5f5f5' : 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            border: uploading ? '2px dashed #d9d9d9' : '2px dashed #1890ff',
            borderRadius: '12px',
            transition: 'all 0.3s ease'
          }}
        >
          <p className="ant-upload-drag-icon">
            {uploading ? (
              <LoadingOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
            ) : (
              <InboxOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
            )}
          </p>
          <p className="ant-upload-text" style={{ fontSize: '18px', fontWeight: 'bold' }}>
            {uploading ? '🚀 正在上传处理中...' : '📁 点击或拖拽音频文件到此区域上传'}
          </p>
          <p className="ant-upload-hint" style={{ fontSize: '14px', color: '#666' }}>
            🎵 支持 MP3、WAV、M4A、FLAC、OGG 等格式，最大 500MB
          </p>
        </Dragger>

        {/* 上传进度 */}
        {uploading && (
          <div>
            <Text>上传进度:</Text>
            <Progress 
              percent={uploadProgress} 
              status={uploadProgress === 100 ? 'success' : 'active'}
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
            />
          </div>
        )}

        {/* 文件信息显示 */}
        {fileList.length > 0 && !uploading && (
          <Alert
            message="文件已选择"
            description={
              <Space direction="vertical" size="small">
                <Text>文件名: {fileList[0].name}</Text>
                <Text>文件大小: {formatFileSize((fileList[0].originFileObj as File)?.size || 0)}</Text>
              </Space>
            }
            type="info"
            showIcon
          />
        )}

        {/* 配置表单 */}
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            language: 'auto',
            whisper_model: 'base'
          }}
        >
          <Form.Item
            label="会议标题"
            name="title"
            extra="可选，如不填写将使用文件名"
          >
            <Input 
              placeholder="请输入会议标题"
              disabled={uploading}
            />
          </Form.Item>

          <Form.Item
            label="转录语言"
            name="language"
            extra="选择音频的主要语言，选择'自动检测'将由系统自动识别"
          >
            <Select disabled={uploading}>
              {LANGUAGE_OPTIONS.map((option: LanguageOption) => (
                <Option key={option.value} value={option.value}>
                  {option.label}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            label={
              <Space>
                选择模型
                <Tooltip title="不同模型在速度和准确性之间有不同的平衡">
                  <InfoCircleOutlined style={{ color: '#1890ff' }} />
                </Tooltip>
              </Space>
            }
            name="whisper_model"
            extra="Base模型速度快，Large模型准确性高，Turbo模型处理最快"
          >
            <Select disabled={uploading}>
              {WHISPER_MODEL_OPTIONS.map((option: WhisperModelOption) => (
                <Option key={option.value} value={option.value}>
                  <div className="model-select-option">
                    <div className="model-info">
                      <div className="model-details">
                        <div className="model-title">{option.label}</div>
                        <div className="model-description">
                          {option.description}
                        </div>
                      </div>
                      <div className="model-specs">
                        <div>大小: {option.size}</div>
                        <div>速度: {option.speed}</div>
                      </div>
                    </div>
                  </div>
                </Option>
              ))}
            </Select>
          </Form.Item>
        </Form>

        {/* 上传按钮 */}
        <Button
          type="primary"
          size="large"
          icon={<CloudUploadOutlined />}
          onClick={handleUpload}
          loading={uploading}
          disabled={fileList.length === 0}
          block
          style={{
            height: '50px',
            fontSize: '16px',
            fontWeight: 'bold',
            background: fileList.length === 0 ? '#d9d9d9' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            borderRadius: '8px',
            boxShadow: fileList.length > 0 ? '0 4px 15px rgba(102, 126, 234, 0.4)' : 'none',
            transition: 'all 0.3s ease'
          }}
        >
          {uploading ? '🚀 正在上传处理中...' : '✨ 开始上传并处理'}
        </Button>

        {/* 使用提示 */}
        <Alert
          message="温馨提示"
          description={
            <ul style={{ margin: 0, paddingLeft: '20px' }}>
              <li>为获得最佳转录效果，建议上传清晰的录音文件</li>
              <li>处理时间取决于音频长度，通常为音频时长的 1/3 到 1/2</li>
              <li>上传后您将跳转到处理页面查看实时进度</li>
              <li>Base模型适合日常使用，Large模型适合重要会议，Turbo模型适合快速转录</li>
            </ul>
          }
          type="info"
          showIcon
        />
      </Space>
    </Card>
  );
};

export default UploadComponent;