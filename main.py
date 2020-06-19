from PIL import Image
import requests
import random
import pytesseract
import json
import time
from bs4 import BeautifulSoup
import os
from Lojin import login
import sys

headers = {
    'Accept-Language':
    'zh-Hans-CN, zh-Hans; q=0.5',
    'Host':
    'urp.npumd.cn',
    'User-Agent':
    '你的UA'
}
os.chdir(sys.path[0])


class Course():
    url = 'http://urp.npumd.cn/gradeLnAllAction.do?type=ln&oper=qbinfo'
    Transcript = {}
    key = []

    def __init__(self):
        html = session.get(self.url, headers=headers)
        self.soup = BeautifulSoup(html.text, 'html.parser')
        if self.get_Transcript():
            self.printf()

    def table(self):
        i = 0
        for val in self.soup.find_all('table', 'titleTop2'):
            i = i + 1
            if i == 7:#这里填写学期（如大一第一学期，填写1，）
                self.soup = val
                return 1
        return 0

    def get_Transcript(self):
        if self.table():
            id = 0
            for val in self.soup.find_all(
                    'tr', onmouseover="this.className='evenfocus';"):
                subject = []
                for val2 in val.find_all('td', align="center"):
                    subject.append(str(val2.string).strip())
                subject.append(str(val.p.string).strip())
                id = id + 1
                self.Transcript[str(id)] = [
                    subject[2], subject[4], subject[5], subject[7]
                ]
            return 1
        else:
            print("本学期成绩未出!")
            with open('Past_transcripts.json',
                      'w') as f:
                f.write("{}")
            return 0

    def printf(self):
        """ tup = "{0:{4}<10}\t{1:^3}\t{2:^4}\t{3:^6}"
        print(tup.format("科目", '学分', "选/必", "得分", chr(12288)))
        for val1 in range(len(self.Transcript)):
            val = str(val1 + 1)
            print(
                tup.format(self.Transcript[val][0], self.Transcript[val][1],
                           self.Transcript[val][2], self.Transcript[val][3],
                           chr(12288))) """
        bi = {}
        i = 0
        s = ''
        with open('Past_transcripts.json',
                  'r',
                  encoding='UTF-8') as f:
            bi = json.load(f)
        if len(bi) < len(self.Transcript):
            text = '有新成绩出来啦!'
            i = 1
        elif len(bi) == len(self.Transcript) and bi != self.Transcript:
            text = '成绩出现变化!'
            i = 1
        if i:

            with open('Past_transcripts.json',
                      'w',
                      encoding='utf-8') as f:
                f.write(
                    json.dumps(self.Transcript, ensure_ascii=False, indent=4))
            for val in range(len(self.Transcript)):
                j = str(val + 1)
                s = s + "```" + self.Transcript[j][
                    0] + " 学分" + self.Transcript[j][1] + ' ' + self.Transcript[
                        j][2] + ' 分数' + self.Transcript[j][3] + '``` '
            desp = s
            params = {'text': text, 'desp': desp}
            requests.get(
                'https://sc.ftqq.com/你的API.send',
                params=params)


if __name__ == "__main__":
    username = 'xuehao'
    password = 'mima'
    session = login(username, password)
    if session:
        Course()
