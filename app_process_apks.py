# -*- coding: utf-8 -*-
# @Time    : 2023/4/15 21:06
# @Author  : Jin Au-yeung
# @File    : app_process_apks.py
# @Software: PyCharm
import multiprocessing
import os
import glob
from concurrent.futures import ProcessPoolExecutor, as_completed
from app_process_apk_module import process_apk
import config

# 指定存放 APK 文件的目录
apk_directory = config.ROOT_PATH + '/apks/apps/'

# 获取 APK 文件列表
apk_files = glob.glob(os.path.join(apk_directory, '*.apk'))
# 定义五个模拟器的地址
port_composes = [
    '62001:1111',
    '62025:2222',
    '62026:3333',
    '62027:4444',
]

def process_apk_with_emulator(port_compose, apk_file, file_lock):
    # print(f"Processing {apk_file} on emulator {port_compose}")
    emulator_port = port_compose.split(':')[0]
    frida_port = port_compose.split(':')[1]

    process_apk(emulator_port=emulator_port,frida_port=frida_port,apk_file=apk_file,file_lock=file_lock)

if __name__ == '__main__':
    print(apk_files[0])
    print(len(apk_files))
    # 使用 multiprocessing.Manager() 创建一个进程间共享的锁
    # manager = multiprocessing.Manager()
    # file_lock = manager.Lock()
    # with ProcessPoolExecutor(max_workers=len(port_composes)) as executor:
    #     tasks = []
    #
    #     for apk_file in apk_files:
    #         # 循环分配模拟器地址
    #         port_compose = port_composes.pop(0)
    #         port_composes.append(port_compose)
    #
    #         # 提交任务到进程池
    #         task = executor.submit(process_apk_with_emulator, port_compose, apk_file,file_lock)
    #         tasks.append(task)
    #
    #     # 等待所有任务完成
    #     for task in as_completed(tasks):
    #         try:
    #             task.result()
    #         except Exception as e:
    #             print(f"Error processing task: {e}")
