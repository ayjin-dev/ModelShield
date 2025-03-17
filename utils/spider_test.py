# -*- coding: utf-8 -*-
# @Time    : 2023/4/2 21:22
# @Author  : Jin Au-yeung
# @File    : spider_test.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2023/4/1 18:08
# @Author  : Jin Au-yeung
# @File    : Spider.py
# @Software: PyCharm
import datetime
import traceback
# 美国3 gia
from GetAppCsv import ReadCsv
import requests
import cloudscraper
from bs4 import BeautifulSoup
import re
from humanfriendly import format_size
import pathlib
import os
from tqdm.auto import tqdm
import config
from fake_useragent import UserAgent
ua = UserAgent()


BASE_URL = 'https://apkpure.com'
API_URL = 'https://apkpure.com/api/www/cmd-down'
DOWNLOADER_URL = 'https://apkpure.com/apk-downloader'


class Spider(object):
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'authority': 'apkpure.com'
        }
        # 可以改为国外代理US
        self.proxy = 'http://127.0.0.1:4780'
        self.session.proxies = {
            "http": self.proxy,
            "https": self.proxy,
        }
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'android',
                'desktop': False
            },
            sess=self.session
        )

    def change_proxy(self):
        # 重新设置代理
        self.proxy = 'http://127.0.0.1:4780'
        self.session.proxies = {
            "http": self.proxy,
            "https": self.proxy,
        }

    def get_detail_link(self,app):
        package = app['appId']
        resp = self.scraper.get(DOWNLOADER_URL)
        soup = BeautifulSoup(resp.content, 'lxml')
        # 找到div标签中的data-csrf属性
        _csrf = soup.select('div.search-input')[1].get('data-csrf')
        data = {
            'package': package,
            '_csrf': _csrf,
            'region': 'US'
        }
        resp = self.scraper.post(API_URL, json=data)
        # {'error': 4, 'url': '/spotify-music-i/com.spotify.music', 'package_name': 'com.spotify.music'}
        # {"error": 5, "package_name": "com.caradvise.fuelman"} # Not Found
        print(resp.json())
        if 'url' in resp.json():
            return resp.json()['url']
        else:
            return None
    def crawl(self, app):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # 构造detail链接
                app_end_url = self.get_detail_link(app)
                # 不存在该app
                if app_end_url is None:
                    break
                app_url = BASE_URL + app_end_url
                # print(app_url)
                req = self.scraper.get(app_url)
                print()
                soup = BeautifulSoup(req.content, 'lxml')
                print(soup.select_one('div.p404').text)
                info = soup.select_one('div.additional')
                print('This is info:',info)
                try:
                    app_name = soup.select_one('div.title-like').text.strip()
                except AttributeError:
                    app_name = soup.select_one('div.title_link').h1.text.strip()

                version = info.find(string=re.compile('Latest Version')).find_next('p').text.strip()

                try:
                    size = format_size(
                        int(soup.select_one('div.ny-down')['data-dt-filesize'])
                    )
                except:
                    size = format_size(
                        int(soup.select_one('a[data-dt-file_size]')['data-dt-file_size'])
                    )

                update = info.find(string=re.compile('Updated on')).find_next('p').text.strip()
                req_android = info.find(string=re.compile('Requires Android')).find_next('p').text.strip()
                package_name = [i for i in req.url.split('/') if i][-1]
                download_url = f'https://d.apkpure.com/b/APK/{package_name}?version=latest'
                data = {
                    'version': version,
                    'update': update,
                    'requirement': req_android,
                    'size': size,
                    'apkpure_url': req.url,
                    'download_url': download_url,
                }
                app.update(data)
                r = self.scraper.get(data['download_url'], stream=True)
                fname = app['sha256'] + '.apk'
                path = pathlib.Path(f'{config.ROOT_PATH}/apps/{app["category"]}/')
                path.mkdir(mode=os.O_WRONLY, parents=True, exist_ok=True)
                f = path / fname
                with tqdm.wrapattr(
                        f.open("wb"), "write",
                        desc=f"{app['title']} ({fname.split('.')[0]})",
                        unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                        total=int(r.headers.get('content-length', 0))
                ) as fout:
                    for chunk in r.iter_content(chunk_size=4096):
                        if not chunk:
                            break
                        fout.write(chunk)

                app['apkpath'] = f'{config.ROOT_PATH}/apps/{app["category"]}/{fname}'
                # print(app)
                # for k,v in app.items():
                #     print(k,v)
                return app


            except Exception as e:
                print(f"Error during crawl attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    self.change_proxy()
                else:
                    print("Failed after 3 attempts. Giving up.")
                    # 错误文件记录
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open('error.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{now}: {app['appId']}\n")
                    return None
"""
app
{
'title': 'Spotify: Music, Podcasts, Lit',
'appId': 'com.spotify.music', 
'url': 'https://play.google.com/store/apps/details?id=com.spotify.music', 
'icon': 'https://play-lh.googleusercontent.com/P2VMEenhpIsubG2oWbvuLGrs0GyyzLiDosGTg8bi8htRXg9Uf0eUtHiUjC28p1jgHzo', 
'developer': 'Spotify AB', 
'currency': 'USD', 
'price': 0, 
'free': True, 
'scoreText': 4.4, 
'score': 4.379852, 
'category': 'ANDROID_WEAR', 
'sha256': 'be0ca287362158a5ad91beed9ebd92636eb6442e2e978de06cdd6fd57807ac75', 
'version': '8.8.22.510', 
'update': 'Mar 27, 2023', 
'requirement': 'Android 5.0+', 
'size': '74.71 MB', 
'apkpure_url': 'https://apkpure.com/spotify-music-i/com.spotify.music', 
'download_url': 'https://d.apkpure.com/b/APK/com.spotify.music?version=latest',
 apkpath': 'D:\\secComm/apps/ANDROID_WEAR/be0ca287362158a5ad91beed9ebd92636eb6442e2e978de06cdd6fd57807ac75.apk'}


"""
#
if __name__ == '__main__':

    apps = ReadCsv()
    app = {}
    for _ in apps:
        if _['appId'] == 'net.skeddy.app':
            app = _
    print(app)
    # app = {'title': 'Spotify: Music, Podcasts, Lit', 'appId': 'com.spotify.music', 'url': 'https://play.google.com/store/apps/details?id=com.spotify.music', 'icon': 'https://play-lh.googleusercontent.com/P2VMEenhpIsubG2oWbvuLGrs0GyyzLiDosGTg8bi8htRXg9Uf0eUtHiUjC28p1jgHzo', 'developer': 'Spotify AB', 'currency': 'USD', 'price': 0, 'free': True, 'scoreText': 4.4, 'score': 4.379852, 'category': 'ANDROID_WEAR', 'sha256': 'be0ca287362158a5ad91beed9ebd92636eb6442e2e978de06cdd6fd57807ac75'}

    # app = {'title': 'Fuelman Maintenance', 'appId': 'com.caradvise.fuelman',
    #  'url': 'https://play.google.com/store/apps/details?id=com.caradvise.fuelman',
    #  'icon': 'https://play-lh.googleusercontent.com/mCyKCb2VeUuDrLnz130P4Fi9JmojHbnP09wOSLOY0J1EnrhATWfgHYq6JCFjyWnRciiK',
    #  'developer': 'CarAdvise LLC', 'currency': 'USD', 'price': 0, 'free': True, 'scoreText': 0.0, 'score': 0.0,
    #  'category': 'AUTO_AND_VEHICLES', 'sha256': '3904616784c20d532df10897cd1df04b32d2b8e5e749c3e4be9ef9a7a6812f8a'}
    spider = Spider()
    appdetail = spider.crawl(app)
    print(appdetail)

