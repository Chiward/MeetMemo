// API响应类型
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
}

// 文件上传响应
export interface UploadResponse {
  success: boolean;
  message: string;
  task_id: string;
  file_info: {
    file_id: string;
    original_filename: string;
    file_size: number;
    meeting_title: string;
    language: string;
    upload_time: string;
  };
}

// 任务状态类型
export type TaskStatus = 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';

// 任务进度信息
export interface TaskProgress {
  progress: number;
  current_step: string;
  total_steps: number;
  estimated_time?: number;
  message?: string;
  stage?: string;
  percentage?: number;
}

// 任务状态响应
export interface TaskStatusResponse {
  task_id: string;
  status: TaskStatus;
  message: string;
  progress?: TaskProgress;
  current_step?: string;
  total_steps?: number;
  result?: ProcessingResult;
  error?: string;
  completed_at?: string;
  created_at?: string;
  started_at?: string;
}

// 转录结果
export interface TranscriptionResult {
  text: string;
  language: string;
  segments: TranscriptionSegment[];
  duration: number;
}

// 转录片段
export interface TranscriptionSegment {
  start: number;
  end: number;
  text: string;
}

// AI摘要结果
export interface SummaryResult {
  meeting_title: string;
  title?: string;
  summary: string;
  model_used: string;
  tokens_used: {
    prompt_tokens?: number;
    completion_tokens?: number;
    total_tokens?: number;
  };
  generated_at: string;
  language: string;
  original_text_length: number;
  // 扩展字段，用于结构化摘要
  key_points?: string[];
  main_points?: string[];
  action_items?: Array<{
    task: string;
    assignee?: string;
    deadline?: string;
  }>;
  participants?: string[];
  decisions?: string[];
  next_meeting?: string;
}

// 处理结果
export interface ProcessingResult {
  success: boolean;
  file_id: string;
  transcription: TranscriptionResult;
  summary: SummaryResult;
  result_file: string;
  processing_completed_at: string;
  file_info?: {
    file_id: string;
    original_name: string;
    file_size: number;
    duration: number;
    created_at: string;
  };
  // 支持 minimal_mode
  status?: string;
  message?: string;
  file_uploaded?: boolean;
}

// 文件信息
export interface FileInfo {
  file_id: string;
  original_filename: string;
  file_size: number;
  meeting_title: string;
  language: string;
  upload_time: string;
}

// 支持的音频格式响应
export interface SupportedFormatsResponse {
  supported_formats: string[];
  max_file_size: number;
  max_file_size_mb: number;
}

// 健康检查响应
export interface HealthCheckResponse {
  status: string;
  timestamp: string;
  service: string;
  version: string;
  dependencies?: {
    [key: string]: {
      status: string;
      [key: string]: any;
    };
  };
}

// 上传参数
export interface UploadParams {
  file: File;
  meeting_title?: string;
  language?: string;
  whisper_model?: WhisperModel;
}

// 语言选项
export interface LanguageOption {
  value: string;
  label: string;
}

// 导出格式类型
export type ExportFormat = 'markdown' | 'txt' | 'docx' | 'pdf';

// Whisper模型类型
export type WhisperModel = 'base' | 'large' | 'turbo';

// Whisper模型选项接口
export interface WhisperModelOption {
  value: WhisperModel;
  label: string;
  description: string;
  size: string;
  speed: string;
}

// 应用状态
export interface AppState {
  currentTask?: {
    taskId: string;
    fileInfo: FileInfo;
    status: TaskStatus;
    progress?: TaskProgress;
  };
  results: {
    [taskId: string]: ProcessingResult;
  };
  loading: boolean;
  error?: string;
}

// 组件Props类型
export interface UploadComponentProps {
  onUploadSuccess: (response: UploadResponse) => void;
  onUploadError: (error: string) => void;
}

export interface ProcessingComponentProps {
  taskId: string;
  onComplete: (result: ProcessingResult) => void;
  onError: (error: string) => void;
}

export interface ResultComponentProps {
  result: ProcessingResult;
  onExport: (format: ExportFormat) => void;
  onNewUpload: () => void;
}