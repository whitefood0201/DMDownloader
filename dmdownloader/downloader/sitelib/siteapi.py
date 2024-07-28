# 封装网站api
import urllib.request, urllib.parse, urllib.error
import zlib

BAHA_ANIMEINFO = "https://api.gamer.com.tw/mobile_app/anime/v2/video.php"
BAHA_DANMAKU = "https://ani.gamer.com.tw/ajax/danmuGet.php"

BILI_ANIMEINFO = "https://api.bilibili.com/pgc/view/web/season?{}={}"
BILI_DANMAKU = "https://comment.bilibili.com/{}.xml"


def get_baha_animeinfo(sn, headers) -> str:
    url = BAHA_ANIMEINFO + "?sn={}".format(sn)
    
    try:
        response = urllib.request.urlopen(url=url, timeout=10)
        ret = response.read().decode("UTF-8")
    except urllib.error.HTTPError as e:
        raise ValueError("Baha api 请求失败，请检查cookie")
    except urllib.error.URLError as e:
        raise ConnectionError("网址错误或网络异常")

    return ret
    

def get_baha_danmaku(sn, headers) -> str:
    data = { "sn": sn }
    data = bytes(urllib.parse.urlencode(data), encoding="UTF-8")

    try:
        req = urllib.request.Request(url=BAHA_DANMAKU, data=data, headers=headers, method="POST")
        response = urllib.request.urlopen(req, timeout=10)
        ret = response.read().decode("UTF-8")
    except urllib.error.HTTPError as e:
        raise ValueError("Baha api 请求失败，请检查cookie")
    except urllib.error.URLError as e:
        raise ConnectionError("网址错误或网络异常")
    
    return ret


def get_bili_animeinfo(prefix, id):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    mapping = { "ep": "ep_id", "ss": "season_id" }

    url = BILI_ANIMEINFO.format(mapping[prefix], id)

    try:
        req = urllib.request.Request(url=url, headers=headers, method="GET")
        response = urllib.request.urlopen(req, timeout=10)
        ret = response.read().decode("UTF-8")
    except urllib.error.HTTPError as e:
        raise ValueError("Bili api 请求失败")
    except urllib.error.URLError as e:
        raise ConnectionError("网址错误或网络异常")
    
    return ret

def get_bili_danmaku(cid):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = BILI_DANMAKU.format(cid)

    try:
        req = urllib.request.Request(url=url, headers=headers, method="GET")
        response = urllib.request.urlopen(req, timeout=10)
        # b站弹幕xml文件使用deflate编码
        ret = zlib.decompress(response.read(), -zlib.MAX_WBITS).decode("UTF-8")
    except urllib.error.HTTPError as e:
        raise ValueError("Bili api 请求失败")
    except urllib.error.URLError as e:
        raise ConnectionError("网址错误或网络异常")

    return ret
