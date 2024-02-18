# 封装网站api
import urllib.request, urllib.parse, urllib.error
import logging

BAHA_ANIMEINFO = "https://api.gamer.com.tw/mobile_app/anime/v2/video.php"
BAHA_DANMAKU = "https://ani.gamer.com.tw/ajax/danmuGet.php"

# TODO
BILI_ANIMEINFO = ""
BILI_DANMAKU = ""


def get_baha_animeinfo(sn, headers) -> str:
    url = BAHA_ANIMEINFO + "?sn={}".format(sn)
    
    try:
        response = urllib.request.urlopen(url=url, timeout=10)
        ret = response.read().decode("UTF-8")
    except urllib.error.HTTPError:
        logging.warning("api: {}: response code 403, check baha cookie".format(BAHA_ANIMEINFO))
        raise ValueError("Baha api 请求被拒，请检查cookie")
    except urllib.error.URLError:
        logging.warning("api: {}: connection failed".format(BAHA_DANMAKU))
        raise ConnectionError("网址错误或网络异常")

    return ret
    

def get_baha_danmaku(sn, headers) -> str:
    data = { "sn": sn }
    data = bytes(urllib.parse.urlencode(data), encoding="UTF-8")

    try:
        req = urllib.request.Request(url=BAHA_DANMAKU, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        ret = response.read().decode("UTF-8")
    except urllib.error.HTTPError:
        logging.warning("api: {}: response code 403, check baha cookie".format(BAHA_DANMAKU))
        raise ValueError("Baha api 请求被拒，请检查cookie")
    except urllib.error.URLError:
        logging.warning("api: {}: connection failed".format(BAHA_DANMAKU))
        raise ConnectionError("网址错误或网络异常")
    
    return ret

def get_bili_animeinfo(epid, header):
    """ TODO """
    logging.error("download: NotImplement bili")
    raise NotImplementedError("b站获取暂未实现，请等待后续更新")

def get_bili_danmaku(epid, header):
    """ TODO """
    logging.error("download: NotImplement bili")
    raise NotImplementedError("b站获取暂未实现，请等待后续更新")
