# -*- coding: utf-8 -*-
# @Time    : 2023/4/9 10:12
# @Author  : Jin Au-yeung
# @File    : cffidownload.py
# @Software: PyCharm
from curl_cffi import requests
import requests as r2
# 注意 impersonate 这个参数
from tqdm.auto import tqdm

proxies = {
    "https": "http://localhost:7890",
    "http": "http://localhost:7890",
}
# r = requests.get("https://d.apkpure.com/b/APK/com.spotify.music?version=latest", impersonate="chrome110",content_callback=True, proxies=proxies)
fname = 'test.apk'
with open("spotify.apk", "wb") as f:
    r = requests.get("https://d.apkpure.com/b/APK/com.spotify.music?version=latest", timeout=100,impersonate="chrome101", content_callback=f.write, proxies=proxies)

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

# output: {'ja3_hash': '53ff64ddf993ca882b70e1c82af5da49'
# 指纹和目标浏览器一致

# 支持使用代理
# proxies = {"https": "http://localhost:3128"}
# r = requests.get("https://tls.browserleaks.com/json", impersonate="chrome101", proxies=proxies)



