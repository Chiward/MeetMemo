# MeetMemo环境安装指南

## 🚨 重要提示
经过环境检查，发现系统缺少以下必要的运行环境：
- Python 3.9+
- Node.js 16+
- FFmpeg

请按照以下步骤安装这些环境，然后继续项目部署。

## 📋 环境安装清单

### 1. Python 3.9+ 安装

#### 下载和安装
1. 访问 Python 官网：https://www.python.org/downloads/
2. 下载最新的 Python 3.9+ 版本（推荐 3.11 或 3.12）
3. 运行安装程序时，**务必勾选 "Add Python to PATH"**
4. 选择 "Install Now" 进行标准安装

#### 验证安装
安装完成后，打开新的命令提示符窗口，运行：
```bash
python --version
pip --version
```

应该看到类似输出：
```
Python 3.11.x
pip 23.x.x
```

### 2. Node.js 16+ 安装

#### 下载和安装
1. 访问 Node.js 官网：https://nodejs.org/
2. 下载 LTS 版本（推荐，通常是 18.x 或 20.x）
3. 运行安装程序，使用默认设置安装
4. 安装程序会自动添加到 PATH

#### 验证安装
安装完成后，打开新的命令提示符窗口，运行：
```bash
node --version
npm --version
```

应该看到类似输出：
```
v18.x.x
9.x.x
```

### 3. FFmpeg 安装 (可选，但推荐)

#### 下载和安装
1. 访问 FFmpeg 官网：https://ffmpeg.org/download.html
2. 选择 Windows 版本下载
3. 解压到合适的目录（如 `C:\ffmpeg`）
4. 将 `C:\ffmpeg\bin` 添加到系统 PATH 环境变量

#### 验证安装
```bash
ffmpeg -version
```

### 4. Git 验证
确认 Git 已安装：
```bash
git --version
```

## 🔧 环境变量配置

### 检查 PATH 环境变量
确保以下路径在系统 PATH 中：
- Python 安装目录（如 `C:\Python311\`）
- Python Scripts 目录（如 `C:\Python311\Scripts\`）
- Node.js 安装目录（通常自动添加）
- FFmpeg bin 目录（如 `C:\ffmpeg\bin`）

### 手动添加 PATH（如果需要）
1. 右键"此电脑" → "属性"
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"系统变量"中找到"Path"，点击"编辑"
5. 点击"新建"，添加相应路径
6. 确定保存

## ✅ 安装完成检查

安装完所有环境后，请重新打开命令提示符，运行以下命令验证：

```bash
# 检查 Python
python --version
pip --version

# 检查 Node.js
node --version
npm --version

# 检查 Git
git --version

# 检查 FFmpeg（可选）
ffmpeg -version
```

## 🚀 继续部署

环境安装完成后，请返回项目目录继续部署：

```bash
cd "d:\AI project\MeetMemo"
```

然后可以继续执行以下步骤：
1. 配置环境变量文件
2. 安装后端 Python 依赖
3. 安装前端 Node.js 依赖
4. 启动各项服务

## 🆘 常见问题解决

### Python 相关问题
- **问题**: `python` 命令不识别
- **解决**: 确保安装时勾选了"Add Python to PATH"，或手动添加到环境变量

### Node.js 相关问题
- **问题**: `node` 或 `npm` 命令不识别
- **解决**: 重新安装 Node.js，确保安装完成后重启命令提示符

### 权限问题
- **问题**: 安装过程中提示权限不足
- **解决**: 以管理员身份运行安装程序

### 网络问题
- **问题**: 下载速度慢或失败
- **解决**: 
  - 使用国内镜像源
  - 配置代理（如果在企业网络环境）
  - 尝试不同时间段下载

## 📞 获取帮助

如果在环境安装过程中遇到问题，可以：
1. 查看官方文档
2. 搜索相关错误信息
3. 检查系统兼容性
4. 确认网络连接正常

安装完成后，请告知我继续进行项目部署的后续步骤。