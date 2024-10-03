# -*- coding:utf-8 -*-
import os

import requests
import json
import re

from PyQt5.QtCore import QThread,pyqtSignal
from merge import merge_video_audio

class MyThread(QThread):
    success = pyqtSignal(str)
    def __init__(self,url,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.url = url
    def sanitize_filename(self,filename):
        # 定义非法字符列表
        illegal_chars = r'\/:*?"<>|\.'

        # 移除非法字符，并将空格替换为下划线
        sanitized = re.sub(r'[' + re.escape(illegal_chars) + r']', '', filename)
        pattern = r"[^\u4e00-\u9fa5A-Za-z\u0020-\u007E]"
        # 使用re.sub替换所有不符合pattern的字符为空字符串
        sanitized = re.sub(pattern, '_', sanitized)
        sanitized = sanitized.replace(' ', '_')

        return sanitized
    def get_proxy(self):
        url = 'http://v2.api.juliangip.com/dynamic/getips?filter=1&num=1&pt=1&result_type=json2&trade_no=1838434402564052&sign=7c150cd0dcb9d1ab2c552114c7e897cb'
        proxy_response = requests.get(url)
        proxy_dict = proxy_response.json()
        proxies = {
            'ip': proxy_dict['data']['proxy_list'][0]['ip'],
            'port': proxy_dict['data']['proxy_list'][0]['port']
        }
        # proxies = proxy_dict['data']['proxy_list'][0]['ip'] + ':' + str(proxy_dict['data']['proxy_list'][0]['port'])
        print('proxies:', proxies)
        return proxies
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }
        try:
            print('开始请求')
            # proxies = self.get_proxy()
            # response = requests.get(url=self.url, headers=headers, proxies=proxies)
            response = requests.get(url=self.url, headers=headers)
            print('status_code:',response.status_code)
            html_source = response.text
            # print('html_source:', html_source)
            info = re.findall(r'<script>window.__INITIAL_STATE__=(.*?});', html_source, re.S)
            result_json = json.loads(info[0])
            title = result_json['videoData']['title']
            title = self.sanitize_filename(title)
            print(title)
            pattern = re.compile(r'<script>window.__playinfo__=(.*?)</script>', re.S)
            result = pattern.findall(html_source)[0]
            result_json = json.loads(result)
            videos = result_json['data']['dash']['video']
            video_url = videos[0]['baseUrl']
            audios = result_json['data']['dash']['audio']
            audio_url = audios[0]['baseUrl']

            # resp_video = requests.get(url=video_url, headers=headers, proxies=proxies)
            # resp_audio = requests.get(url=audio_url, headers=headers, proxies=proxies)
            resp_video = requests.get(url=video_url, headers=headers)
            resp_audio = requests.get(url=audio_url, headers=headers)
            if not os.path.exists('../video'):
                os.mkdir('../video')
            with open(f'../video/{title}_test.mp4', mode='wb') as f:
                f.write(resp_video.content)
            with open(f'../video/{title}.mp3', mode='wb') as f:
                f.write(resp_audio.content)
            merge_video_audio(f'../video/{title}_test.mp4', f'../video/{title}.mp3', f'../video/{title}.mp4')
            os.remove(f'../video/{title}_test.mp4')
            os.remove(f'../video/{title}.mp3')
            self.success.emit('success')
        except Exception as e:
            raise e
