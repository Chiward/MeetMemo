# Redis 安装指南

## Windows 环境下安装 Redis

### 方法1: 使用 Windows Subsystem for Linux (WSL)

1. 安装 WSL2
```bash
wsl --install
```

2. 在 WSL 中安装 Redis
```bash
sudo apt update
sudo apt install redis-server
```

3. 启动 Redis
```bash
sudo service redis-server start
```

4. 测试连接
```bash
redis-cli ping
```

### 方法2: 使用 Docker Desktop

1. 安装 Docker Desktop for Windows
2. 启动 Redis 容器
```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### 方法3: 使用 Memurai (Windows 原生)

1. 下载 Memurai: https://www.memurai.com/
2. 安装并启动服务
3. 默认端口: 6379

### 方法4: 使用 Redis for Windows (非官方)

1. 下载: https://github.com/tporadowski/redis/releases
2. 解压并运行 redis-server.exe

## 验证安装

连接测试:
```bash
redis-cli ping
```

应该返回: `PONG`

## 配置

默认配置文件位置:
- Linux: `/etc/redis/redis.conf`
- Windows: `redis.windows.conf`

重要配置项:
```
port 6379
bind 127.0.0.1
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## 开发环境启动

```bash
# 启动 Redis 服务器
redis-server

# 或指定配置文件
redis-server redis.conf
```

## 生产环境注意事项

1. 设置密码认证
2. 配置持久化
3. 设置内存限制
4. 配置日志
5. 设置防火墙规则