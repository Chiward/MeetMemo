# MeetMemo 部署指南

## 部署环境要求

### 最小系统要求
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **内存**: 4GB RAM (推荐 8GB+)
- **存储**: 10GB 可用空间
- **网络**: 稳定的互联网连接 (用于AI API调用)

### 软件依赖
- **Python**: 3.9 或更高版本
- **Node.js**: 16.0 或更高版本
- **npm**: 8.0 或更高版本

## 部署方式

### 1. 开发环境部署 (推荐新手)

#### 步骤1: 环境准备
```bash
# 检查Python版本
python --version

# 检查Node.js版本
node --version
npm --version

# 安装Python依赖管理工具
pip install --upgrade pip
```

#### 步骤2: 克隆项目
```bash
git clone <your-repository-url>
cd MeetMemo3
```

#### 步骤3: 后端配置
```bash
cd backend

# 复制环境变量文件
cp .env.example .env

# 编辑环境变量 (重要!)
# 使用文本编辑器打开 .env 文件，设置以下变量:
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# DEEPSEEK_BASE_URL=https://api.deepseek.com
```

#### 步骤4: 前端配置
```bash
cd ../frontend

# 复制环境变量文件
cp .env.example .env

# 安装前端依赖
npm install
```

#### 步骤5: 启动服务

**终端1 - 启动后端:**
```bash
cd backend
python start_minimal.py
```

**终端2 - 启动前端:**
```bash
cd frontend
npm start
```

#### 步骤6: 验证部署
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 2. Docker部署 (推荐生产环境)

#### 前提条件
- 安装 Docker Desktop
- 安装 Docker Compose

#### 部署步骤
```bash
# 克隆项目
git clone <your-repository-url>
cd MeetMemo3

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 停止服务
```bash
docker-compose down
```

## 环境变量配置

### 后端环境变量 (.env)
```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=false

# 文件上传配置
MAX_FILE_SIZE=524288000  # 500MB
UPLOAD_DIR=./uploads

# 数据库配置 (可选)
DATABASE_URL=sqlite:///./meetmemo.db

# Redis配置 (可选，用于Celery)
REDIS_URL=redis://localhost:6379/0
```

### 前端环境变量 (.env)
```env
# API服务器地址
REACT_APP_API_BASE_URL=http://localhost:8000

# 应用配置
REACT_APP_APP_NAME=MeetMemo
REACT_APP_VERSION=1.0.0
```

## 故障排除

### 常见问题及解决方案

#### 1. 后端启动失败
**问题**: `ImportError: No module named 'xxx'`
**解决**: 
```bash
cd backend
pip install -r requirements_minimal.txt
```

#### 2. 前端启动失败
**问题**: `npm ERR! missing script: start`
**解决**: 
```bash
cd frontend
npm install
npm start  # 不是 npm run dev
```

#### 3. API连接失败
**问题**: 前端无法连接后端API
**解决**: 
- 检查后端服务是否正常运行 (http://localhost:8000/health)
- 检查前端环境变量 `REACT_APP_API_BASE_URL`
- 确认防火墙设置

#### 4. DeepSeek API调用失败
**问题**: AI功能无法使用
**解决**: 
- 验证API Key是否正确
- 检查网络连接
- 确认API余额充足

#### 5. 文件上传失败
**问题**: 音频文件无法上传
**解决**: 
- 检查文件格式是否支持 (mp3, wav, m4a, flac, ogg)
- 确认文件大小不超过500MB
- 检查uploads目录权限

### 日志查看

#### 开发环境
- 后端日志: 直接在终端查看
- 前端日志: 浏览器开发者工具 Console

#### Docker环境
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend

# 实时查看日志
docker-compose logs -f
```

## 性能优化建议

### 1. 系统资源
- 确保至少4GB可用内存
- 使用SSD存储提高I/O性能
- 关闭不必要的后台程序

### 2. 网络优化
- 使用稳定的网络连接
- 考虑使用CDN加速静态资源
- 配置适当的超时设置

### 3. 应用优化
- 定期清理uploads目录
- 监控API调用频率
- 使用生产环境构建版本

## 安全注意事项

1. **API Key安全**
   - 不要将API Key提交到版本控制系统
   - 定期轮换API Key
   - 使用环境变量存储敏感信息

2. **文件上传安全**
   - 验证文件类型和大小
   - 定期清理临时文件
   - 限制上传频率

3. **网络安全**
   - 使用HTTPS (生产环境)
   - 配置适当的CORS策略
   - 实施访问控制

## 监控和维护

### 健康检查
- 定期访问 http://localhost:8000/health
- 监控服务器资源使用情况
- 检查日志文件中的错误信息

### 备份策略
- 定期备份配置文件
- 备份重要的音频文件和结果
- 保存环境变量配置

### 更新维护
- 定期更新依赖包
- 关注安全补丁
- 测试新版本功能

---

如有部署问题，请参考项目文档或提交Issue获取帮助。