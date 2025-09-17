#!/bin/bash
# 
# DouyinLiveRecorder 一键部署脚本
# 适用于 Ubuntu/Debian 系统
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "请不要使用root用户运行此脚本"
        exit 1
    fi
}

# 检查系统类型
check_system() {
    log_step "检查系统环境..."
    
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        log_info "系统: $OS $VER"
    else
        log_error "无法识别系统类型"
        exit 1
    fi
    
    # 检查是否为Ubuntu/Debian
    if [[ "$OS" != *"Ubuntu"* ]] && [[ "$OS" != *"Debian"* ]]; then
        log_warn "此脚本主要针对Ubuntu/Debian系统，其他系统可能需要手动调整"
        read -p "是否继续? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 安装系统依赖
install_system_deps() {
    log_step "安装系统依赖..."
    
    sudo apt update
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        git \
        curl \
        wget \
        htop \
        screen
    
    log_info "系统依赖安装完成"
}

# 检查Python版本
check_python() {
    log_step "检查Python版本..."
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    log_info "Python版本: $PYTHON_VERSION"
    
    if [[ "$PYTHON_VERSION" != "3.8" ]] && [[ "$PYTHON_VERSION" != "3.9" ]]; then
        log_error "Python版本不符合要求，需要3.8或3.9"
        log_info "尝试安装Python 3.9..."
        
        sudo apt install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install -y python3.9 python3.9-pip python3.9-venv
        
        # 创建软链接
        sudo ln -sf /usr/bin/python3.9 /usr/local/bin/python3
        sudo ln -sf /usr/bin/pip3.9 /usr/local/bin/pip3
        
        log_info "Python 3.9 安装完成"
    fi
}

# 安装项目
install_project() {
    log_step "安装项目..."
    
    PROJECT_DIR="$HOME/DouyinLiveRecorder"
    
    # 如果目录已存在，备份
    if [[ -d "$PROJECT_DIR" ]]; then
        log_warn "项目目录已存在，创建备份..."
        mv "$PROJECT_DIR" "${PROJECT_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    # 复制项目文件（假设当前目录就是项目目录）
    if [[ -f "main.py" ]] && [[ -f "requirements.txt" ]]; then
        log_info "从当前目录复制项目文件..."
        cp -r . "$PROJECT_DIR"
    else
        log_error "在当前目录未找到项目文件"
        exit 1
    fi
    
    cd "$PROJECT_DIR"
    
    # 安装Python依赖
    log_info "安装Python依赖..."
    pip3 install --user -r requirements.txt
    
    # 创建必要目录
    mkdir -p download logs
    
    log_info "项目安装完成: $PROJECT_DIR"
}

# 配置文件设置
setup_config() {
    log_step "配置文件设置..."
    
    # 检查配置文件
    if [[ ! -f "config.txt" ]]; then
        log_error "config.txt 不存在"
        exit 1
    fi
    
    if [[ ! -f "rooms.json" ]]; then
        log_error "rooms.json 不存在"
        exit 1
    fi
    
    log_info "配置文件检查完成"
    echo
    log_warn "请编辑以下配置文件:"
    echo "  - config.txt: 基础配置"
    echo "  - rooms.json: 主播房间列表"
    echo
}

# 创建systemd服务
create_systemd_service() {
    log_step "创建systemd服务..."
    
    SERVICE_FILE="/etc/systemd/system/douyin-recorder.service"
    PROJECT_DIR="$HOME/DouyinLiveRecorder"
    USER_NAME=$(whoami)
    
    # 创建服务文件
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=DouyinLiveRecorder - 抖音直播录制服务
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER_NAME
Group=$USER_NAME
WorkingDirectory=$PROJECT_DIR
Environment=PATH=/usr/bin:/usr/local/bin:$HOME/.local/bin
Environment=PYTHONPATH=$PROJECT_DIR
ExecStart=/usr/bin/python3 $PROJECT_DIR/server_deploy.py
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=douyin-recorder

# 安全设置
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
ReadWritePaths=$PROJECT_DIR/download
ReadWritePaths=$PROJECT_DIR/logs

[Install]
WantedBy=multi-user.target
EOF
    
    # 重载systemd并启用服务
    sudo systemctl daemon-reload
    sudo systemctl enable douyin-recorder
    
    log_info "systemd服务创建完成"
}

# 安装Docker（可选）
install_docker() {
    log_step "安装Docker（可选）..."
    
    read -p "是否安装Docker? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "安装Docker..."
        
        # 安装Docker
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $(whoami)
        
        # 安装docker-compose
        sudo apt install -y docker-compose
        
        log_info "Docker安装完成"
        log_warn "请重新登录以生效Docker组权限"
    fi
}

# 显示部署完成信息
show_completion() {
    log_step "部署完成!"
    echo
    echo "🎉 DouyinLiveRecorder 已成功部署到服务器!"
    echo
    echo "📁 项目目录: $HOME/DouyinLiveRecorder"
    echo "📋 配置文件: config.txt, rooms.json"
    echo "📂 录制目录: download/"
    echo "📋 日志目录: logs/"
    echo
    echo "🚀 启动方式:"
    echo "  方式1 - 直接启动:"
    echo "    cd $HOME/DouyinLiveRecorder"
    echo "    python3 server_deploy.py"
    echo
    echo "  方式2 - systemd服务:"
    echo "    sudo systemctl start douyin-recorder"
    echo "    sudo systemctl status douyin-recorder"
    echo
    echo "  方式3 - Screen会话:"
    echo "    screen -S douyin-recorder"
    echo "    cd $HOME/DouyinLiveRecorder && python3 server_deploy.py"
    echo
    echo "📊 管理命令:"
    echo "  查看服务状态: sudo systemctl status douyin-recorder"
    echo "  查看日志: sudo journalctl -u douyin-recorder -f"
    echo "  停止服务: sudo systemctl stop douyin-recorder"
    echo "  重启服务: sudo systemctl restart douyin-recorder"
    echo
    echo "📖 更多信息请查看: SERVER_DEPLOY.md"
    echo
    log_warn "记得编辑配置文件后再启动服务!"
}

# 主函数
main() {
    echo "🚀 DouyinLiveRecorder 服务器一键部署脚本"
    echo "=" * 50
    echo
    
    check_root
    check_system
    install_system_deps
    check_python
    install_project
    setup_config
    create_systemd_service
    install_docker
    show_completion
}

# 运行主函数
main "$@"