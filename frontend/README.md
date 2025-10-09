# MeetMemo Frontend

MeetMemo 的前端应用，基于 React + TypeScript + Ant Design 构建的现代化 Web 应用。

## 功能特性

- 🎵 **音频上传**: 支持多种音频格式的拖拽上传
- 📝 **实时处理**: 实时显示转录和AI摘要生成进度
- 📊 **结果展示**: 结构化展示会议纪要和完整转录
- 📤 **多格式导出**: 支持 Markdown、TXT、DOCX、PDF 等格式导出
- 📱 **响应式设计**: 适配桌面端和移动端
- 🎨 **现代化UI**: 基于 Ant Design 的美观界面

## 技术栈

- **React 18** - 前端框架
- **TypeScript** - 类型安全
- **Ant Design** - UI 组件库
- **React Router** - 路由管理
- **Axios** - HTTP 客户端
- **Vite** - 构建工具

## 项目结构

```
frontend/
├── public/                 # 静态资源
│   ├── index.html         # HTML 模板
│   ├── manifest.json      # PWA 配置
│   └── favicon.ico        # 网站图标
├── src/
│   ├── components/        # 可复用组件
│   │   ├── AppHeader.tsx  # 应用头部
│   │   ├── AppFooter.tsx  # 应用底部
│   │   ├── UploadComponent.tsx # 上传组件
│   │   └── index.ts       # 组件导出
│   ├── pages/             # 页面组件
│   │   ├── HomePage.tsx   # 首页
│   │   ├── ProcessingPage.tsx # 处理页面
│   │   ├── ResultPage.tsx # 结果页面
│   │   └── index.ts       # 页面导出
│   ├── services/          # API 服务
│   │   └── api.ts         # API 接口
│   ├── types/             # TypeScript 类型定义
│   │   └── index.ts       # 类型导出
│   ├── utils/             # 工具函数
│   │   └── index.ts       # 工具函数
│   ├── App.tsx            # 主应用组件
│   ├── index.tsx          # 应用入口
│   └── index.css          # 全局样式
├── package.json           # 项目配置
├── tsconfig.json          # TypeScript 配置
├── .env                   # 环境变量
└── README.md              # 项目说明
```

## 开发指南

### 环境要求

- Node.js >= 16.0.0
- npm >= 8.0.0

### 安装依赖

```bash
cd frontend
npm install
```

### 环境配置

复制环境变量示例文件并根据需要修改：

```bash
cp .env.example .env
```

主要配置项：

- `REACT_APP_API_BASE_URL`: 后端 API 地址
- `REACT_APP_DEBUG`: 是否启用调试模式
- `REACT_APP_API_TIMEOUT`: API 请求超时时间

### 开发运行

```bash
npm start
```

应用将在 http://localhost:3000 启动

### 构建部署

```bash
npm run build
```

构建产物将生成在 `build/` 目录

### 代码检查

```bash
# ESLint 检查
npm run lint

# 代码格式化
npm run format

# 类型检查
npm run type-check
```

### 测试

```bash
npm test
```

## API 接口

前端通过以下主要接口与后端通信：

- `POST /api/upload` - 上传音频文件
- `GET /api/tasks/{task_id}` - 获取任务状态
- `DELETE /api/tasks/{task_id}` - 取消任务
- `GET /api/health` - 健康检查
- `GET /api/upload/formats` - 获取支持的格式

## 组件说明

### AppHeader
应用头部组件，包含导航和品牌信息。

### AppFooter
应用底部组件，包含版权和链接信息。

### UploadComponent
文件上传组件，支持拖拽上传和表单配置。

### HomePage
首页组件，展示应用介绍和上传界面。

### ProcessingPage
处理页面组件，实时显示任务进度。

### ResultPage
结果页面组件，展示转录和摘要结果。

## 样式规范

- 使用 Ant Design 的设计语言
- 响应式设计，支持移动端
- 统一的颜色主题和间距
- 无障碍访问支持

## 部署说明

### 开发环境

```bash
npm start
```

### 生产环境

1. 构建应用：
```bash
npm run build
```

2. 部署到静态文件服务器（如 Nginx）

3. 配置反向代理到后端 API

### Docker 部署

```dockerfile
FROM node:16-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License