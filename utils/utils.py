# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 20:24
# @Author  : Jin Au-yeung
# @File    : utils.py
# @Software: PyCharm
import os
import glob
import csv

def find_apk_files(folder_path):
    # 使用glob查找文件夹下所有的apk文件
    return glob.glob(os.path.join(folder_path, '*.apk'))

def write_apk_paths_to_csv(apk_files, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # 写入CSV文件的表头
        csv_writer.writerow(['ApkPath', 'isCheck'])

        # 写入apk文件路径和isCheck字段
        for apk_file in apk_files:
            csv_writer.writerow([apk_file, False])

# folder_path = r'D:\secComm\apks'  # 替换为实际的文件夹路径
# csv_path = r'D:\secComm\data\apk_list.csv'  # 替换为你想要的CSV文件路径
# apk_files = find_apk_files(folder_path)
# write_apk_paths_to_csv(apk_files, csv_path)

# import json
#
# file_path = "../RunTimeAppStatus.json"
#
# with open(file_path, 'r', encoding='utf-8') as json_file:
#     json_data = json.load(json_file)
#
# for _ in json_data:
#     print(_['cpu_usage'])