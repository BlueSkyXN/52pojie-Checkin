import requests 
from bs4 import BeautifulSoup
import time
import re
import rsa
import base64
import hashlib
import os
import sys

sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass
from urllib import parse

result = '🏆52破解签到姬🏆\n'

cookie = os.environ.get("cookie")
TGBOTAPI = os.environ.get("TGBOTAPI")
TGID = os.environ.get("TGID")

def pushtg(data):
    global TGBOTAPI
    global TGID
    requests.post(
        'https://api.telegram.org/bot'+TGBOTAPI+'/sendMessage?chat_id='+TGID+'&text='+data)

# 【BOTAPI】格式为123456:abcdefghi
# 【TGID】格式为123456（人）或者-100123456（群组/频道）

def main():
    global result
    headers={
        'Cookie': cookie,
        'ContentType':'text/html;charset=gbk'
    }
    requests.session().get('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2',headers=headers)
    fa=requests.session().get('https://www.52pojie.cn/home.php?mod=task&do=draw&id=2',headers=headers)
    fb=BeautifulSoup(fa.text,'html.parser')         
    fc=fb.find('div',id='messagetext').find('p').text
    print("🏆52破解签到姬🏆\n")
    print("返回内容")
    print(fc)
    if  "您需要先登录才能继续本操作"  in fc:
        result += "Cookie失效"
    elif "恭喜"  in fc:
        result += "签到成功"
    elif "不是进行中的任务"  in fc:
        result += "不是进行中的任务"
    else:
        result += "签到成功失败"
    
    pushtg(result)
    
    
def main_handler(event, context):
    main()


if __name__ == '__main__':
    main()
