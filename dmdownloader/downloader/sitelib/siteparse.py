# 解析网站 api 发过来的数据
import logging

def parse_baha_anime_info(json: dict) -> dict:
    if json.get("error", None) != None:
        logging.warning("baha parse: illegal args")
        raise ValueError("api参数错误")

    anime_info = {}
    anime = json["data"]["anime"]
    volumes = anime["volumes"]["0"]

    anime_info["title"] = anime["title"]
    anime_info["from"] = "baha"

    eps = {}
    for i, vol in enumerate(volumes, 1):
        sn = vol["video_sn"]
        video_title = anime["title"][:-4] + " 第 {} 集".format(i)
        eps[video_title] = sn
    
    anime_info["eps"] = eps
    
    return anime_info

def parse_bili_anime_info(json: dict) -> dict:
    if json["code"] != 0:
        logging.warning("bili parse: illegal args")
        raise ValueError("api参数错误")
    result = json["result"]
    volumens = result["episodes"]

    anime_info = {}
    anime_info["title"] = result["title"]
    anime_info["from"] = "bili"

    eps = {}
    for vol in volumens:
        cid = vol["cid"]
        title = vol["share_copy"]
        eps[title] = cid
    anime_info["eps"] = eps

    return anime_info