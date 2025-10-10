import { saveAs } from 'file-saver';
import { ExportFormat, WhisperModelOption } from '@/types';

/**
 * 格式化文件大小
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

/**
 * 格式化时间
 */
export const formatTime = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
};

/**
 * 格式化日期时间
 */
export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};

/**
 * 验证音频文件格式
 */
export const validateAudioFile = (file: File, allowedFormats?: string[]): { isValid: boolean; error?: string } => {
  const defaultFormats = ['mp3', 'wav', 'flac', 'm4a', 'aac', 'ogg', 'wma'];
  const formats = allowedFormats || defaultFormats;
  const fileExtension = file.name.split('.').pop()?.toLowerCase();
  
  if (!fileExtension) {
    return { isValid: false, error: '无法识别文件格式' };
  }
  
  if (!formats.includes(fileExtension)) {
    return { isValid: false, error: `不支持的文件格式: .${fileExtension}` };
  }
  
  return { isValid: true };
};

/**
 * 获取文件扩展名
 */
export const getFileExtension = (filename: string): string => {
  return filename.split('.').pop()?.toLowerCase() || '';
};

/**
 * 生成唯一ID
 */
export const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

/**
 * 防抖函数
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

/**
 * 节流函数
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};

/**
 * 导出文件
 */
export const exportFile = (content: string, filename: string, format: ExportFormat): void => {
  let blob: Blob;
  let finalFilename: string;
  
  switch (format) {
    case 'markdown':
      blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
      finalFilename = `${filename}.md`;
      break;
      
    case 'txt':
      blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      finalFilename = `${filename}.txt`;
      break;
      
    default:
      blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      finalFilename = `${filename}.txt`;
  }
  
  saveAs(blob, finalFilename);
};

/**
 * 复制文本到剪贴板
 */
export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    } else {
      // 降级方案
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      
      const result = document.execCommand('copy');
      document.body.removeChild(textArea);
      return result;
    }
  } catch (error) {
    console.error('复制到剪贴板失败:', error);
    return false;
  }
};

/**
 * 获取错误消息
 */
export const getErrorMessage = (error: any): string => {
  if (typeof error === 'string') {
    return error;
  }
  
  if (error?.message) {
    return error.message;
  }
  
  if (error?.response?.data?.detail) {
    return error.response.data.detail;
  }
  
  if (error?.response?.data?.message) {
    return error.response.data.message;
  }
  
  return '发生未知错误';
};

// 语言选项
export const LANGUAGE_OPTIONS = [
  { value: 'auto', label: '自动检测' },
  { value: 'zh', label: '中文' },
  { value: 'en', label: '英文' },
  { value: 'ja', label: '日文' },
  { value: 'ko', label: '韩文' },
  { value: 'es', label: '西班牙文' },
  { value: 'fr', label: '法文' },
  { value: 'de', label: '德文' },
  { value: 'ru', label: '俄文' },
];

// Whisper模型选项
export const WHISPER_MODEL_OPTIONS: WhisperModelOption[] = [
  { 
    value: 'base' as const, 
    label: 'Base（基础模型）', 
    description: '平衡速度和准确性的基础模型',
    size: '~140MB',
    speed: '快速'
  },
  { 
    value: 'large' as const, 
    label: 'Large（大型模型）', 
    description: '最高准确性，适合重要会议',
    size: '~3GB',
    speed: '较慢'
  },
  { 
    value: 'turbo' as const, 
    label: 'Turbo（极速模型）', 
    description: '最快处理速度，适合快速转录',
    size: '~800MB',
    speed: '极快'
  },
];

/**
 * 导出格式选项
 */
export const EXPORT_FORMAT_OPTIONS = [
  { value: 'markdown', label: 'Markdown (.md)' },
  { value: 'txt', label: '纯文本 (.txt)' },
];

/**
 * 任务状态映射
 */
export const TASK_STATUS_MAP = {
  pending: { text: '等待处理', color: 'default' },
  processing: { text: '处理中', color: 'processing' },
  completed: { text: '已完成', color: 'success' },
  failed: { text: '处理失败', color: 'error' },
  cancelled: { text: '已取消', color: 'warning' },
};

/**
 * 语言代码到中文显示名称的映射
 */
export const LANGUAGE_DISPLAY_MAP: { [key: string]: string } = {
  'auto': '自动检测',
  'zh': '中文',
  'en': '英文',
  'ja': '日文',
  'ko': '韩文',
  'es': '西班牙文',
  'fr': '法文',
  'de': '德文',
  'ru': '俄文',
  'pt': '葡萄牙文',
  'it': '意大利文',
  'ar': '阿拉伯文',
  'hi': '印地文',
  'th': '泰文',
  'vi': '越南文',
  'tr': '土耳其文',
  'pl': '波兰文',
  'nl': '荷兰文',
  'sv': '瑞典文',
  'da': '丹麦文',
  'no': '挪威文',
  'fi': '芬兰文',
  'cs': '捷克文',
  'sk': '斯洛伐克文',
  'hu': '匈牙利文',
  'ro': '罗马尼亚文',
  'bg': '保加利亚文',
  'hr': '克罗地亚文',
  'sr': '塞尔维亚文',
  'sl': '斯洛文尼亚文',
  'et': '爱沙尼亚文',
  'lv': '拉脱维亚文',
  'lt': '立陶宛文',
  'uk': '乌克兰文',
  'be': '白俄罗斯文',
  'mk': '马其顿文',
  'mt': '马耳他文',
  'is': '冰岛文',
  'ga': '爱尔兰文',
  'cy': '威尔士文',
  'eu': '巴斯克文',
  'ca': '加泰罗尼亚文',
  'gl': '加利西亚文',
  'ast': '阿斯图里亚斯文',
  'unknown': '未知语言'
};

/**
 * 获取语言的中文显示名称
 * @param languageCode 语言代码
 * @returns 中文显示名称
 */
export const getLanguageDisplayName = (languageCode: string): string => {
  return LANGUAGE_DISPLAY_MAP[languageCode] || languageCode;
};