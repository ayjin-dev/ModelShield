# -*- coding: utf-8 -*-
# @Time    : 2023/4/21 14:38
# @Author  : Jin Au-yeung
# @File    : compare_model.py
# @Software: PyCharm
import tensorflow as tf
import time
def parse_tflite_model_structure(model_path):
    try:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        ops = interpreter.get_tensor_details()

        return input_details, output_details, ops
    except Exception as e:
        print(f"Error parsing model {model_path}: {e}")
        return [], [], []

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def compare_tflite_models(model_path1, model_path2):
    input_details1, output_details1, ops1 = parse_tflite_model_structure(model_path1)
    input_details2, output_details2, ops2 = parse_tflite_model_structure(model_path2)
    input_set1 = set([tensor['name'] for tensor in input_details1])
    input_set2 = set([tensor['name'] for tensor in input_details2])

    output_set1 = set([tensor['name'] for tensor in output_details1])
    output_set2 = set([tensor['name'] for tensor in output_details2])

    ops_set1 = set([op['name'] for op in ops1])
    ops_set2 = set([op['name'] for op in ops2])

    input_similarity = jaccard_similarity(input_set1, input_set2)
    output_similarity = jaccard_similarity(output_set1, output_set2)
    ops_similarity = jaccard_similarity(ops_set1, ops_set2)

    return input_similarity, output_similarity, ops_similarity


def find_similar_tflite_models(model_files, similarity_threshold=0.8):
    similar_models = []
    for i in range(len(model_files)):
        for j in range(i+1, len(model_files)):
            model1 = model_files[i]
            model2 = model_files[j]
            input_similarity, output_similarity, ops_similarity = compare_tflite_models(model1, model2)
            average_similarity = (input_similarity + output_similarity + ops_similarity) / 3
            with open('average_similarity.txt', 'a', encoding='utf-8') as f:
                f.write(f"{model1},{model2},{average_similarity}\n")

    return similar_models

tflite_files = []
with open('model_path.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line:
            ## 找到后缀不为tflite的文件
            if '.tflite' in line:
                    tflite_files.append(line)
print(len(tflite_files))
print(tflite_files[0])
import shutil
import os
import shutil


src_root = 'D:/secComm/apps/'
dest_root = 'D:/secComm/models'

for file_path in tflite_files:
    # 获取模型文件相对于根目录的路径
    rel_path = os.path.relpath(file_path, src_root)

    # 构建目标文件夹路径和目标文件路径
    dest_dir = os.path.join(dest_root, os.path.dirname(rel_path))
    dest_path = os.path.join(dest_dir, os.path.basename(file_path))

    # 创建目标文件夹并复制文件
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(file_path, dest_path)

# # 设置相似度阈值，仅返回大于或等于该阈值的相似度的模型对
# similarity_threshold = 0.8
#
# similar_models = find_similar_tflite_models(tflite_files, similarity_threshold)
# print("相似的模型：")
# for model1, model2, similarity in similar_models:
#     print(f"{model1} 和 {model2} 的相似度为 {similarity}")


