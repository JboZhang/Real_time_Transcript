from PIL import Image
import requests
import random
import pytesseract
import json
import time
from bs4 import BeautifulSoup
import os
from io import BytesIO
headers = {
    'Accept-Language':
    'zh-Hans-CN, zh-Hans; q=0.5',
    'Host':
    'urp.npumd.cn',
    'User-Agent':
    '你的ua'
}

session = requests.session()


def get_img_code():
    try:
        for _ in range(12):
            img = session.get('http://urp.npumd.cn/validateCodeAction.do?' +
                              str(random.random()),
                              headers=headers).content
            img = Image.open(BytesIO(img))
            w, h = img.size
            img = img.resize((w * 2, h * 2))
            img = img.convert('L')
            i = 127
            tuble = []
            for t in range(256):
                if t < i:
                    tuble.append(0)
                else:
                    tuble.append(1)
            img = img.point(tuble, '1')
            img = pytesseract.image_to_string(img,
                                              lang='eng',
                                              config='--psm 6')
            img = ''.join(img.split())
            if (len(img) == 4):
                break
        return img
    except:
        print("验证码获取过程错误")
        return ''


def login(username, password):
    try:
        for _ in range(12):
            data = {'mm': password, 'zjh': username, 'v_yzm': get_img_code()}
            html = session.post('http://urp.npumd.cn/loginAction.do',
                                headers=headers,
                                data=data)
            if "<title>学分制综合教务</title>" in html.text:
                return session
            if '你输入的证件号不存' in html.text:
                print('密码错误!')
                return 0
            time.sleep(2)

        return 0
    except:
        print("登陆错误!")
        return False
