# 🚀 DouyinLiveRecorder 服务器部署指南

## 📋 部署方案概览

本项目支持多种服务器部署方式，根据您的需求选择合适的方案：

1. **直接部署** - 在服务器上直接运行Python脚本
2. **Systemd服务** - 作为Linux系统服务运行（推荐）
3. **Docker部署** - 容器化部署（推荐）
4. **Screen/Tmux** - 会话管理工具运行

---

## 🔧 方案一：直接部署

### 环境要求
- ✅ Python 3.8 或 3.9
- ✅ 1核2G内存以上服务器
- ✅ 稳定的网络连接

### 部署步骤

#### 1. 环境准备
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip git

# CentOS/RHEL
sudo yum install python3 python3-pip git
```

#### 2. 项目部署
```bash
# 上传项目到服务器（或使用git clone）
cd /opt
sudo git clone <your-repo-url> DouyinLiveRecorder
cd DouyinLiveRecorder

# 安装依赖
pip3 install -r requirements.txt

# 配置文件
cp config.txt.example config.txt  # 如果有示例文件
vim config.txt  # 编辑配置

# 配置房间列表
vim rooms.json
```

#### 3. 启动程序
```bash
# 使用部署脚本启动（推荐）
python3 server_deploy.py

# 或直接启动
python3 main.py --cli
```

---

## 🔧 方案二：Systemd服务部署（推荐）

### 优势
- ✅ 开机自启动
- ✅ 自动重启机制
- ✅ 日志管理
- ✅ 系统级进程管理

### 部署步骤

#### 1. 准备服务文件
```bash
# 编辑服务文件
sudo vim /etc/systemd/system/douyin-recorder.service
```

将项目中的 `douyin-recorder.service` 内容复制，并修改以下路径：
- `your_username` → 你的用户名
- `/path/to/DouyinLiveRecorder` → 项目实际路径

#### 2. 启动服务
```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable douyin-recorder

# 启动服务
sudo systemctl start douyin-recorder

# 查看状态
sudo systemctl status douyin-recorder

# 查看日志
sudo journalctl -u douyin-recorder -f
```

#### 3. 服务管理命令
```bash
# 停止服务
sudo systemctl stop douyin-recorder

# 重启服务
sudo systemctl restart douyin-recorder

# 禁用自启
sudo systemctl disable douyin-recorder
```

---

## 🐳 方案三：Docker部署（推荐）

### 优势
- ✅ 环境隔离
- ✅ 版本一致性
- ✅ 易于迁移
- ✅ 资源限制

### 部署步骤

#### 1. 安装Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装docker-compose
sudo apt install docker-compose
```

#### 2. 构建和运行
```bash
# 构建镜像
docker build -t douyin-recorder .

# 使用docker-compose运行（推荐）
docker-compose up -d

# 或直接运行
docker run -d \
  --name douyin-recorder \
  --restart unless-stopped \
  -v $(pwd)/download:/app/download \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config.txt:/app/config.txt:ro \
  -v $(pwd)/rooms.json:/app/rooms.json \
  douyin-recorder
```

#### 3. 容器管理
```bash
# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f douyin-recorder

# 停止容器
docker-compose down

# 重启容器
docker-compose restart douyin-recorder
```

---

## 🖥️ 方案四：Screen/Tmux会话

### 适用场景
- 临时部署
- 开发测试
- 简单场景

### 使用Screen
```bash
# 安装screen
sudo apt install screen

# 创建会话
screen -S douyin-recorder

# 在会话中运行程序
cd /path/to/DouyinLiveRecorder
python3 server_deploy.py

# 分离会话：按 Ctrl+A 再按 D

# 重新连接会话
screen -r douyin-recorder

# 查看所有会话
screen -ls
```

### 使用Tmux
```bash
# 安装tmux
sudo apt install tmux

# 创建会话
tmux new-session -d -s douyin-recorder

# 在会话中运行
tmux send-keys -t douyin-recorder 'cd /path/to/DouyinLiveRecorder' Enter
tmux send-keys -t douyin-recorder 'python3 server_deploy.py' Enter

# 查看会话
tmux list-sessions

# 连接会话
tmux attach-session -t douyin-recorder
```

---

## 📊 监控和维护

### 1. 日志监控
```bash
# 实时查看日志
tail -f logs/$(ls logs/ | tail -1)

# 查看错误日志
grep -i error logs/*.log

# 日志轮转（防止日志文件过大）
sudo logrotate -f /etc/logrotate.conf
```

### 2. 资源监控
```bash
# 查看进程资源使用
ps aux | grep python3

# 查看系统资源
htop
free -h
df -h
```

### 3. 网络监控
```bash
# 查看网络连接
netstat -an | grep ESTABLISHED

# 监控网络流量
iftop
```

---

## 🔧 配置优化

### 服务器配置调优

#### 1. 针对低配服务器优化
```ini
# config.txt 优化配置
check_period = 30
check_threads = 1
check_wait = 1.0
important_check_period = 10
```

#### 2. 针对高配服务器优化
```ini
# config.txt 高性能配置
check_period = 15
check_threads = 2
check_wait = 0.3
important_check_period = 3
```

### 系统优化
```bash
# 增加文件描述符限制
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# 优化网络参数
echo "net.core.rmem_max = 134217728" >> /etc/sysctl.conf
echo "net.core.wmem_max = 134217728" >> /etc/sysctl.conf
sysctl -p
```

---

## 🛡️ 安全建议

### 1. 防火墙配置
```bash
# 只开放必要端口
sudo ufw enable
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow out 80,443
```

### 2. 用户权限
```bash
# 创建专用用户
sudo useradd -m -s /bin/bash douyin-recorder
sudo chown -R douyin-recorder:douyin-recorder /opt/DouyinLiveRecorder
```

### 3. 定期备份
```bash
# 备份配置和录制文件
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /backup/douyin-recorder-$DATE.tar.gz \
  /opt/DouyinLiveRecorder/config.txt \
  /opt/DouyinLiveRecorder/rooms.json \
  /opt/DouyinLiveRecorder/download/
```

---

## 🚨 故障排除

### 常见问题

#### 1. 程序无法启动
```bash
# 检查Python版本
python3 --version

# 检查依赖
pip3 list | grep -E "requests|websocket|protobuf"

# 检查日志
cat logs/latest.log
```

#### 2. 录制失败
```bash
# 检查网络连接
ping live.douyin.com

# 检查磁盘空间
df -h

# 检查权限
ls -la download/
```

#### 3. 内存不足
```bash
# 监控内存使用
free -h
top -p $(pgrep -f python3)

# 调整配置降低资源使用
# 减少 check_threads
# 增加 check_period
```

---

## 📱 远程管理

### 1. SSH管理
```bash
# 生成SSH密钥（本地）
ssh-keygen -t rsa -b 4096

# 复制公钥到服务器
ssh-copy-id user@server-ip

# 配置SSH别名
echo "Host douyin-server
    HostName your-server-ip
    User your-username
    Port 22" >> ~/.ssh/config
```

### 2. Web管理界面（可选）
可以考虑安装轻量级的Web管理工具：
- Portainer（Docker管理）
- Cockpit（系统管理）
- htop的Web版本

---

## 📈 性能调优

### 资源使用建议

| 服务器配置 | 同时录制数量 | 推荐配置 |
|------------|--------------|----------|
| 1核1G | 1-2个主播 | check_threads=1, check_period=60 |
| 1核2G | 3-5个主播 | check_threads=1, check_period=30 |
| 2核4G | 5-10个主播 | check_threads=2, check_period=15 |
| 4核8G | 10+个主播 | check_threads=3, check_period=10 |

---

## 🔗 相关资源

- [项目GitHub地址](https://github.com/your-repo)
- [Python官方文档](https://docs.python.org/3/)
- [Docker官方文档](https://docs.docker.com/)
- [Systemd服务管理](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

---

**注意事项**：
- 🚨 确保服务器有足够的磁盘空间存储录制文件
- 🚨 定期清理旧的录制文件和日志
- 🚨 监控服务器资源使用情况
- 🚨 遵守相关法律法规，仅用于个人学习研究