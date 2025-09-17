#!/usr/bin/env python3
# coding=utf-8
"""
:author: Qoder Assistant
:brief: Python版本兼容性检查和修复脚本
"""

import sys
import os
import subprocess
import platform

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3:
        print("❌ 错误：需要Python 3.x版本")
        return False
    
    if version.minor not in [8, 9]:
        print(f"⚠️  警告：当前Python版本{version.major}.{version.minor}可能不兼容")
        print("💡 项目推荐使用Python 3.8或3.9版本")
        
        if version.minor >= 10:
            print("🔧 检测到Python 3.10+版本，可能存在以下兼容性问题：")
            print("   - protobuf版本限制")
            print("   - 某些依赖库可能不支持")
            print("   - 建议降级到Python 3.9")
            return False
    else:
        print("✅ Python版本检查通过")
        return True

def get_python_installations():
    """获取系统中可用的Python安装"""
    python_versions = []
    
    # macOS下常见的Python路径
    possible_paths = [
        '/usr/bin/python3.8',
        '/usr/bin/python3.9',
        '/usr/local/bin/python3.8',
        '/usr/local/bin/python3.9',
        '/opt/homebrew/bin/python3.8',
        '/opt/homebrew/bin/python3.9',
    ]
    
    # 检查系统中已安装的Python版本
    for i in range(6, 12):  # Python 3.6 到 3.11
        try:
            result = subprocess.run([f'python3.{i}', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_str = result.stdout.strip()
                python_versions.append((f'python3.{i}', version_str))
        except:
            pass
    
    # 检查特定路径
    for path in possible_paths:
        if os.path.exists(path):
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    version_str = result.stdout.strip()
                    python_versions.append((path, version_str))
            except:
                pass
    
    return python_versions

def install_python_mac():
    """在macOS上安装Python 3.9"""
    print("🍎 检测到macOS系统")
    
    # 检查是否有brew
    try:
        subprocess.run(['brew', '--version'], capture_output=True, check=True)
        has_brew = True
    except:
        has_brew = False
    
    if has_brew:
        print("📦 使用Homebrew安装Python 3.9...")
        try:
            subprocess.run(['brew', 'install', 'python@3.9'], check=True)
            print("✅ Python 3.9安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ Homebrew安装失败")
    else:
        print("❌ 未找到Homebrew")
        print("💡 请手动安装Python 3.9:")
        print("   1. 访问 https://www.python.org/downloads/")
        print("   2. 下载Python 3.9.x版本")
        print("   3. 按照安装向导完成安装")
    
    return False

def create_venv_with_correct_python():
    """使用正确的Python版本创建虚拟环境"""
    python_versions = get_python_installations()
    
    # 寻找合适的Python版本
    suitable_python = None
    for python_cmd, version_str in python_versions:
        if 'Python 3.8' in version_str or 'Python 3.9' in version_str:
            suitable_python = python_cmd
            print(f"✅ 找到合适的Python版本: {python_cmd} ({version_str})")
            break
    
    if not suitable_python:
        print("❌ 未找到Python 3.8或3.9版本")
        
        if platform.system() == 'Darwin':  # macOS
            install_python_mac()
        else:
            print("💡 请安装Python 3.8或3.9版本")
        
        return False
    
    # 创建虚拟环境
    venv_path = 'venv_py39'
    print(f"🔧 使用{suitable_python}创建虚拟环境...")
    
    try:
        subprocess.run([suitable_python, '-m', 'venv', venv_path], check=True)
        print(f"✅ 虚拟环境已创建: {venv_path}")
        
        # 提供激活指令
        if platform.system() == 'Windows':
            activate_cmd = f"{venv_path}\\Scripts\\activate"
        else:
            activate_cmd = f"source {venv_path}/bin/activate"
        
        print(f"💡 激活虚拟环境: {activate_cmd}")
        print(f"💡 然后运行: pip install -r requirements.txt")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建虚拟环境失败: {e}")
        return False

def fix_compatibility_issues():
    """修复兼容性问题"""
    print("🔧 修复已知的兼容性问题...")
    
    # 检查并修复protobuf版本问题
    try:
        import google.protobuf
        print(f"protobuf版本: {google.protobuf.__version__}")
        
        # 检查版本是否在支持范围内
        version_parts = google.protobuf.__version__.split('.')
        major_version = int(version_parts[0])
        
        if major_version >= 4:
            print("⚠️  检测到protobuf 4.x版本，可能需要降级")
            print("💡 建议运行: pip install 'protobuf>=3.20.0,<4.0.0'")
    except ImportError:
        print("❌ protobuf未安装")
    
    # 其他兼容性检查...
    print("✅ 兼容性检查完成")

def main():
    """主函数"""
    print("🔍 DouyinLiveRecorder Python版本兼容性检查")
    print("=" * 50)
    
    # 检查当前Python版本
    if check_python_version():
        print("\n🎉 当前Python版本兼容，可以直接运行项目")
        fix_compatibility_issues()
    else:
        print("\n⚠️  需要使用兼容的Python版本")
        
        # 尝试创建虚拟环境
        print("\n🔧 解决方案：")
        print("方案1: 创建Python 3.9虚拟环境")
        
        response = input("是否创建虚拟环境? (y/N): ").lower()
        if response in ['y', 'yes']:
            create_venv_with_correct_python()
        else:
            print("\n💡 手动解决方案：")
            print("1. 安装Python 3.8或3.9")
            print("2. 使用pyenv管理Python版本")
            print("3. 使用conda创建环境:")
            print("   conda create -n douyin-recorder python=3.9")
            print("   conda activate douyin-recorder")
    
    print("\n📚 更多信息请查看项目文档")

if __name__ == '__main__':
    main()