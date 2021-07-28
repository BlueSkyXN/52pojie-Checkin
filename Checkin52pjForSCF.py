# -*- coding: utf8 -*-

import requests, os, sys, re
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass
from bs4 import BeautifulSoup

cookie = os.environ.get('cookie_52pj')
pj_rate = os.environ.get('rate_52pj')

s = requests.Session()
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'Cookie': cookie,
    'ContentType':'text/html;charset=gbk'
}

def main(*args):
    msg = ""
    try:
        s.get('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2', headers=headers)
        a = s.get('https://www.52pojie.cn/home.php?mod=task&do=draw&id=2', headers=headers)
        b = BeautifulSoup(a.text,'html.parser')
        c = b.find('div',id='messagetext').find('p').text

        if "您需要先登录才能继续本操作"  in c:
            pusher("52pojie  Cookie过期", c)
            msg += "cookie_52pj失效，需重新获取"
        elif "恭喜"  in c:
            msg += "52pj签到成功"
        elif "不是进行中的任务" in c:
            msg += "不是进行中的任务"
        else:
            print(c)
    except:
        msg += "52pj出错,大概率是触发52pj安全防护，访问出错。自行修改脚本运行时间和次数，总有能访问到的时间"
        msg += "\n如果错误需要推送的话，自行去掉代码内的注释"
        #pusher("52pojie  访问出错", b)
    return msg + "\n"


def pjRate(*args):
    msg = ""
    try:
        # 获取热门帖子
        rssurl = "https://www.52pojie.cn/forum.php?mod=guide&view=hot&rss=1"
        r = s.get(rssurl, headers=headers)
        tidlist = re.findall("tid=\d+", r.text)
        for tid in tidlist:
            tid = tid[4:]
            # 获取评分所需信息
            url = f'https://www.52pojie.cn/forum.php?mod=viewthread&tid={tid}'
            r = s.get(url, headers=headers)
            if "需要登录" in r.text:
                pusher("52pojie  Cookie过期")
                msg += "cookie_52pj失效，需重新获取"
                break
            formhash = re.findall("formhash=\w+", r.text)[0][9:]
            pid = re.findall("pid=\d+", r.text)[0][4:]
            data = {
                "formhash": formhash,
                "tid": tid,
                "pid": pid,
                "referer": f"https://www.52pojie.cn/forum.php?mod=viewthread&tid={tid}&page=0#pid{pid}",
                "handlekey": "rate",
                "score2": "1",
                "score6": "1",
                "reason": "热心回复！".encode("GBK")
            }
            # 免费评分
            rateurl = 'https://www.52pojie.cn/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1'
            r = s.post(rateurl, headers=headers, data=data)
            if "succeedhandle_rate" in r.text:
                msg += re.findall("succeedhandle_rate\('.*'", r.text)[0][19:]
                break
            elif "评分数超过限制" in r.text:
                msg += re.findall("errorhandle_rate\('.*'", r.text)[0][18:-1]
                break
            else:
                msg += re.findall("errorhandle_rate\('.*'", r.text)[0][18:-1]
                msg += "\n"
    except:
        # pusher("52pojie  免费评分失败")
        pass
    return msg + "\n"


def pjCheckin(*args):
    global cookie
    msg = ""
    if "\\n" in cookie:
        clist = cookie.split("\\n")
    else:
        clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += main()
        if pj_rate:
            msg += pjRate()
        i += 1
    print(msg[:-1])
    return msg

if __name__ == "__main__":
    if cookie:
        print("----------52pojie开始尝试签到----------")
        pjCheckin()
        print("----------52pojie签到执行完毕----------")
