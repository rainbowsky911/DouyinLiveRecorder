#!/usr/bin/env python3
# coding=utf-8
"""
:author: Qoder Assistant
:brief: 服务器部署启动脚本
"""

import os
import sys
import signal
import subprocess
import time
from pathlib import Path

def check_python_version():
    """检查Python版本是否符合要求"""
    version = sys.version_info
    if not (version.major == 3 and version.minor in [8, 9]):
        print(f"❌ Python版本不符合要求！当前版本: {version.major}.{version.minor}")
        print("⚠️  项目要求Python 3.8或3.9版本")
        return False
    print(f"✅ Python版本检查通过: {version.major}.{version.minor}")
    return True

def check_dependencies():
    """检查项目依赖是否安装"""
    print("🔍 检查项目依赖...")
    
    dependencies = [
        'requests',
        'websocket-client', 
        'protobuf',
        'jsengine',
        'quickjs',
        'gmssl'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  缺少以下依赖: {', '.join(missing)}")
        print("📦 请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖检查通过")
    return True

def create_directories():
    """创建必要的目录"""
    print("📁 创建必要的目录结构...")
    
    dirs = ['download', 'logs']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ 目录: {dir_name}")

def check_config_files():
    """检查配置文件"""
    print("🔧 检查配置文件...")
    
    if not os.path.exists('config.txt'):
        print("❌ config.txt 不存在")
        return False
    
    if not os.path.exists('rooms.json'):
        print("❌ rooms.json 不存在")
        return False
    
    print("✅ 配置文件检查通过")
    return True

def setup_signal_handlers():
    """设置信号处理器，用于优雅关闭"""
    def signal_handler(signum, frame):
        print(f"\n🛑 接收到信号 {signum}，正在优雅关闭...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def start_recording():
    """启动录制程序"""
    print("🚀 启动抖音直播录制程序...")
    print("=" * 60)
    
    # 强制使用CLI模式
    os.environ['DISPLAY'] = ''  # 确保无GUI环境
    
    try:
        # 启动主程序
        subprocess.run([sys.executable, 'main.py', '--cli'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 程序运行失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 用户中断程序")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 DouyinLiveRecorder 服务器部署启动器")
    print("=" * 60)
    
    # 环境检查
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_config_files():
        sys.exit(1)
    
    # 准备工作
    create_directories()
    setup_signal_handlers()
    
    # 启动程序
    print("\n📡 准备启动录制服务...")
    print("💡 提示: 按 Ctrl+C 可以优雅关闭程序")
    print("📂 录制文件将保存在 ./download/ 目录下")
    print("📋 日志文件将保存在 ./logs/ 目录下")
    print("=" * 60)
    
    time.sleep(2)  # 给用户时间阅读提示
    
    if start_recording():
        print("✅ 程序正常退出")
    else:
        print("❌ 程序异常退出")
        sys.exit(1)

if __name__ == '__main__':
    main()