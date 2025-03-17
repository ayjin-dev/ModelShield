# -*- coding: utf-8 -*-
# @Time    : 2023/4/1 18:01
# @Author  : Jin Au-yeung
# @File    : config.py
# @Software: PyCharm
import os

# Path
# ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = r'D:\ISSRE'
DATA_PATH = os.path.join(ROOT_PATH, 'data')
APK_PATH = os.path.join(ROOT_PATH, 'apps')

# model file identify
end_model_format = ['.tflite', '.lite', '.pt', '.ptl', '.param', '.mlmodel', '.model', '.caffemodel',
                                 '.feathermodel', '.chainermodel', 'PaddlePredictor.jar', 'libpaddle_lite_jni.so',
                                 '.nnet', 'libtvm_rumtime.so', '.moa', 'model.prof',
                                 '.mallet', '.classifier', '.inferencer', '.cntk']

class Config:
    def __init__(self):
        self.ROOT_DIR = os.getcwd()
        self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
        self.DATA_PATH = os.path.join(ROOT_PATH, 'data')
        self.APK_PATH = os.path.join(ROOT_PATH, 'apks')
        self.APP_PATH = os.path.join(ROOT_PATH, 'apps')
        self.CATEGORY_LIST = ['APPLICATION', 'ANDROID_WEAR', 'ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY',
                     'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'EDUCATION',
                     'ENTERTAINMENT', 'EVENTS', 'FINANCE', 'FOOD_AND_DRINK', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME',
                     'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'MAPS_AND_NAVIGATION', 'MEDICAL', 'MUSIC_AND_AUDIO',
                     'NEWS_AND_MAGAZINES', 'PARENTING', 'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'SHOPPING',
                     'SOCIAL', 'SPORTS', 'TOOLS', 'TRAVEL_AND_LOCAL', 'VIDEO_PLAYERS', 'WATCH_FACE', 'WEATHER',
                     'FAMILY']
        self.dic_dl_framework_keywords_ = {
            'Pytorch': ['.pt', '.ptl'],
            'TfLite': ['.tflite', '.lite'],
            'TensorFlow': ['.pb','.pbtxt'],
            'Caffe': ['.pb','.caffemodel','.prototxt'],
            'Mace': ['.pb'], # .yml delete
            'NCNN': ['.params','.bin'], # QQ，Qzone，微信，天天 P 图
            'TNN': ['.tnnmodel', '.tnnproto'],
            'PaddleLite': ['.nb'],
            'MxNet': ['.params'],
            'DeepLearning4j': ['.zip'],
            'FeatherCNN': ['.feathermodel'],
            'CNNDroid': ['.model'],
        }
        self.dic_dl_framework_keywords = {
            'Pytorch': ['.pt', '.ptl'], # 8 2 10
            'TfLite': ['.tflite', '.lite'], # 666 37 703
            'TensorFlow': ['.pb', '.pbtxt'], # 362 2 364
            'Caffe': ['.caffemodel', '.prototxt'], # 66 63 129
            # 'Mace': ['.pb'],  # .yml delete # 362
            'NCNN': ['.bin'],  #1453
            'TNN': ['.tnnmodel', '.tnnproto'], # 930 925 1855
            'PaddleLite': ['.nb'], # 63
            'MxNet': ['.params'], # 52
            'DeepLearning4j': ['.zip'], # 116
            'FeatherCNN': ['.feathermodel'], # 0
            'CNNDroid': ['.model'], # 2661
            # 重复的 .pb(Tensorflow\Caffe\Mace)->TensorFlow .params(NCNN\MxNet)->MxNet
        }
        # self.dic_dl_framework_list = [
        #     '.lite', '.prototxt', '.zip', '.model', '.feathermodel',
        #     '.params', '.pbtxt', '.bin', '.tflite', '.tnnproto',
        #     '.caffemodel', '.pt', '.tnnmodel', '.ptl', '.nb', '.pb'
        # ]
        self.dic_dl_framework_list = [
            '.lite', '.prototxt' , '.model', 'model' , '.feathermodel',
            '.params', '.pbtxt', '.tflite', '.tnnproto',
            '.caffemodel', '.pt', '.tnnmodel', '.ptl', '.nb', '.pb'
        ]
    # MKDIR FOR EVERY CATEGORY
    def create_dir(self):
        for item in self.CATEGORY_DICT.items():
            path = os.path.join(self.ROOT_DIR, 'apps', item[1])
            if not os.path.exists(path):
                os.mkdir(path)

    # 列表查重，返回每个元素出现的次数
    def find_duplicates(self,list):
        d = {}
        for i in list:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
        return d
    # READ CATEGORY STATUS FILES
    def read_category_status(self):
        data_dict = {}
        all_number = 0
        all_data = []
        dlapp_num = 0
        for item in self.CATEGORY_DICT.items():
            print(item)
            APP_STATUS_FILE_PATH = item[1] + '_apps_status.txt'
            dlapp = []
            no_dlapp = []
            category_data = []
            if os.path.exists(APP_STATUS_FILE_PATH):
                with open(APP_STATUS_FILE_PATH,'r',encoding='utf-8') as fp:
                    lines = fp.readlines()
                    for line in lines:
                        line = line.strip().split(',')
                        all_data.append(line[0])
                        if line[1] == 'True':
                            dlapp_num += 1
                            dlapp.append(line[0])
                        else:
                            no_dlapp.append(line[0])
                    # print(dlapp)
                    # print(no_dlapp)
                    category_data = dlapp + no_dlapp
                    category_data = list(set(category_data))
                    all_number += len(dlapp)+len(no_dlapp)
                    print('dlapp number is ',len(dlapp))
                    print('no_dlapp number is ',len(no_dlapp))
                    print('all apps numbers is ',len(category_data))
                    print('\n')
                    # data_dict[item[0]]['dlapp'] = dlapp
                    # data_dict[item[0]]['no_dlapp'] = no_dlapp
                    # print(item[0],'all apps numbers is ',len(dlapp)+len(no_dlapp))
                    # print(item[0],'dlapp number is ',len(dlapp))
                    # print(item[0],'no_dlapp number is ',len(no_dlapp))
        print(all_number)
        print(dlapp_num)
        print(len(all_data))
        print(len(list(set(all_data))))
