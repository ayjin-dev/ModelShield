# -*- coding: utf-8 -*-
# @Time    : 2023/4/2 10:32
# @Author  : Jin Au-yeung
# @File    : run.py
# @Software: PyCharm

import config
from Analyzer import Analyzer
from Spider import Spider
import os
import multiprocessing
from multiprocessing import Pool
from functools import partial
import csv
from utils.GetAppCsv import ReadCsv
import pandas as pd
from core.api import Api


def process_apks(apk):
    # 创建一个 Spider 对象
    spider = Spider()


    # 爬取 APK 文件
    # app_info = spider.page_to_csv(apk)
    # 将数据保存到 CSV 文件中
    # with open('app_info_add.csv', mode='a', newline='', encoding='utf-8-sig') as f:
    #     writer = csv.writer(f)
    #     # 判断是否是第一行，如果是第一行则写入 header
    #     if f.tell() == 0:
    #         header = list(app_info.keys())
    #         writer.writerow(header)
    #     writer.writerow(list(app_info.values()))
    # return app_info
    # 如果需要进一步分析，请创建一个 Analyzer 对象

    app_info = spider.download(apk)
    if app_info is None:
        return None
    analyzer = Analyzer(app_info)
    # 在这里执行您的分析任务
    analyzer.run()

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

def main():
    csv_path = f'{config.DATA_PATH}/app_info.csv'

    # 假设您有一个包含所有应用信息的列表
    apps = ReadCsv(csv_path)
    print(f'可分析共计: {len(apps)}个APP')
    app_status = getAnalysis()
    print(f'已分析共计: {len(app_status)}个APP')

    unknow = 0
    no_ai = 0
    ai = 0
    for app in apps:
        # 取出当前字典的appId
        app_id = app['appId']
        # 在app_status字典中查找对应的值，若找不到则返回Unknown
        is_AI = app_status.get(app_id, 'Unknown')
        if is_AI == 'True':
            ai += 1
        elif is_AI == 'False':
            no_ai += 1
        else:
            unknow += 1
        # 将is_AI添加到当前字典的isAI键中
        app['isAI'] = is_AI
    print(f'未知共计: {unknow}个APP')
    print(f'noai共计: {no_ai}个APP')
    print(f'ai共计: {ai}个APP')
    df = pd.DataFrame(apps)
    # 将数据框保存为 csv 文件
    df.to_csv('apps.csv', index=False)
    # 将数据框保存为 excel 文件
    df.to_excel('apps.xlsx', index=False)
    # print(apps[0])
    # print(app_status)
    # print(app_status)




    #========================去重操作
    # 从 apps 中删除已经存在于应用状态字典中的应用
    # for app in list(apps):
    #     if app['appId'] in app_status:
    #         apps.remove(app)
    # print('还需分析共计: ',len(apps))
    #=========================


    # 确定要使用的进程数量
    # num_processes = multiprocessing.cpu_count() 16
    # 设置进程数量
    # num_processes = 16
    # # 使用 multiprocessing.Pool 实现多进程并行处理
    # with Pool(processes=num_processes) as pool:
    #     pool.map(process_apks, apps)


if __name__ == "__main__":
    main()

