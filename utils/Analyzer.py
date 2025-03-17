# -*- coding: utf-8 -*-
# @Time    : 2023/4/1 19:52
# @Author  : Jin Au-yeung
# @File    : Analyzer.py
# @Software: PyCharm
import datetime
import os
import shutil
import config
import threading

# 分析，反编译apk 遍历寻找模型
class Analyzer(object):
    def __init__(self,app_info,*args, **kwargs):
        super(Analyzer, self).__init__(*args, **kwargs)
        self.app_info = app_info
        self.model_end = config.end_model_format
    def run(self):
        apk = self.app_info
        APP_STATUS_FILE_PATH = config.DATA_PATH + '/status/' + apk['category'] + '_apps_status.txt'
        try:
            apk['APK_DIR'] = self.apk_decompile(apk)
            if apk['APK_DIR'] == 'error':
                return
            # judge dl application
            apk['IS_DL_APP'] = self.get_model_path(apk)
            # 删除apk文件
            if apk['IS_DL_APP']:
                # print("find tflite model")
                shutil.copy(apk['apkpath'],config.ROOT_PATH+'/apks/')
                os.remove(apk['apkpath']) # delete apk
                shutil.rmtree(apk['APK_DIR']) # delete decomplie apk dir
            else:
                # 删除apk文件和apk解压目录
                # print('should delete dir')
                shutil.rmtree(apk['APK_DIR'])  # Delete apk dir
                os.remove(apk['apkpath'])  # Delete apk file
            with open(APP_STATUS_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(apk['appId'] + ',' + str(apk['IS_DL_APP']) + '\n')
            return
        except Exception as e:
            print(e)
            # 错误文件记录
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('error.txt', 'a', encoding='utf-8') as f:
                 f.write(f"{now}: {apk['title']}\n")
            return
    def apk_decompile(self,apk):
        apk_path = apk['apkpath']
        apktool_command = 'apktool -q d -s -f {path_apk} -o {path_save_file}'
        apk_dir =  apk_path.replace('.apk','')
        apktool_command = apktool_command.format(path_apk=apk_path, path_save_file=apk_dir)
        # print(apk['title'],apk['apkpure_url'],apk_path,apktool_command)
        try:
            os.system(apktool_command + '\n')
        except Exception as e:
            print(e,apktool_command)
        # subprocess.check_output(apktool_command+' \n',shell=True)
        if os.path.exists(apk_dir):
            return apk_dir
        else:
            return 'error'

    # ================= find tflite model =================
    def get_model_path(self,apk):
        apk_dir = apk['APK_DIR']
        MODEL_FILE_PATH = config.DATA_PATH + '/model/' +apk['category'] + '_apps_model.txt'
        CATEGORY_DIR = config.APK_PATH + '/' + apk['category']
        path_model = []

        if os.path.isdir(apk_dir):
            for root, dirs, files in os.walk(apk_dir, topdown=True):
                if 'assets' in root:
                    for file in files:
                        file_absolute_path = os.path.join(root, file)
                        # 遍历所有模型后缀
                        for model in self.model_end:
                            if file_absolute_path.endswith(model):
                                path_model.append(file_absolute_path)
                        # 当文件名中包含model字符串时也加入
                        if 'model' in file:
                            if file_absolute_path not in path_model:
                                path_model.append(file_absolute_path)
        else:
            return False
        if len(path_model) > 0:
            with open(MODEL_FILE_PATH, 'a', encoding='utf-8') as f:
                for path in path_model:
                    # 保存模型文件到
                    # path = r'G:\mobileSec\utils\apps\photo\动联青少儿\assets\automl\model.tflite'
                    model_name = path.split('\\')[-1]
                    save_path = os.path.join(CATEGORY_DIR, apk['appId'])
                    if not os.path.isdir(save_path):
                        os.mkdir(save_path)
                    model_path = save_path + '\\' + str(model_name)
                    shutil.copy(path,  save_path)
                    f.write(model_path + '\n')
            print('Find dl model: ', apk['title'],path_model)
            return True
        else:
            # print('Not find dl model')
            return False