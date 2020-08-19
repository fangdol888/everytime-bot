import requests
from bs4 import BeautifulSoup
import getpass
import xml.etree.ElementTree as elemTree

import pandas as pd
import sys

from  threading import Timer
from threading import Thread

import time
import keyboard

time_interval = 10 #수집 시간 간격 설정 변수
data = {'time':[]}
df = pd.DataFrame(data)
re = True

def now_time():
      now = time.localtime()
      return "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

def scraping(article):
      title = article['title']
      id = article['id']
      index = str(id)+ title
      like = article['posvote']
      if  data.get(index) :
        data[index].append(int(like))
      else:
        data[index] = [0 for i in range(1,len(data['time']))]
        data[index].append(int(like))

def collection(s):
    now = now_time()
    print(now)
    data['time'].append(now)
    everytime_board_list = s.post(api_url + '/find/board/article/list', data={
        'id': 'hotarticle',
        'limit_num': 20,
        'start_num': 0,
        'moiminfo': True,
    })
    soup = BeautifulSoup(everytime_board_list.text, 'html.parser')
    for article in soup.findAll('article'):
        scraping(article)
    if re == True:
       Timer(time_interval,collection, args=[s]).start()


login_url ="https://everytime.kr/user/login"
api_url = 'https://api.everytime.kr/'

LOGIN_INFO = {
    'userid': '사용자이름',
    'password': '사용자패스워드'
}

LOGIN_INFO['userid'] = input("ID: ")
LOGIN_INFO['password'] = input("PW: ")

with requests.Session() as s:
    login_req = s.post(login_url, data = LOGIN_INFO)
    collection(s)

    while(True):
        if keyboard.is_pressed('q'):
            print("종료합니다.\n")
            df = pd.DataFrame(data)
            df.to_excel("test.xlsx")
            print("저장했습니다.")
            re = False
            break



