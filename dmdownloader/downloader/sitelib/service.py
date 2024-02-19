# gui任务
import re
import logging
import os
import json as json
import dmdownloader.downloader.sitelib.siteapi as api
import dmdownloader.downloader.sitelib.siteparse as paser
import dmdownloader.converter.conv as converter

def search(url: str, config: dict) -> dict:
    """ search background task """
    logging.info("search from {}".format(url))

    match = re.search("(sn=|ss|ep)([0-9]+)", url)
    if match == None: 
        logging.warning("search: ValueError: illegal link")
        raise ValueError("请检查网址")
    
    prefix, id = match.groups()
    if prefix == "sn=":
        headers = {}
        headers["User-Agent"] = config["user_agent"]
        headers["Cookie"] = config["cookie"]
        return baha_search(id, headers)
    elif prefix in ("ss", "ep"):
        return bili_search(prefix, id)

def baha_search(sn: str, headers: dict) -> dict:
    """ search in baha """
    ret = json.loads(api.get_baha_animeinfo(sn, headers))
    return paser.parse_baha_anime_info(ret)

def bili_search(prefix: str, id: str) -> dict:
    """ search in bili """
    ret = json.loads(api.get_bili_animeinfo(prefix, id))
    return paser.parse_bili_anime_info(ret)


def download(vid: str, site:str, ofile: str, config: dict) -> None:
    """ 
        Download backgournd task.\n
        Download the danmuku from the giving site with giving video id.
    """
    logging.info("download from {}@vid={} to {}".format(site, vid, ofile))    

    # replace illegal chars of filepath
    valid_ofile = re.sub(pattern="\/|\\|\*|\?|\"|<|>|:|\|", repl="-", string=ofile)

    ofile = "./downloads/" + valid_ofile
    ifile = "(web={}*) ".format(site) + valid_ofile # for log

    if site == "baha":
        headers = { "User-Agent": config["user_agent"], "Cookie": config["cookie"] }
        text = baha_download(vid, headers)
    elif site == "bili":
        text = bili_download(vid)
    else:
        logging.warning("ValueError: Unknow website")
        raise ValueError("未知网站")

    # converter module
    if config["download_origin"]:
        path = ofile + (site == "bili" and ".xml" or ".json")
        write_file(path, text)
        logging.info('下载完毕: "{}" -----> "{}"'.format(ifile, path))
    else:
        cfg = config.copy()
        ## 主要用于日志输入 和 IO
        cfg["ifile"] = ifile
        cfg["ofile"] = ofile
        cfg["from"] = site
        cfg["text"] = text
        converter.convert(cfg)

def baha_download(sn: str, headers: dict) -> str:
    """ get the baha danmaku """
    return api.get_baha_danmaku(sn, headers)

def bili_download(cid: str) -> dict:
    """ get the bili danmaku """
    return api.get_bili_danmaku(cid)

def write_file(path: str, text: str) -> None:
    if not os.path.exists("./downloads/"): os.mkdir("./downloads/")            
    try:
        file = open(path, "w", encoding="UTF-8")
        file.write(text)
        file.flush()
    except IOError:
        raise IOError("文件写入异常")

def load_json(path: str) -> dict:
    """ load a json file from giving path """
    try:
        file = open(path, "r", encoding="UTF-8")
        config = json.loads(file.read())
    except (IOError, json.JSONDecodeError):
        logging.warning("file not found: {}".format(path))
        raise IOError("请检查文件")
    
    return config