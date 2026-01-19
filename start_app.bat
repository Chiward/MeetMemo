@echo off
chcp 65001 >nul
setlocal

title MeetMemo Launcher

echo ===================================================
echo       MeetMemo AI 智能会议纪要 - 一键启动
echo ===================================================

REM 1. 环境检查
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+ 并确保添加到 PATH 环境变量。
    pause
    exit /b
)

where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js。
    pause
    exit /b
)

REM 2. 启动 Redis
echo.
echo [1/4] 正在启动 Redis 服务...
if exist "redis\redis-server.exe" (
    start "Redis Server" /min "redis\redis-server.exe" "redis\redis.windows.conf"
) else (
    echo [警告] 根目录下未找到 redis 目录，尝试使用系统全局 Redis...
    REM 如果系统未安装 Redis，后续 Celery 可能会报错
)

REM 等待 Redis 启动
timeout /t 2 /nobreak >nul

REM 3. 准备后端依赖并启动
echo.
echo [2/4] 检查后端依赖...
cd backend
if not exist "venv" (
    echo 正在安装/更新 Python 依赖...
    python -m pip install -r requirements.txt
)

echo 正在启动后端服务 (API & Celery)...
REM 启动 Celery Worker (在新窗口)
start "MeetMemo Celery Worker" cmd /k "python celery_worker.py"

REM 启动 API Server (在新窗口)
REM 使用 start_dev.py，但我们已禁用了它的自动安装依赖功能
start "MeetMemo API Server" cmd /k "python start_dev.py"
cd ..

REM 4. 准备前端依赖并启动
echo.
echo [3/4] 检查前端依赖...
cd frontend
if not exist "node_modules" (
    echo.
    echo [首次运行] 正在安装前端依赖...
    echo -------------------------------------------------------
    echo 正在自动切换 npm 为淘宝镜像源，以加快下载速度...
    call npm config set registry https://registry.npmmirror.com
    echo 正在下载依赖包，请耐心等待（约需 1-3 分钟）...
    echo 期间请勿关闭窗口！
    echo -------------------------------------------------------
    call npm install
    if %errorlevel% neq 0 (
        echo.
        echo [错误] 前端依赖安装失败！
        echo 请检查网络连接，或尝试手动在 frontend 目录下运行 npm install
        pause
        exit /b
    )
)

echo.
echo [4/4] 正在启动前端服务...
start "MeetMemo Frontend" cmd /k "npm start"

REM 5. 自动打开浏览器
echo.
echo 正在等待服务就绪，即将打开浏览器...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo ===================================================
echo ✅ 启动指令已发送完毕！
echo.
echo [重要提示]
echo 1. 您会看到多个黑色窗口（API Server, Worker, Frontend）。
echo 2. 这些窗口中出现 "Application startup complete" 或 "Compiled successfully" 后，
echo    即表示启动成功。此时窗口停止滚动是【正常现象】，请不要关闭它们。
echo 3. 浏览器已自动打开 http://localhost:3000。
echo.
echo 如需完全停止应用，请直接关闭所有黑色窗口。
echo ===================================================
pause