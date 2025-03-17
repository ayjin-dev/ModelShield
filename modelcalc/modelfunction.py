# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 14:23
# @Author  : Jin Au-yeung
# @File    : modelfunction.py
# @Software: PyCharm

# 读取csv文件
import pandas as pd

def read_csv(path):
    df = pd.read_csv(path, header=None)
    return df

path = r'D:\secComm\utils\apps.csv'
df = read_csv(path)
print()