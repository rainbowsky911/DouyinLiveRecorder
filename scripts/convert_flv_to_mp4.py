#!/usr/bin/env python3
# coding=utf-8
"""
将超过24小时的flv文件转换为mp4格式
"""
import os
import time
import subprocess
from pathlib import Path


def convert_old_flv_to_mp4(download_dir="download", hours_threshold=24):
    """
    将超过指定小时数的flv文件转换为mp4格式
    
    Args:
        download_dir: 下载目录路径
        hours_threshold: 时间阈值（小时），默认24小时
    """
    download_path = Path(download_dir)
    if not download_path.exists():
        print(f"下载目录不存在: {download_path}")
        return
    
    current_time = time.time()
    threshold_seconds = hours_threshold * 3600  # 转换为秒
    
    converted_count = 0
    skipped_count = 0
    error_count = 0
    
    # 递归查找所有flv文件
    for flv_file in download_path.rglob("*.flv"):
        try:
            # 检查文件修改时间
            file_mtime = flv_file.stat().st_mtime
            time_diff = current_time - file_mtime
            
            if time_diff < threshold_seconds:
                print(f"跳过新文件 ({time_diff/3600:.1f}小时): {flv_file.name}")
                skipped_count += 1
                continue
            
            # 生成mp4文件路径
            mp4_file = flv_file.with_suffix('.mp4')
            
            # 检查mp4文件是否已存在
            if mp4_file.exists():
                print(f"已存在mp4文件，跳过: {mp4_file.name}")
                skipped_count += 1
                continue
            
            # 检查ffmpeg是否可用
            if not check_ffmpeg():
                print("错误: 未找到ffmpeg，请先安装ffmpeg")
                return
            
            print(f"开始转换 ({time_diff/3600:.1f}小时前): {flv_file.name}")
            
            # 执行转换
            cmd = [
                'ffmpeg', 
                '-i', str(flv_file),
                '-c', 'copy',  # 不重新编码，直接复制流
                str(mp4_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ 转换成功: {mp4_file.name}")
                converted_count += 1
            else:
                print(f"✗ 转换失败: {flv_file.name}")
                print(f"错误信息: {result.stderr}")
                error_count += 1
                
        except Exception as e:
            print(f"处理文件时出错 {flv_file}: {e}")
            error_count += 1
    
    # 输出统计信息
    print("\n" + "="*50)
    print(f"转换完成统计:")
    print(f"成功转换: {converted_count} 个文件")
    print(f"跳过文件: {skipped_count} 个文件")
    print(f"转换失败: {error_count} 个文件")
    print("="*50)


def check_ffmpeg():
    """检查ffmpeg是否可用"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    """主函数"""
    print("FLV转MP4转换工具")
    print("将超过24小时的flv文件转换为mp4格式")
    print("="*50)
    
    # 获取脚本所在目录的download文件夹
    script_dir = Path(__file__).parent
    download_dir = script_dir / "download"
    
    convert_old_flv_to_mp4(download_dir)


if __name__ == "__main__":
    main()