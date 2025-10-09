# MeetMemo - AI智能会议纪要生成助手

## 项目简介

MeetMemo是一款基于AI技术的智能会议纪要生成助手，能够将会议音频自动转录并生成专业的结构化会议纪要。系统集成了OpenAI Whisper语音识别和DeepSeek大语言模型，提供从音频到专业会议纪要的一站式解决方案。

### 核心功能

- 🎵 **音频上传**: 支持多种音频格式 (MP3, WAV, M4A, FLAC)
- 🔊 **智能转录**: 基于OpenAI Whisper模型的高精度语音转录
- 📝 **专业纪要生成**: 通过DeepSeek API智能生成结构化会议纪要，包含完整的会议信息、讨论要点、决策事项等
- 📋 **标准化格式**: 自动生成符合企业标准的会议纪要格式
- 📤 **多格式导出**: 支持Markdown、纯文本等格式导出
- 💾 **自动保存**: 生成的会议纪要自动保存，支持历史记录查看

### 技术栈

**前端**:
- React 18 + TypeScript
- Ant Design UI组件库
- Vite构建工具

**后端**:
- FastAPI (Python)
- OpenAI Whisper (离线语音转录)
- DeepSeek API (AI文本处理)
- Celery + Redis (异步任务队列)
- SQLite/PostgreSQL (数据存储)

## 项目状态

✅ **当前状态**: 核心功能已完成 - 音频转录和会议纪要生成功能已集成并测试通过

### 已完成功能
- ✅ 前后端基础架构
- ✅ 音频文件上传和验证
- ✅ Whisper语音转录集成
- ✅ DeepSeek会议纪要生成
- ✅ 专业会议纪要模板
- ✅ 任务状态管理和进度跟踪
- ✅ 结果展示和格式化
- ✅ 用户界面和交互设计
- ✅ TypeScript类型系统
- ✅ 完整工作流程测试

### 功能特色
- 🎯 **智能识别**: 自动识别会议内容并分类整理
- 📊 **结构化输出**: 生成包含会议基本信息、讨论要点、决策事项、行动项等完整结构的纪要
- 🔄 **实时处理**: 异步处理机制，支持大文件处理
- 📱 **响应式设计**: 支持桌面和移动端访问

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- Redis (用于任务队列)
- FFmpeg (用于音频处理)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Chiward/MeetMemo.git
   cd MeetMemo
   ```

2. **配置环境变量**
   ```bash
   # 后端环境变量
   cd backend
   cp .env.example .env
   # 编辑 .env 文件，填入你的DeepSeek API Key
   
   # 前端环境变量
   cd ../frontend
   cp .env.example .env
   ```

3. **启动Redis服务**
   ```bash
   # Windows
   cd redis
   .\redis-server.exe
   
   # Linux/Mac
   redis-server
   ```

4. **启动后端服务**
   ```bash
   cd backend
   pip install -r requirements.txt
   python start_dev.py
   ```

5. **启动Celery工作进程**
   ```bash
   cd backend
   python -m celery -A app.tasks.celery_app worker --loglevel=info --pool=solo
   ```

6. **启动前端服务**
   ```bash
   cd frontend
   npm install
   npm start
   ```

7. **访问应用**
   - 前端: http://localhost:3000
   - 后端API: http://localhost:8000
   - API文档: http://localhost:8000/docs

### Docker部署 (推荐)

```bash
docker-compose up -d
```

## 使用指南

### 基本使用流程

1. **上传音频文件**: 
   - 支持拖拽或点击上传
   - 支持格式：MP3, WAV, M4A, FLAC
   - 文件大小限制：100MB

2. **配置处理参数**:
   - 选择语言（中文/英文）
   - 选择Whisper模型（推荐使用base模型）

3. **开始处理**:
   - 点击"开始生成"按钮
   - 系统将自动进行语音转录和纪要生成

4. **查看结果**:
   - 实时查看处理进度
   - 查看生成的专业会议纪要
   - 包含完整的会议信息、讨论要点、决策事项等

5. **导出和分享**:
   - 复制纪要内容
   - 导出为Markdown或其他格式

### 会议纪要格式

生成的会议纪要包含以下标准化内容：

- **基本信息**: 会议主题、时间、地点、主持人
- **主要讨论内容**: 多个议题及详细讨论要点
- **决策事项**: 会议中达成的重要决定
- **行动项**: 后续需要执行的任务和责任人
- **参会人员**: 与会者名单
- **分发名单**: 纪要接收人员

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的API文档。

### 主要API端点

- `POST /api/upload/audio` - 上传音频文件
- `GET /api/tasks/{task_id}/status` - 查询任务状态
- `GET /api/tasks/{task_id}/result` - 获取处理结果
- `GET /health` - 健康检查

## 开发指南

### 项目结构

```
MeetMemo/
├── frontend/                 # React前端应用
│   ├── src/
│   │   ├── components/      # 可复用组件
│   │   ├── pages/          # 页面组件
│   │   ├── services/       # API调用服务
│   │   ├── types/          # TypeScript类型定义
│   │   └── utils/          # 工具函数
│   └── package.json
├── backend/                 # FastAPI后端应用
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── tasks/          # Celery任务
│   ├── models/             # Whisper模型文件
│   ├── uploads/            # 上传文件存储
│   └── requirements.txt
├── redis/                   # Redis服务文件
├── docker-compose.yml       # Docker配置
├── .env.example            # 环境变量模板
└── README.md
```

### 开发命令

```bash
# 前端开发
cd frontend && npm start

# 后端开发
cd backend && python start_dev.py

# Celery工作进程
cd backend && python -m celery -A app.tasks.celery_app worker --loglevel=info --pool=solo

# 运行测试
cd backend && python test_whisper.py
cd backend && python test_deepseek.py

# 构建生产版本
docker-compose -f docker-compose.yml up --build
```

## 配置说明

### DeepSeek API配置

1. 注册DeepSeek账户并获取API Key
2. 在 `backend/.env` 文件中设置 `DEEPSEEK_API_KEY`
3. 根据需要调整API调用参数

### Whisper模型配置

支持的模型大小：
- `tiny`: 最快，精度较低 (39MB)
- `base`: 平衡速度和精度，推荐 (74MB)
- `small`: 较高精度 (244MB)
- `medium`: 高精度 (769MB)
- `large-v3`: 最高精度，速度较慢 (1550MB)

模型会在首次使用时自动下载到 `backend/models/` 目录。

## 故障排除

### 常见问题

1. **音频转录失败**
   - 检查FFmpeg是否正确安装
   - 确认音频文件格式支持
   - 检查磁盘空间是否充足
   - 查看Celery工作进程日志

2. **API调用失败**
   - 验证DeepSeek API Key是否正确
   - 检查网络连接
   - 查看API调用频率限制
   - 检查后端服务日志

3. **Redis连接失败**
   - 确认Redis服务已启动
   - 检查Redis配置和端口
   - 查看Redis日志

4. **前端无法连接后端**
   - 确认后端服务已启动
   - 检查端口配置是否正确
   - 查看浏览器控制台错误信息

### 日志查看

```bash
# 后端日志
cd backend && tail -f logs/app.log

# Celery日志
cd backend && python -m celery -A app.tasks.celery_app worker --loglevel=debug

# Redis日志
cd redis && .\redis-server.exe --loglevel verbose
```

## 性能优化

- 使用适当的Whisper模型大小平衡速度和精度
- 对于长音频文件，建议使用`base`或`small`模型
- 生产环境建议使用Redis集群和多个Celery工作进程
- 可配置文件上传大小限制和处理超时时间

## 贡献指南

1. Fork项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交Pull Request

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 更新日志

### v1.0.0 (2024-10-09)
- ✅ 完成核心功能开发
- ✅ 集成Whisper语音转录
- ✅ 集成DeepSeek会议纪要生成
- ✅ 实现专业会议纪要模板
- ✅ 完成前后端集成测试

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue: [GitHub Issues](https://github.com/Chiward/MeetMemo/issues)
- 项目主页: [GitHub Repository](https://github.com/Chiward/MeetMemo)

---

**注意**: 请确保在使用前配置好DeepSeek API Key，并根据实际需求选择合适的Whisper模型。