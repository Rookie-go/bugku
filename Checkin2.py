import os
import requests
USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
)
class login(object):
    """使用账号密码登陆 NSSCTF"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def login(self):
        resp = requests.post(
            "https://www.nssctf.cn/api/user/login/",
            headers={"User-Agent": USER_AGENT},
            data={
                "username": self.username,
                "password": self.password,
            },
        )
        cookies = dict(resp.cookies)
        cookies["token"] = resp.json()["data"]["token"]
        return cookies


def signin(cookies):
    """签到"""
    resp = requests.post(
        "https://www.nssctf.cn/api/user/clockin/",
        headers={"User-Agent": USER_AGENT},
        cookies=cookies,
    )
    return resp.json()["code"] == 200


def get_coin_num(cookies):
    """获取金币数量"""
    resp = requests.get(
        "https://www.nssctf.cn/api/user/info/opt/setting/",
        headers={"User-Agent": USER_AGENT},
        cookies=cookies,
    )
    data = resp.json()
    if data["code"] != 200:
        return None
    return data.get("data", {}).get("coin", None)
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
    return r.content
    
if __name__ == "__main__":
    username = os.environ.get("NSS_USERNAME")
    password = os.environ.get("NSS_PASSWORD")
    NSS=login(username,password)
    cookies=NSS.login()
    signin(cookies)
    coin_num = get_coin_num(cookies)
    if coin_num is None:
        print("签到失败")
    else:
        checkin_res = f"当前的金币为: {coin_num}"
        send_text("Bugku签到通知", checkin_res)
        print(f"签到成功，当前金币数量为 {coin_num}")