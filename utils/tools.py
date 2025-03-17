# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 13:09
# @Author  : Jin Au-yeung
# @File    : tools.py
# @Software: PyCharm

import json
# 读取json文件返回字典
def read_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data
