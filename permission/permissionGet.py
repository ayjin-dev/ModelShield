import json
import multiprocessing as mp
import os
import subprocess
import config
from filelock import FileLock
import pandas as pd

def get_permission(apk_path, json_file_path):
    # 构造命令行参数
    aapt_cmd = ['aapt', 'd', 'permissions', apk_path]

    # 调用aapt命令，并捕获输出结果
    output = subprocess.check_output(aapt_cmd, universal_newlines=True).splitlines()

    # 解析输出结果，获取权限列表
    package = output[0].split(': ')[1]
    permissions = []
    for line in output[1:]:
        permission = line.split(': ')[1]
        if permission not in permissions:
            permissions.append(permission)

    # 构造数据字典
    data_dict = {'package': package, 'permissions': permissions}
    print(data_dict)
    # 加锁写入JSON文件
    with FileLock(json_file_path + '.lock'):
        # 如果文件存在，则读取原有数据，并将新数据追加到数组中
        if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                json_data.append(data_dict)
        else:
            # 如果文件不存在或为空，则创建一个包含新数据的数组
            json_data = [data_dict]

        # 将更新后的数据重新写入JSON文件
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def main():
    dl_app_path = r'G:\apkdataset\apks\aiapps'
    non_dl_app_path = r'G:\apkdataset\apks\apps'
    # 读取配置
    cf = config.Config()
    # 读取所有APK路径
    apk_path_list = []
    for root, dirs, files in os.walk(non_dl_app_path):
        for file in files:
            if file.endswith('.apk'):
                apk_path_list.append(os.path.join(root, file))
    print(len(apk_path_list))

    # 读取dl app
    dl_apk_path_list = []
    for root, dirs, files in os.walk(dl_app_path):
        for file in files:
            if file.endswith('.apk'):
                dl_apk_path_list.append(os.path.join(root, file))

    # 删除dl apk
    for apk in dl_apk_path_list:
        # 匹配apk文件的文件名
        apk_name = os.path.basename(apk)
        for _ in apk_path_list:
            if apk_name in _:
                apk_path_list.remove(_)
    print(len(apk_path_list))
    # 构造进程池
    pool = mp.Pool(processes=16)
    JSON_FILE_PATH = 'non_dl_permissions.json'
    # 处理所有APK文件
    for apk_path in apk_path_list:
        pool.apply_async(get_permission, args=(apk_path, JSON_FILE_PATH))

    # 关闭进程池
    pool.close()
    pool.join()

# 读取文件
def read_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data

def analyze_permission(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        print(len(json_data))
        # 统计所有APK文件中出现的权限数量,去重后的
        total_permissions = set()
        for data in json_data:
            total_permissions.update(data['permissions'])

        print('Total number of permissions:', len(total_permissions))

        # 统计出现次数最多的权限
        permission_count = {}
        for data in json_data:
            for permission in data['permissions']:
                if permission not in permission_count:
                    permission_count[permission] = 1
                else:
                    permission_count[permission] += 1
        # 筛选出前十的权限
        sorted_permission_count = sorted(permission_count.items(), key=lambda x: x[1], reverse=True)
        sorted_permission_count = [(p[0], p[1], round(p[1] / len(json_data) * 100, 2)) for p in sorted_permission_count]
        # suspicious_permission_count = {}
        # 读取可疑权限
        # with open('suspicious_permissions.txt', 'r', encoding='utf-8') as f:
        #     suspicious_permissions = f.read().splitlines()
        #
        # # 统计可疑权限出现次数
        # for permission, count in sorted_permission_count:
        #     if permission in suspicious_permissions:
        #         suspicious_permission_count[permission] = (count, count / total_permissions_count * 100)
        # print(suspicious_permission_count)

        # return sorted_permission_count[:youwanna]
        return sorted_permission_count
if __name__ == '__main__':
    # main()
    aiappjson = 'dl_permissions.json'
    normalappjson = 'non_dl_permissions.json'
    aiapp_permission = analyze_permission(aiappjson)
    normalapp_permission = analyze_permission(normalappjson)
    print(len(aiapp_permission),len(normalapp_permission))
    p_dict_list = []
    for ap in aiapp_permission:
        permission = ap[0]
        for np in normalapp_permission:
            if permission == np[0] and ap[2] >= np[2] and ap[2]>1:
                p_dict = {
                    'permission': permission,
                    'dl_data': (ap[1],ap[2]),
                    'non_dl_data': (np[1],np[2]),
                }
                p_dict_list.append(p_dict)

    df = pd.DataFrame(p_dict_list)
    writer = pd.ExcelWriter('output.xlsx')
    df.to_excel(writer, index=False)
    writer.save()




