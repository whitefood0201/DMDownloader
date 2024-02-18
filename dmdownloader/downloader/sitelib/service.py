# gui任务
import re
import logging
import json as json
import dmdownloader.downloader.sitelib.siteapi as api
import dmdownloader.downloader.sitelib.siteparse as paser
import dmdownloader.converter.conv as converter

def search(url: str, config: dict) -> dict:
    """ search background task """
    logging.info("search from {}".format(url))

    match = re.search("(sn=|md|ss|ep)([0-9]+)", url)
    if match == None: 
        logging.warning("search: ValueError: illegal link")
        raise ValueError("请检查网址")
    
    headers = {}
    headers["User-Agent"] = config["user_agent"]
    headers["Cookie"] = config["cookie"]
    
    prefix, id = match.groups()
    if prefix == "sn=":
        return baha_search(id, headers)
    elif prefix in ("ss", "ep", "md"):
        return bili_search(id, headers)

def baha_search(sn: str, headers: dict) -> dict:
    """ search in baha """
    ret = json.loads(api.get_baha_animeinfo(sn, headers))
    return paser.parse_baha_anime_info(ret)

def bili_search(epid: str, headers: dict) -> dict:
    """ TODO """
    logging.error("search: NotImplement bili")
    raise NotImplementedError("b站获取暂未实现，请等待后续更新")


def download(epid: str, site:str, ofile: str, config: dict) -> None:
    """ download backgournd task """
    logging.info("download from {}@epid={} to {}".format(site, epid, ofile))
    
    headers = {}
    headers["User-Agent"] = config["user_agent"]
    headers["Cookie"] = config["cookie"]

    if site == "baha":
        gui_config = baha_download(epid, ofile, headers)
    elif site == "bili":
        gui_config = bili_download(epid, ofile, headers)
    else:
        logging.warning("ValueError: Unknow website")
        raise ValueError("未知网站")

    # converter module
    converter.convert(config, gui_config)


def baha_download(sn: str, ofile: str, headers: dict) -> dict:
    """ get the baha danmaku """
    text_json = api.get_baha_danmaku(sn, headers)

    # replace illegal chars of filepath
    valid_ofile = re.sub(pattern="\/|\\|\*|\?|\"|<|>|:|\|", repl="-", string=ofile)

    gui_config = {}
    gui_config["text"] = text_json
    gui_config["from"] = "baha"
    gui_config["ofile"] = "./downloads/" + valid_ofile
    # for log
    gui_config["ifile"] = "(web=baha*) " + valid_ofile

    return gui_config

def bili_download(epid: str, ofile: str, headers: dict) -> dict:
    """ TODO """
    logging.error("download: NotImplement bili")
    raise NotImplementedError("暂未实现，请等待后续更新")


def load_json(path: str) -> dict:
    """ load a json file from giving path """
    try:
        file = open(path, "r", encoding="UTF-8")
        config = json.loads(file.read())
    except (IOError, json.JSONDecodeError):
        logging.warning("file not found: {}".format(path))
        raise IOError("请检查文件")
    
    return config