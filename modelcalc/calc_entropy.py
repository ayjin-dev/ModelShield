import math
import os
from config import Config
from concurrent.futures import wait, ThreadPoolExecutor
from collections import Counter
import threading

# 创建锁对象
lock = threading.Lock()

# 分析框架使用情况
def framework_aiapps_use():
    root = os.getcwd()
    config = Config()
    for item in config.dic_dl_framework_keywords.items():
        print(item[0],item[1])
    model_end_list = config.dic_dl_framework_list
    print('检测模型关键词: ',model_end_list)
    model_path_list = []
    # 读取所有模型路径
    for category in config.CATEGORY_LIST:
        MODEL_FILE_PATH = config.DATA_PATH + '\model\\'+ category + '_apps_model.txt'
        print(MODEL_FILE_PATH)
        with open(MODEL_FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                model_path_list.append(line.strip())
    print(len(model_path_list))
    # 模型去重
    model_path_list = list(set(model_path_list))
    print(len(model_path_list))
    print(model_path_list[0])
    real_model = []
    entropy_list = []
    for model in model_path_list:
        for keyword in model_end_list:
            if keyword in model:
                real_model.append(model)
                break
    for i in range(0,len(real_model)):
        try:
            real_model[i] = os.path.join(root,'apps',real_model[i].split('apps\\')[-1])
            # 判断模型是否存在
            if not os.path.exists(real_model[i]):
                # 从列表中删除
                real_model.remove(real_model[i])
            # print(real_model[i])
            # entropy_list.append(get_entropy(real_model[i]))
        except Exception as e:
            print(e)
    print('共计', len(real_model), '个模型')

    # 记录出现最多次的模型名称
    model_name_list = []
    for model in real_model:
        model_name = model.split('\\')[-1]
        model_name_list.append(model_name)
    print(len(model_name_list))
    repeat = config.find_duplicates(model_name_list)
    print(repeat)
    c = Counter(repeat).most_common()  # 返回一个列表，按照dict的value从大到小排序
    for i in range(0,40):
        print(c[i])


    # 统计每个框架使用情况
    dic = {}
    model_end_list = [
            '.lite', '.prototxt', '.zip', '.model', '.feathermodel',
            '.params', '.pbtxt', '.bin', '.tflite', '.tnnproto',
            '.caffemodel', '.pt', '.tnnmodel', '.ptl', '.nb', '.pb'
        ]
    for keyword in model_end_list:
        dic[keyword] = 0
    print(dic)
    for item in dic.items():
        for path in real_model:
            if item[0] in path:
                dic[item[0]] += 1
    sum = 0
    for item in dic.items():
        sum+=item[1]
    print(dic,sum)

    return real_model
def get_entropy(path_file):
    with open(path_file, "rb") as file:
        counters = {byte: 0 for byte in range(2 ** 8)}
        for byte in file.read():
            counters[byte] += 1
        filesize = file.tell()
        probabilities = [counter / filesize for counter in counters.values()]
        entropy = -sum(probability * math.log2(probability) for probability in probabilities if probability > 0)
    with lock:
        if entropy > 7.99:
            # 加密文件
            with open('entropy_model.txt', 'a', encoding='utf-8') as fp:
                fp.write(path_file + ',' + str(entropy) + '\n')
        else:
            # 未加密
            with open('unentropy_model.txt', 'a', encoding='utf-8') as fp:
                fp.write(path_file + ',' + str(entropy) + '\n')
    print(entropy)
    return entropy
def get_all():
    task = []
    realmodel = framework_aiapps_use()
    print(len(realmodel))
    with ThreadPoolExecutor(max_workers=64) as t:
        for i in realmodel:
            task.append(t.submit(get_entropy, i))
        wait(task)
        print("finish")
