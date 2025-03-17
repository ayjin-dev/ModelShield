# -*- coding: utf-8 -*-
# @Time    : 2023/4/15 20:40
# @Author  : Jin Au-yeung
# @File    : normaldownload.py
# @Software: PyCharm
import glob
import multiprocessing

import config
from Spider import Spider
import os
from GetAppCsv import ReadCsv
import pandas as pd
from multiprocessing import Pool

def process_apks(apk):
    # 创建一个 Spider 对象
    spider = Spider()

    app_info = spider.download(apk)
    if app_info is None:
        return None
    with open('normal_apps.txt', 'a') as f:
        f.write(apk['download_url']+'\n')


def getAnalysis():
    category_list = ['APPLICATION', 'ANDROID_WEAR', 'ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY',
                     'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'EDUCATION',
                     'ENTERTAINMENT', 'EVENTS', 'FINANCE', 'FOOD_AND_DRINK', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME',
                     'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'MAPS_AND_NAVIGATION', 'MEDICAL', 'MUSIC_AND_AUDIO',
                     'NEWS_AND_MAGAZINES', 'PARENTING', 'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'SHOPPING',
                     'SOCIAL', 'SPORTS', 'TOOLS', 'TRAVEL_AND_LOCAL', 'VIDEO_PLAYERS', 'WATCH_FACE', 'WEATHER',
                     'FAMILY']
    print(f'共计: {len(category_list)} 个类别')
    status_path_list = [os.path.join(config.DATA_PATH, 'status', path + '_apps_status.txt') for path in category_list]
    # print(status_path_list)
    # 存储应用状态的字典

    # 逐个读取应用状态文件，将内容存入字典中
    app_status = {}
    for status_file in status_path_list:
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                # 读取文件内容并将其按逗号分隔
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split(',')
                    app_status[line[0]] = line[1]

    return app_status
import random
def main():
    csv_path = r'D:\secComm\utils\apps.csv'

    # 假设您有一个包含所有应用信息的列表
    apps = ReadCsv(csv_path)
    normal_apps = []
    ai_apps = []
    for app in apps:
        if app['isAI'] == 'False':
            normal_apps.append(app)
        elif app['isAI'] == 'True':
            ai_apps.append(app)

    print('Normal App Number: ',len(normal_apps))
    print('AI App Number: ',len(ai_apps))

    # 随机采样1100个数据
    sampled_normal_apps = random.sample(normal_apps, 2000)
    print(len(sampled_normal_apps))
    print(sampled_normal_apps[0])

    # 指定存放 APK 文件的目录
    apk_directory = config.ROOT_PATH + '/apks/apps/'
    # 获取 APK 文件列表
    apk_files = glob.glob(os.path.join(apk_directory, '*.apk'))
    print(apk_files[0]) # D:\secComm/apks/apps\0028032e0487c9ca10d49d1e7a906ac0d3a6ab5940a4937a795f0dd571311916.apk
    # 获得apk_files中的sha值
    apk_sha = [os.path.basename(apk_file).split('.')[0] for apk_file in apk_files]
    # 从随机样本中删除已经下载的apk
    for apk in sampled_normal_apps:
        if apk['sha256'] in apk_sha:
            sampled_normal_apps.remove(apk)
    print(len(sampled_normal_apps))

    #
    # 设置进程数量
    num_processes = 16
    # 使用 multiprocessing.Pool 实现多进程并行处理
    with Pool(processes=num_processes) as pool:
        pool.map(process_apks, sampled_normal_apps)


if __name__ == "__main__":
    main()

