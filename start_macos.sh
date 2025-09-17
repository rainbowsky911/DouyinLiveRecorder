#!/bin/bash
# 
# DouyinLiveRecorder macOS启动脚本
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🍎 DouyinLiveRecorder macOS启动脚本${NC}"
echo "=================================================="

# 检查Python版本
check_python() {
    echo -e "${BLUE}🔍 检查Python环境...${NC}"
    
    # 检查是否有合适的Python版本
    PYTHON_CMD=""
    
    for py_version in python3.9 python3.8 python3; do
        if command -v $py_version &> /dev/null; then
            PY_VERSION=$($py_version -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
            echo "找到 $py_version (版本: $PY_VERSION)"
            
            if [[ "$PY_VERSION" == "3.8" ]] || [[ "$PY_VERSION" == "3.9" ]]; then
                PYTHON_CMD=$py_version
                echo -e "${GREEN}✅ 使用Python版本: $PY_VERSION${NC}"
                break
            fi
        fi
    done
    
    if [[ -z "$PYTHON_CMD" ]]; then
        echo -e "${RED}❌ 未找到合适的Python版本（需要3.8或3.9）${NC}"
        echo -e "${YELLOW}💡 请安装Python 3.9:${NC}"
        echo "   brew install python@3.9"
        echo -e "${YELLOW}💡 或者运行兼容性检查脚本:${NC}"
        echo "   python3 check_compatibility.py"
        exit 1
    fi
}

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}📦 检查依赖...${NC}"
    
    if [[ ! -f "requirements.txt" ]]; then
        echo -e "${RED}❌ 未找到requirements.txt文件${NC}"
        exit 1
    fi
    
    # 检查是否需要安装依赖
    if ! $PYTHON_CMD -c "import requests, websocket, google.protobuf, jsengine, quickjs, gmssl" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  缺少必要依赖，正在安装...${NC}"
        $PYTHON_CMD -m pip install -r requirements.txt
        
        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ 依赖安装完成${NC}"
        else
            echo -e "${RED}❌ 依赖安装失败${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ 依赖检查通过${NC}"
    fi
}

# 检查配置文件
check_config() {
    echo -e "${BLUE}⚙️  检查配置文件...${NC}"
    
    if [[ ! -f "config.txt" ]]; then
        echo -e "${RED}❌ config.txt不存在${NC}"
        exit 1
    fi
    
    if [[ ! -f "rooms.json" ]]; then
        echo -e "${RED}❌ rooms.json不存在${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 配置文件检查通过${NC}"
}

# 创建必要目录
create_directories() {
    echo -e "${BLUE}📁 创建目录...${NC}"
    mkdir -p download logs
    echo -e "${GREEN}✅ 目录创建完成${NC}"
}

# 启动程序
start_program() {
    echo -e "${BLUE}🚀 启动程序...${NC}"
    echo "按 Ctrl+C 停止程序"
    echo "=================================================="
    
    # 根据参数选择启动模式
    if [[ "$1" == "--cli" ]]; then
        echo -e "${GREEN}📟 使用CLI模式启动${NC}"
        $PYTHON_CMD main.py --cli
    elif [[ "$1" == "--gui" ]]; then
        echo -e "${GREEN}🖥️  使用GUI模式启动${NC}"
        $PYTHON_CMD main.py
    else
        # 自动检测
        if [[ -n "$DISPLAY" ]] || [[ "$TERM_PROGRAM" == "vscode" ]] || [[ -n "$SSH_CLIENT" ]]; then
            echo -e "${GREEN}📟 检测到服务器环境，使用CLI模式${NC}"
            $PYTHON_CMD main.py --cli
        else
            echo -e "${GREEN}🖥️  使用GUI模式启动${NC}"
            $PYTHON_CMD main.py
        fi
    fi
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --cli     强制使用命令行模式"
    echo "  --gui     强制使用图形界面模式"
    echo "  --help    显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0              # 自动选择模式"
    echo "  $0 --cli        # 命令行模式"
    echo "  $0 --gui        # 图形界面模式"
}

# 主函数
main() {
    # 处理命令行参数
    case "$1" in
        --help|-h)
            show_help
            exit 0
            ;;
        --cli|--gui)
            # 继续执行
            ;;
        "")
            # 无参数，继续执行
            ;;
        *)
            echo -e "${RED}❌ 未知参数: $1${NC}"
            show_help
            exit 1
            ;;
    esac
    
    # 执行检查和启动流程
    check_python
    check_dependencies
    check_config
    create_directories
    start_program "$1"
}

# 运行主函数
main "$@"