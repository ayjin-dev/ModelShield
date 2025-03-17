# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 19:40
# @Author  : Jin Au-yeung
# @File    : Static.py
# @Software: PyCharm
import pandas as pd
import config

csv_path = f'{config.DATA_PATH}/app_info.csv'
# 读取app_info.csv文件
df = pd.read_csv(csv_path)

# 筛选出download_url不为空的记录
df = df[df['download_url'].notna()]

# 统计每个种类的数量
count_by_category = df.groupby('category')['title'].count()

# 将统计结果保存为csv文件
count_by_category.to_csv('count_by_category.csv')
