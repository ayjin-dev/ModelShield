# -*- coding: utf-8 -*-
# @Time    : 2023/4/24 16:54
# @Author  : Jin Au-yeung
# @File    : findothermodel.py
# @Software: PyCharm
import os
import os

def get_file_size(file_path):
    """
    计算文件大小（以字节为单位）并返回字符串表示形式（包括单位）
    """
    # 获取文件大小（以字节为单位）
    file_size = os.path.getsize(file_path)

    # 将文件大小转换为其他单位（如 KB、MB、GB 等）
    KB = 1024
    MB = KB ** 2
    GB = KB ** 3

    if file_size < KB:
        return f'{file_size} 字节'
    elif file_size < MB:
        return f'{file_size/KB:.2f} KB'
    elif file_size < GB:
        return f'{file_size/MB:.2f} MB'
    else:
        return f'{file_size/GB:.2f} GB'
