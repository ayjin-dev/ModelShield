# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 13:10
# @Author  : Jin Au-yeung
# @File    : sitechannel.py
# @Software: PyCharm
import config
from tools import read_json_file
# 导入模块
import statistics
# config = config.Config()
import config
from tools import read_json_file
import statistics

def get_stats(json_path):
    # 读取配置
    data = read_json_file(json_path)
    dict_list = data

    # 计算 cpu_usage 平均值和标准差
    cpu_usage_list = [int(float(d['cpu_usage'])) for d in dict_list]
    cpu_usage_mean = statistics.mean(cpu_usage_list)
    cpu_usage_stdev = statistics.stdev(cpu_usage_list)

    # 计算 Janky_frames_List 平均值和标准差
    janky_frames_list = []
    for d in dict_list:
        janky_frames = d.get('Janky_frames_List', [])
        if janky_frames and len(janky_frames) > 0:
            janky_frames_list.append(float(janky_frames[0][1]))
    janky_frames_mean = statistics.mean(janky_frames_list)
    janky_frames_stdev = statistics.stdev(janky_frames_list)

    # 计算 Caches_frames_List 平均值和标准差
    caches_frames_list = []
    for d in dict_list:
        if len(d['Caches_frames_List']) > 0:
            caches_frames_list.append(int(d['Caches_frames_List'][0]))
    caches_frames_mean = sum(caches_frames_list) / len(caches_frames_list) / 1024 / 1024 # 转换为MB
    caches_frames_stdev = statistics.stdev(caches_frames_list) / 1024 / 1024 # 转换为MB
    # 计算 Total_Memory_List 平均值和标准差
    total_memory_list = []
    for d in dict_list:
        if 'Total_Memory_List' in d and len(d['Total_Memory_List']) > 0:
            try:
                total_memory = int(d['Total_Memory_List'][0][:-2])
                total_memory_list.append(total_memory)
            except:
                continue
    total_memory_mean = sum(total_memory_list) / len(total_memory_list) / 1024 # 转换为MB
    total_memory_stdev = statistics.stdev(total_memory_list) / 1024 # 转换为MB

    # 输出统计结果
    print(f"数据量: {len(dict_list)}")
    print(f"cpu_usage mean: {cpu_usage_mean:.2f}, stdev: {cpu_usage_stdev:.2f}")
    print(f"janky_frames mean: {janky_frames_mean:.2f}, stdev: {janky_frames_stdev:.2f}")
    print(f"caches_frames mean: {caches_frames_mean:.2f}MB, stdev: {caches_frames_stdev:.2f}MB")
    print(f"total_memory mean: {total_memory_mean:.2f}MB, stdev: {total_memory_stdev:.2f}MB")
    # 返回统计结果
    return cpu_usage_mean, cpu_usage_stdev, janky_frames_mean, janky_frames_stdev, caches_frames_mean, caches_frames_stdev, total_memory_mean, total_memory_stdev


# 读取配置
ai_json_path = '/RunTimeAppStatus.json'
no_ai_json_path = '/merged.json'
ai_data = get_stats(ai_json_path)
no_ai_data = get_stats(no_ai_json_path)

"""
normal
cpu_usage mean: 33.77, stdev: 38.30
janky_frames mean: 38.29, stdev: 35.81
caches_frames mean: 5.29MB, stdev: 5.71MB
total_memory mean: 125.35MB, stdev: 53.08MB

aiapps
cpu_usage mean: 39.30, stdev: 53.12
janky_frames mean: 36.20, stdev: 33.62
caches_frames mean: 5.15MB, stdev: 5.54MB
total_memory mean: 137.12MB, stdev: 52.10MB


normal
cpu_usage mean: 33.77, stdev: 38.30
janky_frames mean: 38.29, stdev: 35.81
caches_frames mean: 5.29MB, stdev: 5.71MB
total_memory mean: 125.35MB, stdev: 53.08MB

aiapps
cpu_usage mean: 39.30, stdev: 53.12
janky_frames mean: 36.20, stdev: 33.62
caches_frames mean: 5.15MB, stdev: 5.54MB
total_memory mean: 137.12MB, stdev: 52.10MB
"""
