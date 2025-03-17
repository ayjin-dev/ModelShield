# -*- coding: utf-8 -*-
# @Time    : 2023/5/12 20:09
# @Author  : Jin Au-yeung
# @File    : tfliteFIndEntropy.py
# @Software: PyCharm

import os
import numpy as np
import tensorflow as tf
from modelcalc import parse_tflite_model_structure
from tqdm import tqdm
tflite_path = []
with open('entropy_model.txt','r',encoding='utf-8') as fp:
    for line in fp.readlines():
        if line.strip().split(',')[0].endswith('.tflite'):
            model = {}
            model['path'] = line.strip().split(',')[0]
            model['entropy'] = line.strip().split(',')[1]
            tflite_path.append(model)
with open('unentropy_model.txt','r',encoding='utf-8') as fp:
    for line in fp.readlines():
        if line.strip().split(',')[0].endswith('.tflite'):
            model = {}
            model['path'] = line.strip().split(',')[0]
            model['entropy'] = line.strip().split(',')[1]
            tflite_path.append(model)

print(tflite_path[0])
# tflite_path = tflite_path[:50]
encrypt_model = []
encrypt_score = []
unencrypt_model = []
unencrypt_score = []
for model in tqdm(tflite_path):
    try:
        tf.lite.Interpreter(model_path=model['path'])
        unencrypt_model.append(model)
        unencrypt_score.append(float(model['entropy']))
    except Exception as e:
        encrypt_model.append(model)
        encrypt_score.append(float(model['entropy']))
print('加密:',len(encrypt_model),encrypt_model[0])
print('未加密:',len(unencrypt_model),unencrypt_model[0])
print('加密最小值:',np.min(encrypt_score))
print('加密平均值:',np.mean(encrypt_score))
print('加密最大值:',np.max(encrypt_score))
print('未加密最小值:',np.min(unencrypt_score))
print('未加密平均值:',np.mean(unencrypt_score))
print('未加密最大值:',np.max(unencrypt_score))
