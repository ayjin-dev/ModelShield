# Copyright 2017 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Decrypts and logs a process's SSL traffic.
Hooks the functions SSL_read() and SSL_write() in a given process and logs the
decrypted data to the console and/or to a pcap file.
  Typical usage example:
  ssl_log("wget", "log.pcap", True)
Dependencies:
  frida (https://www.frida.re/):
    sudo pip install frida
  hexdump (https://bitbucket.org/techtonik/hexdump/) if using verbose output:
    sudo pip install hexdump
"""

__author__ = "geffner@google.com (Jason Geffner)"
__version__ = "2.0"

import json
import re
import subprocess
import threading
import traceback

"""
# r0capture

ID: r0ysue 

安卓应用层抓包通杀脚本

https://github.com/r0ysue/r0capture

## 简介

- 仅限安卓平台，测试安卓7、8、9、10 可用 ；
- 无视所有证书校验或绑定，无视任何证书；
- 通杀TCP/IP四层模型中的应用层中的全部协议；
- 通杀协议包括：Http,WebSocket,Ftp,Xmpp,Imap,Smtp,Protobuf等等、以及它们的SSL版本；
- 通杀所有应用层框架，包括HttpUrlConnection、Okhttp1/3/4、Retrofit/Volley等等；
"""

# Windows版本需要安装库：
# pip install 'win_inet_pton'
# pip install hexdump
import argparse
import os
import pprint
import random
import signal
import socket
import struct
import sys
import time
from pathlib import Path

import frida
from loguru import logger

try:
    if os.name == 'nt':
        import win_inet_pton
except ImportError:
    # win_inet_pton import error
    pass

try:
    import myhexdump as hexdump # pylint: disable=g-import-not-at-top
except ImportError:
    pass
try:
    from shutil import get_terminal_size as get_terminal_size
except:
    try:
        from backports.shutil_get_terminal_size import get_terminal_size as get_terminal_size
    except:
        pass

try:
    import click
except:
    class click:
        @staticmethod
        def secho(message=None, **kwargs):
            print(message)

        @staticmethod
        def style(**kwargs):
            raise Exception("unsupported style")
banner = """
--------------------------------------------------------------------------------------------
           .oooo.                                      .                                  
          d8P'`Y8b                                   .o8                                  
oooo d8b 888    888  .ooooo.   .oooo.   oo.ooooo.  .o888oo oooo  oooo  oooo d8b  .ooooo.  
`888""8P 888    888 d88' `"Y8 `P  )88b   888' `88b   888   `888  `888  `888""8P d88' `88b 
 888     888    888 888        .oP"888   888   888   888    888   888   888     888ooo888 
 888     `88b  d88' 888   .o8 d8(  888   888   888   888 .  888   888   888     888    .o 
d888b     `Y8bd8P'  `Y8bod8P' `Y888""8o  888bod8P'   "888"  `V88V"V8P' d888b    `Y8bod8P' 
                                         888                                              
                                        o888o                                                                                                                                       
                    https://github.com/r0ysue/r0capture
--------------------------------------------------------------------------------------------\n
"""


def show_banner():
    colors = ['bright_red', 'bright_green', 'bright_blue', 'cyan', 'magenta']
    try:
        click.style('color test', fg='bright_red')
    except:
        colors = ['red', 'green', 'blue', 'cyan', 'magenta']
    try:
        columns = get_terminal_size().columns
        if columns >= len(banner.splitlines()[1]):
            for line in banner.splitlines():
                click.secho(line, fg=random.choice(colors))
    except:
        pass


# ssl_session[<SSL_SESSION id>] = (<bytes sent by client>,
#                                  <bytes sent by server>)
ssl_sessions = {}
def append_to_json_file(file_path, data, file_lock):
    with file_lock:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            # 如果文件存在且非空，则读取原有数据，并将新数据追加到数组中
            with open(file_path, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                json_data.append(data)
        else:
            # 如果文件不存在或为空，则创建一个包含新数据的数组
            json_data = [data]

        # 将更新后的数据重新写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def process_function(file_path, data, file_lock):
    append_to_json_file(file_path, data, file_lock)

def resource_monitor(emulator_address, appInfo, interval, duration, filelock):
    package_name = appInfo['package_name']
    gfxinfo_cmd = f"adb -s {emulator_address} shell dumpsys gfxinfo {package_name}"
    meminfo_cmd = f"adb -s {emulator_address} shell dumpsys meminfo {package_name}"

    end_time = time.time() + duration
    Janky_frames_List = []
    Caches_frames_List = []
    Total_Memory_List = []
    while time.time() < end_time:
        try:
            gpu_usage = subprocess.check_output(gfxinfo_cmd, shell=True).decode()
            Janky_frames = re.findall(r'Janky frames:\s+(\d+)\s+\(([\d.]+)%\)', gpu_usage)
            Caches = re.findall(r'Total memory usage:\s+(\d+) bytes', gpu_usage)
            if Janky_frames and Caches:
                Janky_frames_List.append(Janky_frames[0])
                Caches_frames_List.append(Caches[0])

            # 获取内存使用情况
            memory_usage = subprocess.check_output(meminfo_cmd, shell=True).decode()
            total_memory = re.findall(r"TOTAL:\s+(\d+)", memory_usage)
            if total_memory:
                Total_Memory_List.append(total_memory[0]+'KB')
            time.sleep(interval)
        except Exception as e:
            print("出现异常：",traceback.print_exc(),e)
    appInfo['Janky_frames_List'] = Janky_frames_List
    appInfo['Caches_frames_List'] = Caches_frames_List
    appInfo['Total_Memory_List'] = Total_Memory_List
    print(appInfo)
    process_function(file_path='RunTimeAppStatus_normal_new.json', data=appInfo, file_lock=filelock)
def ssl_log(process, pcap=None, host=False, verbose=False, isUsb=False, ssllib="", isSpawn=True, wait=0, worktime=0,emulator_address=None, file_lock=None,apk_file=None):
    def log_pcap(pcap_file, ssl_session_id, function, src_addr, src_port,
                 dst_addr, dst_port, data):
        t = time.time()

        if ssl_session_id not in ssl_sessions:
            ssl_sessions[ssl_session_id] = (random.randint(0, 0xFFFFFFFF),
                                            random.randint(0, 0xFFFFFFFF))
        client_sent, server_sent = ssl_sessions[ssl_session_id]

        if function == "SSL_read":
            seq, ack = (server_sent, client_sent)
        else:
            seq, ack = (client_sent, server_sent)

        for writes in (
                # PCAP record (packet) header
                ("=I", int(t)),  # Timestamp seconds
                ("=I", int((t * 1000000) % 1000000)),  # Timestamp microseconds
                ("=I", 40 + len(data)),  # Number of octets saved
                ("=i", 40 + len(data)),  # Actual length of packet
                # IPv4 header
                (">B", 0x45),  # Version and Header Length
                (">B", 0),  # Type of Service
                (">H", 40 + len(data)),  # Total Length
                (">H", 0),  # Identification
                (">H", 0x4000),  # Flags and Fragment Offset
                (">B", 0xFF),  # Time to Live
                (">B", 6),  # Protocol
                (">H", 0),  # Header Checksum
                (">I", src_addr),  # Source Address
                (">I", dst_addr),  # Destination Address
                # TCP header
                (">H", src_port),  # Source Port
                (">H", dst_port),  # Destination Port
                (">I", seq),  # Sequence Number
                (">I", ack),  # Acknowledgment Number
                (">H", 0x5018),  # Header Length and Flags
                (">H", 0xFFFF),  # Window Size
                (">H", 0),  # Checksum
                (">H", 0)):  # Urgent Pointer
            pcap_file.write(struct.pack(writes[0], writes[1]))
        pcap_file.write(data)

        if function == "SSL_read":
            server_sent += len(data)
        else:
            client_sent += len(data)
        ssl_sessions[ssl_session_id] = (client_sent, server_sent)

    def on_message(message, data):
        """Callback for errors and messages sent from Frida-injected JavaScript.
        Logs captured packet data received from JavaScript to the console and/or a
        pcap file. See https://www.frida.re/docs/messages/ for more detail on
        Frida's messages.
        Args:
          message: A dictionary containing the message "type" and other fields
              dependent on message type.
          data: The string of captured decrypted data.
        """
        if message["type"] == "error":
            logger.info(f"{message}")
            os.kill(os.getpid(), signal.SIGTERM)
            return
        if len(data) == 1:
            logger.info(f'{message["payload"]["function"]}')
            logger.info(f'{message["payload"]["stack"]}')
            return
        p = message["payload"]
        if verbose:
            src_addr = socket.inet_ntop(socket.AF_INET,
                                        struct.pack(">I", p["src_addr"]))
            dst_addr = socket.inet_ntop(socket.AF_INET,
                                        struct.pack(">I", p["dst_addr"]))
            session_id = p['ssl_session_id']
            logger.info(f"SSL Session: {session_id}")
            logger.info("[%s] %s:%d --> %s:%d" % (
                p["function"],
                src_addr,
                p["src_port"],
                dst_addr,
                p["dst_port"]))
            gen = hexdump.hexdump(data, result="generator",only_str=True)
            str_gen = ''.join(gen)
            logger.info(f"{str_gen}")
            logger.info(f"{p['stack']}")
        if pcap:
            log_pcap(pcap_file, p["ssl_session_id"], p["function"], p["src_addr"],
                     p["src_port"], p["dst_addr"], p["dst_port"], data)

    if isUsb:
        try:
            device = frida.get_usb_device()
        except:
            device = frida.get_remote_device()
    else:
        if host:
            manager = frida.get_device_manager()
            device = manager.add_remote_device(host)
        else:
            device = frida.get_local_device()

    if isSpawn:
        pid = device.spawn([process])
        start_time = time.time()
        time.sleep(1)
        session = device.attach(pid)
        time.sleep(1)
        device.resume(pid)

    else:
        print("attach")
        session = device.attach(process)
    if wait > 0:
        print(f"wait for {wait} seconds")
        time.sleep(wait)
    if pcap:
        pcap_file = open(pcap, "wb", 0)
        for writes in (
                ("=I", 0xa1b2c3d4),  # Magic number
                ("=H", 2),  # Major version number
                ("=H", 4),  # Minor version number
                ("=i", time.timezone),  # GMT to local correction
                ("=I", 0),  # Accuracy of timestamps
                ("=I", 65535),  # Max length of captured packets
                ("=I", 228)):  # Data link type (LINKTYPE_IPV4)
            pcap_file.write(struct.pack(writes[0], writes[1]))

    with open(Path(__file__).resolve().parent.joinpath("./script.js"), encoding="utf-8") as f:
        _FRIDA_SCRIPT = f.read()
    script = session.create_script(_FRIDA_SCRIPT)
    script.on("message", on_message)
    script.load()

    if ssllib != "":
        script.exports.setssllib(ssllib)
    def stoplog(signum, frame):
        session.detach()
        if pcap:
            pcap_file.flush()
            pcap_file.close()
        exit()
    signal.signal(signal.SIGINT, stoplog)
    signal.signal(signal.SIGTERM, stoplog)

    app_info = {}
    package_name = process
    app_info['package_name'] = package_name


    try:
        top_cmd = f"adb -s {emulator_address} shell top -n 1 -p $(pidof {package_name})"
        top_output = subprocess.check_output(top_cmd, shell=True).decode()
        top_info = top_output.split('\n')[-1].split(' ')
        top_info = [x for x in top_info if x]
        app_info['cpu_usage'] = top_info[-4]
    except Exception as e:
        app_info['cpu_usage'] = ' '
        print("出现异常：",traceback.print_exc(),e)
        return

    # 判断应用是否启动成功
    time.sleep(5)
    windows = subprocess.run(['adb', '-s', emulator_address, 'shell', 'dumpsys', 'window', 'windows'],
                             capture_output=True, text=True, check=True).stdout

    if f'Application Error: {package_name}' in windows:
        print(f'应用启动失败，应用包名：{package_name}')
        with open('checked_apps_normal.txt', 'a') as f:
            f.write(f'{apk_file},{package_name},False\n')
    else:
        # 开始资源监控线程
        monitor_thread = threading.Thread(target=resource_monitor, args=(emulator_address, app_info, 5, worktime, file_lock))
        monitor_thread.start()

        time.sleep(worktime)
        # 等待资源监控线程完成
        monitor_thread.join()
    # 停止应用
    subprocess.run(['adb', '-s', emulator_address, 'shell', 'am', 'force-stop', package_name], check=True)

    session.detach()
    if pcap:
        pcap_file.flush()
        pcap_file.close()
    exit()

    # sys.stdin.read()

#
# if __name__ == "__main__":
#     # show_banner()
#
#
#     class ArgParser(argparse.ArgumentParser):
#
#         def error(self, message):
#             print("ssl_logger v" + __version__)
#             print("by " + __author__)
#             print("Modified by BigFaceCat")
#             print("Error: " + message)
#             print()
#             print(self.format_help().replace("usage:", "Usage:"))
#             self.exit(0)
#
#
#     parser = ArgParser(
#         add_help=False,
#         description="Decrypts and logs a process's SSL traffic.",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog=r"""
# Examples:
#     %(prog)s -pcap ssl.pcap openssl
#     %(prog)s -verbose 31337
#     %(prog)s -pcap log.pcap -verbose wget
#     %(prog)s -pcap log.pcap -ssl "*libssl.so*" com.bigfacecat.testdemo
# """)
#     # 本机 python r0capture.py -U -f io.faceapp -t 10 -p D:\secComm\r0capture\pcap\test.pcap
#     # 远控 python r0capture.py -f io.faceapp -t 10 -p D:\secComm\r0capture\pcap\test.pcap -H 127.0.0.1:1234
#     args = parser.add_argument_group("Arguments")
#     args.add_argument("-pcap", '-p', metavar="<path>", required=False,
#                       help="Name of PCAP file to write")
#     args.add_argument("-host", '-H', metavar="<192.168.1.1:27042>", required=False,
#                       help="connect to remote frida-server on HOST")
#     args.add_argument("-verbose", "-v", required=False, action="store_const", default=True,
#                       const=True, help="Show verbose output")
#     args.add_argument("process", metavar="<process name | process id>",
#                       help="Process whose SSL calls to log")
#     args.add_argument("-ssl", default="", metavar="<lib>",
#                       help="SSL library to hook")
#     args.add_argument("--isUsb", "-U", default=False, action="store_true",
#                       help="connect to USB device")
#     args.add_argument("--isSpawn", "-f", default=False, action="store_true",
#                       help="if spawned app")
#     args.add_argument("-wait", "-w", type=int, metavar="<seconds>", default=0,
#                       help="Time to wait for the process")
#     args.add_argument("-time", '-t', metavar="work time", required=False,
#                       help="Setting the work time",type=int)
#     parsed = parser.parse_args()
#     # logger.add(f"{parsed.process.replace('.','_')}-{int(time.time())}.log", rotation="500MB", encoding="utf-8", enqueue=True, retention="10 days")
#     print(parsed)
#     ssl_log(
#         int(parsed.process) if parsed.process.isdigit() else parsed.process,
#         parsed.pcap,
#         parsed.host,
#         parsed.verbose,
#         isUsb=parsed.isUsb,
#         isSpawn=parsed.isSpawn,
#         ssllib=parsed.ssl,
#         wait=parsed.wait,
#         worktime=parsed.time
#     )
