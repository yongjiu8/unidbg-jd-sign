import json
import random
import re
import threading
import time
import requests
import datetime
from urllib.parse import quote, unquote

starttime = 1652507999000

mycookies = [
    '',
]


range_n = 3  # 链接个数
range_sleep = 0.5  # 间隔时间
delay_time = 0.4

# 辅助参数
atime = 0
re_body = re.compile(r'body=.*?&')


def get_sign_api(functionId, body):
    sign_api = 'http://127.0.0.1:8888/jd/sign'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'functionId': functionId,
        'body': json.dumps(body, ensure_ascii=False)
    }
    res = requests.post(url=sign_api, headers=headers, data=data, timeout=30).json()
    if res['code'] == 0:
        return res['data']
    else:
        print(res['msg'])
        return -1


def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)


def getCcFeedInfo(cookie, index):
    eid = randomString(16)
    body = {
        "categoryId": 118,
        "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
        "eid": eid,
        "globalLat": "",
        "globalLng": "",
        "lat": "",
        "lng": "",
        "monitorRefer": "appClient",
        "monitorSource": "ccfeed_android_index_feed",
        "pageClickKey": "Coupons_GetCenter",
        "pageNum": 1,
        "pageSize": 20,
        "shshshfpb": ""
    }
    res = get_sign_api('getCcFeedInfo', body)
    if res == -1:
        return -1
    else:
        url = f'https://api.m.jd.com?functionId=getCcFeedInfo{res}&eid={eid}'
        headers = {
            "cookie": cookie,
            "user-agent": "okhttp/3.12.1;jdmall;android;version/11.0.2;build/97565;",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        data = {
            "body": json.dumps(body)
        }
        res = requests.post(url=url, headers=headers, data=data, timeout=30).json()
        print(res)
        if res['code'] == '0':
            for coupon in res['result']['couponList']:
                if coupon['title'] != None and '每周可领一次' in coupon['title']:
                    receiveKey = coupon['receiveKey']
                    print(f'账号{index + 1}：获取receiveKey成功')
                    return receiveKey
            print(f'账号{index + 1}：没有找到59-20券的receiveKey')
            return -1
        else:
            print(f'账号{index + 1}：获取59-20券的receiveKey失败')
            return -1


def get_receiveNecklaceCoupon_sign(receiveKey):
    eid = randomString(16)
    body = {"channel": "领券中心",
            "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
            "couponSource": "manual",
            "couponSourceDetail": None,
            "eid": eid,
            "extend": receiveKey,
            "lat": "",
            "lng": "",
            "pageClickKey": "Coupons_GetCenter",
            "rcType": "4",
            "riskFlag": 1,
            "shshshfpb": "",
            "source": "couponCenter_app",
            "subChannel": "feeds流"
            }
    # res = get_sign_api('newReceiveRvcCoupon', body) # 领券
    res = get_sign_api('receiveNecklaceCoupon', body)  # 59-20
    if res == -1:
        return -1
    else:
        url = f'https://api.m.jd.com?functionId=receiveNecklaceCoupon{res}&eid={eid}'
        data = {
            "body": json.dumps(body, ensure_ascii=False)
        }
        return [url, data]


def receiveNecklaceCoupon(url, body, cookie, index):
    headers = {
        "cookie": cookie,
        "user-agent": "okhttp/3.12.1;jdmall;android;version/11.0.2;build/97565;",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    res = requests.post(url=url, headers=headers, data=body, timeout=30).json()
    try:
        if res['code'] == '0' and res['msg'] == '响应成功':
            print(f"账号{index + 1}：{res['result']['desc']}")
    except:
        pass


def jdtime():
    url = 'http://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5'
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    try:
        res = requests.get(url=url, headers=headers, timeout=1).json()
        return int(res['currentTime2'])
    except:
        return 0


def use_thread(cookie, index):
    if receiveKeys[index] != -1:
        print(f'账号{index + 1}：正在生成{range_n * 2}条抢券链接')
        tasks = list()
        s = 0
        while s < range_n:
            res = get_receiveNecklaceCoupon_sign(receiveKeys[index])
            if res != -1:
                url = res[0]
                body = res[1]
                tasks.append(threading.Thread(target=receiveNecklaceCoupon, args=(url, body, cookie, index)))
                tasks.append(threading.Thread(target=receiveNecklaceCoupon, args=(url, body, cookie, index)))
                s = s + 1
        print(f'账号{index + 1}：{range_n * 2}条抢券链接生成完毕，等待抢券')
        while True:
            if jdtime() >= starttime:
                time.sleep(delay_time)
                for task in tasks:
                    task.start()
                    time.sleep(range_sleep)
                for task in tasks:
                    task.join()
                break


if __name__ == '__main__':

    print('59-20准备...')
    print('正在获取59-20券key')
    while True:
           if datetime.datetime.now().hour ==23:
              time.sleep(0.2)
              atime = 0
           else:
             break
    receiveKeys = []
    for i in range(len(mycookies)):
        receiveKey = getCcFeedInfo(mycookies[i], i)
        receiveKeys.append(receiveKey)
    if len(receiveKeys) != 0:
        # print(receiveKeys)
        while True:
            if starttime - int(time.time() * 1000) <= 180000:
                break
            else:
                if int(time.time() * 1000) - atime >= 30000:
                    atime = int(time.time() * 1000)
                    print(f'等待获取log中，还差{int((starttime - int(time.time() * 1000)) / 1000)}秒')

        threads = []
        for i in range(len(mycookies)):
            threads.append(
                threading.Thread(target=use_thread, args=(mycookies[i], i))
            )
        for t in threads:
            t.start()
        for t in threads:
            t.join()
