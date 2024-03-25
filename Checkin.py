import os
import random
import time
import ddddocr
import requests
from retrying import retry

class BugkuCK(object):
    LOGIN_SUCCESS = {"code": 1, "msg": "登录成功", "data": "", "url": "/", "wait": 3}
    PASS_ERROR = {"code": 0, "msg": "账号或密码失败", "data": "", "url": "", "wait": 3}
    VCODE_ERROR = {"code": 0, "msg": "验证码错误!", "data": "", "url": "", "wait": 3}

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    def pd_login(self):
        captcha = ss.get(f'https://ctf.bugku.com/captcha.html{random.random()}', proxies=proxies, headers=get_headers, verify=False)
        vcode = ocr.classification(captcha.content)
        print(vcode)
        assert len(vcode) == 4
        time.sleep(3)
        res = ss.post('https://ctf.bugku.com/login/check.html',
                      data={'username': self.username,
                            'password': self.password,
                            'vcode': vcode,
                            'autologin': '1'}, proxies=proxies, headers=post_headers, verify=False).json()
        assert '验证码错误' not in res['msg']
        return res

    def login(self):
        try:
            return self.pd_login()
        except:
            return self.VCODE_ERROR

    def checkin(self):
        res = ss.get('https://ctf.bugku.com/user/checkin', proxies=proxies, headers=post_headers, verify=False).json()
        code = res['code']
        msg = res['msg']
        if code == 1:
            data = res['data']
            user_id = data['user_id']
            count = data['count']
            coin = data['coin']
            msg = f'{msg}\n\n{user_id}：恭喜您获得：{coin}金币，已连续签到：{count}天'
        return msg

def send_text(title, content):
    dingtalk_access_token = os.environ.get("DINGTALK_ACCESS_TOKEN")
    url = f"https://oapi.dingtalk.com/robot/send?access_token={dingtalk_access_token}"
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": f'**{title}**\n\n{content}'
        }
    }
    r = requests.post(url, json=data)
    # print(r.content)
    return r.content

if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    ss = requests.session()
    ocr = ddddocr.DdddOcr(old=True, show_ad=False)
    post_headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    get_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    # proxies = {'http': 'http://localhost:7722', 'https': 'http://localhost:7722'}
    proxies = {'http': '', 'https': ''}

    username = os.environ.get("BUGKU_USERNAME")
    password = os.environ.get("BUGKU_PASSWORD")

    bk =BugkuCK(username, password)
    login_res = bk.login()
    code = login_res['code']
    msg = login_res['msg']
    if code == 1:
        checkin_res = bk.checkin()
        print(checkin_res)
    else:
        print(msg)
        checkin_res = msg
    print(send_text("Bugku签到通知", checkin_res))
    print('--------------------\n\n')

# git init
# git add .
# git commit -m 'first'
# git branch -M main
# git remote add origin https://github.com/Rookie-go/bugku.git
# git push -u origin main

