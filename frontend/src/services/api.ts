import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  UploadResponse,
  TaskStatusResponse,
  SupportedFormatsResponse,
  HealthCheckResponse,
  UploadParams,
} from '@/types';

// 创建axios实例
const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  timeout: parseInt(process.env.REACT_APP_API_TIMEOUT || '120000'), // 增加到2分钟
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // 统一错误处理
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        '网络请求失败';
    
    console.error('API Error:', errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
);

// API服务类
export class ApiService {
  /**
   * 上传音频文件
   */
  static async uploadAudio(params: UploadParams): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', params.file);
    
    if (params.meeting_title) {
      formData.append('meeting_title', params.meeting_title);
    }
    
    if (params.language) {
      formData.append('language', params.language);
    }

    if (params.whisper_model) {
      formData.append('whisper_model', params.whisper_model);
    }

    const response = await api.post<UploadResponse>('/api/upload/audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 300000, // 音频上传设置5分钟超时
    });

    return response.data;
  }

  /**
   * 获取任务状态
   */
  static async getTaskStatus(taskId: string): Promise<TaskStatusResponse> {
    const response = await api.get<TaskStatusResponse>(`/api/tasks/${taskId}`);
    return response.data;
  }

  /**
   * 取消任务
   */
  static async cancelTask(taskId: string): Promise<{ success: boolean; message: string }> {
    const response = await api.delete(`/api/tasks/${taskId}`);
    return response.data;
  }

  /**
   * 获取支持的音频格式
   */
  static async getSupportedFormats(): Promise<SupportedFormatsResponse> {
    const response = await api.get<SupportedFormatsResponse>('/api/upload/formats');
    return response.data;
  }

  /**
   * 健康检查
   */
  static async healthCheck(): Promise<HealthCheckResponse> {
    const response = await api.get<HealthCheckResponse>('/api/health');
    return response.data;
  }

  /**
   * 详细健康检查
   */
  static async detailedHealthCheck(): Promise<HealthCheckResponse> {
    const response = await api.get<HealthCheckResponse>('/api/health/detailed');
    return response.data;
  }

  /**
   * 删除音频文件
   */
  static async deleteAudioFile(fileId: string): Promise<{ success: boolean; message: string }> {
    const response = await api.delete(`/api/upload/audio/${fileId}`);
    return response.data;
  }

  /**
   * 获取活跃任务列表
   */
  static async getActiveTasks(): Promise<any> {
    const response = await api.get('/api/tasks/');
    return response.data;
  }

  /**
   * 获取任务统计
   */
  static async getTaskStats(): Promise<any> {
    const response = await api.get('/api/tasks/stats/summary');
    return response.data;
  }
}

// 导出axios实例供其他地方使用
export default api;