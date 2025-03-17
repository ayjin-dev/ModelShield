# -*- coding: utf-8 -*-
# @Time    : 2023/4/2 20:43
# @Author  : Jin Au-yeung
# @File    : clean.py
# @Software: PyCharm
import os
import config
## 清空文件夹
def clean(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.removedirs(os.path.join(root, dir))
    print('clean done')

if __name__ == '__main__':
    print(config.ROOT_PATH)
    print(config.APK_PATH)
    print(config.DATA_PATH)
