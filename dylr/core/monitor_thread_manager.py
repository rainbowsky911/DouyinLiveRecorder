# coding=utf-8
"""
:author: Lyzen
:date: 2023.02.07
:brief: 检测线程池
"""

from concurrent.futures import ThreadPoolExecutor
import atexit

# 检测线程池
# 由于检测是高频低消耗的，因此使用线程池
# 录制线程低频高消耗且必须保证不等待、长时间稳定运行，不使用线程池
check_thread_pool = ThreadPoolExecutor(max_workers=16)

# 注册关闭处理函数
def shutdown_pool():
    check_thread_pool.shutdown(wait=False)

atexit.register(shutdown_pool)


def new_check_task(fn):
    try:
        return check_thread_pool.submit(fn)
    except RuntimeError:
        # 解释器关闭时忽略任务提交
        return None
