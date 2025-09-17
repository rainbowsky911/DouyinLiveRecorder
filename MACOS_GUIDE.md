# 🍎 macOS 兼容性指南

## 🚨 当前遇到的问题

您遇到的问题主要有两个：

1. **Python版本不兼容** - 使用了Python 3.12，项目要求3.8或3.9
2. **GUI功能错误** - `os.startfile`函数在macOS上不存在

## ✅ 已修复的问题

### 1. GUI文件管理器打开功能
- ✅ 修复了`dylr/gui/grip_frame.py`中的跨平台兼容性
- ✅ 现在支持macOS (`open`)、Linux (`xdg-open`)、Windows (`os.startfile`)
- ✅ 添加了错误处理机制

### 2. Python版本检查
- ✅ 在`main.py`中添加了版本兼容性检查
- ✅ 创建了专门的兼容性检查脚本`check_compatibility.py`
- ✅ 提供了详细的版本问题解决方案

## 🛠️ 解决方案

### 方案1: 使用兼容性检查脚本（推荐）
```bash
# 运行兼容性检查
python3 check_compatibility.py

# 根据提示选择创建虚拟环境
```

### 方案2: 手动安装Python 3.9
```bash
# 使用Homebrew安装Python 3.9
brew install python@3.9

# 使用Python 3.9运行项目
python3.9 main.py --cli
```

### 方案3: 使用conda环境
```bash
# 创建conda环境
conda create -n douyin-recorder python=3.9

# 激活环境
conda activate douyin-recorder

# 安装依赖
pip install -r requirements.txt

# 运行项目
python main.py --cli
```

### 方案4: 使用macOS专用启动脚本（最简单）
```bash
# 直接运行macOS启动脚本
./start_macos.sh

# 或强制CLI模式
./start_macos.sh --cli
```

## 📋 macOS专用功能

### 自动环境检测
- ✅ 自动寻找合适的Python版本
- ✅ 自动安装缺失的依赖
- ✅ 智能选择运行模式（CLI/GUI）

### 文件系统兼容性
- ✅ 使用`open`命令打开Finder
- ✅ 正确处理macOS路径格式
- ✅ 支持中文路径和文件名

## 🔧 常见问题解决

### Q: Python版本问题
```bash
# 检查当前Python版本
python3 --version

# 查看所有可用的Python版本
ls /usr/bin/python*
ls /opt/homebrew/bin/python*

# 使用特定版本运行
python3.9 main.py --cli
```

### Q: 依赖安装问题
```bash
# 更新pip
python3.9 -m pip install --upgrade pip

# 安装依赖
python3.9 -m pip install -r requirements.txt

# 如果protobuf版本有问题
python3.9 -m pip install 'protobuf>=3.20.0,<4.0.0'
```

### Q: GUI显示问题
```bash
# 强制使用CLI模式
python3.9 main.py --cli

# 或使用macOS启动脚本
./start_macos.sh --cli
```

### Q: 权限问题
```bash
# 给脚本执行权限
chmod +x start_macos.sh
chmod +x check_compatibility.py

# 检查目录权限
ls -la download/ logs/
```

## 🎯 推荐的macOS使用流程

### 1. 首次使用
```bash
# 1. 检查兼容性
python3 check_compatibility.py

# 2. 根据提示安装Python 3.9或创建虚拟环境

# 3. 使用macOS专用脚本启动
./start_macos.sh --cli
```

### 2. 日常使用
```bash
# 直接使用macOS启动脚本
./start_macos.sh

# 或者如果已配置好环境
python3.9 main.py --cli
```

### 3. 服务器部署（macOS服务器）
```bash
# 使用服务器部署脚本
./deploy.sh

# 或手动部署
./start_macos.sh --cli
```

## 📊 性能优化（macOS）

### 系统资源配置
```bash
# 查看系统资源
top -l 1 | grep -E "(CPU|PhysMem)"

# 监控Python进程
top -pid $(pgrep -f python3)
```

### 配置文件优化（config.txt）
```ini
# macOS优化配置
check_period = 30
check_threads = 1
check_wait = 0.5
debug = false
```

## 🔐 macOS安全注意事项

### 网络权限
```bash
# 确保Python有网络访问权限
# 系统偏好设置 → 安全性与隐私 → 隐私 → 网络传入连接
```

### 文件系统权限
```bash
# 确保有写入权限
sudo chown -R $(whoami) download/ logs/
chmod 755 download/ logs/
```

## 📝 macOS特有配置

### 环境变量设置
```bash
# 在~/.zshrc或~/.bash_profile中添加
export PYTHONPATH="/Users/$(whoami)/DouyinLiveRecorder"
export PATH="/opt/homebrew/bin:$PATH"  # 如果使用Homebrew
```

### LaunchAgent配置（可选）
创建`~/Library/LaunchAgents/com.douyin.recorder.plist`实现开机自启：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.douyin.recorder</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/DouyinLiveRecorder/start_macos.sh</string>
        <string>--cli</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/DouyinLiveRecorder</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

## 🎉 现在可以开始使用了！

运行以下命令开始使用：
```bash
./start_macos.sh --cli
```

您的macOS系统现在已经完全兼容DouyinLiveRecorder项目了！