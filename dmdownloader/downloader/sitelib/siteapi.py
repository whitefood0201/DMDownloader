# 封装网站api
import requests
import json
import logging

BAHA_ANIMEINFO = "https://api.gamer.com.tw/mobile_app/anime/v2/video.php"
BAHA_DANMAKU = "https://ani.gamer.com.tw/ajax/danmuGet.php"

# TODO
BILI_ANIMEINFO = ""
BILI_DANMAKU = ""


def get_baha_animeinfo(sn, headers) -> dict:
    url = BAHA_ANIMEINFO + "?sn={}".format(sn)
    
    try:
        resp = requests.post(url, headers=headers, timeout=5).text
        ret = json.loads(resp)
    except (requests.exceptions.RequestException):
        logging.warning("api: connection failed")
        raise ConnectionError("网址错误或网络异常")
    except json.JSONDecodeError:
        logging.warning("api: check baha cookie")
        raise ValueError("api传回异常数据，请检查cookie")

    return ret
    

def get_baha_danmaku(sn, headers) -> str:
    data = {}
    data["sn"] = sn

    try:
        resp = requests.post(BAHA_DANMAKU, data=data, headers=headers, timeout=5).text
        # 检测
        json.loads(resp)
    except (requests.exceptions.RequestException):
        logging.warning("api: connection failed")
        raise ConnectionError("网络异常")
    except json.JSONDecodeError:
        logging.warning("api: check baha cookie")
        raise ValueError("api传回异常数据，请检查cookie")
    
    return resp

def get_bili_animeinfo(epid, header):
    """ TODO """
    logging.error("download: NotImplement bili")
    raise NotImplementedError("b站获取暂未实现，请等待后续更新")

def get_bili_danmaku(epid, header):
    """ TODO """
    logging.error("download: NotImplement bili")
    raise NotImplementedError("b站获取暂未实现，请等待后续更新")
