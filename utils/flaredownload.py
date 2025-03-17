# -*- coding: utf-8 -*-
# @Time    : 2023/4/4 19:06
# @Author  : Jin Au-yeung
# @File    : flaredownload.py
# @Software: PyCharm
import requests
from tqdm.auto import tqdm
import json

url = "http://localhost:8191/v1"

# https://d.apkpure.com/b/APK/com.infinitygames.shapes?version=latest
# https://d.apkpure.com/b/APK/com.whatsapp?cf=1&version=latest
payload = json.dumps({
    "cmd": "request.get",
    "url": "https://d.apkpure.com/b/APK/com.whatsapp?cf=1&version=latest",
    "maxTimeout": 60000
})

proxy = 'http://127.0.0.1:7890'
proxies = {
        "http": proxy,
        "https": proxy,
}
from fake_useragent import UserAgent
ua = UserAgent()
headers = {
    # 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'authority': 'd.apkpure.com',
    'Content-Type': 'application/json',
}

r = requests.post(url, headers=headers,data=payload,proxies=proxies)
print(r.content)
print(r.headers.get('User-Agent', 0))
print(r.headers.get('cf_clearence cookie', 0))
# f = open("test.apk", "wb")
# with tqdm.wrapattr(
#         f, "write",
#         # desc=f"{app['title']} ({fname.split('.')[0]})",
#         unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
#         total=int(r.headers.get('content-length', 0))
# ) as fout:
#     for chunk in r.iter_content(chunk_size=4096):
#         if not chunk:
#             break
#         fout.write(chunk)
# print(r.headers.get('content-length', 0))