# -*- coding: utf-8 -*-
# @Time    : 2023/4/2 9:55
# @Author  : Jin Au-yeung
# @File    : aiapp_process_apk_module.py
# @Software: PyCharm
import re
import subprocess
import time
import threading
import traceback
from r0capture.r0capture import ssl_log

def process_apk(emulator_port, frida_port, apk_file, file_lock):
    emulator_address = '127.0.0.1:' + emulator_port
    frida_address = '127.0.0.1:' + frida_port
    # 获取应用包名 errors='ignore'忽略编码问题
    package_name = subprocess.run(['aapt', 'dump', 'badging', apk_file], capture_output=True, text=True, check=True,
                                  errors='ignore').stdout
    package_name = re.search(r'package: name=\'(.*?)\'', package_name).group(1)
    app_info = {}
    app_info['package_name'] = package_name
    print(f"Processing {package_name} on emulator {emulator_address}")

    try:
        # 安装 APK
        subprocess.run(['adb', '-s', emulator_address, 'install', '-r', '-g', apk_file], check=True)
    except:
        # 安装失败，直接返回
        print("Install Error")
        return
    try:
        ssl_log(
            pcap=f'D:\\secComm\\pcap\\aiapps\\{package_name}.pcap',
            host=frida_address,
            process=package_name,
            isUsb=False,
            isSpawn=True,
            worktime=20,
            emulator_address=emulator_address,
            file_lock=file_lock,
            apk_file = apk_file
        )
        with open('checked_apps.txt', 'a') as f:
            f.write(f'{apk_file},{package_name},True\n')
    except Exception as e:
        print(f"Error processing APK {apk_file}: {e}")
        with open('checked_apps.txt', 'a') as f:
            f.write(f'{apk_file},{package_name},Error\n')
    finally:
        # 停止应用
        subprocess.run(['adb', '-s', emulator_address, 'shell', 'am', 'force-stop', package_name], check=True)
        # 卸载应用
        subprocess.run(['adb', '-s', emulator_address, 'uninstall', package_name], check=True)

