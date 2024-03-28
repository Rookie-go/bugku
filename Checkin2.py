import os
import requests
USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
)
def login():
    """使用账号密码登陆 NSSCTF"""
    resp = requests.post(
        "https://www.nssctf.cn/api/user/login/",
        headers={"User-Agent": USER_AGENT},
        data={
            "username": "Rorye",
            "password": "jyj123456.",
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
def main():
    cookies = login()
    signin(cookies)
    coin_num = get_coin_num(cookies)
    if coin_num is None:
        print("签到失败")
    else:
        checkin_res = "当前的金币为: {}".format(coin_num)
        send_text("nss签到通知", checkin_res)
        print(f"签到成功，当前金币数量为 {coin_num}")
if __name__ == "__main__":
    main()