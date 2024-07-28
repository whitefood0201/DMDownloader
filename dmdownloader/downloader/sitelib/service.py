# gui任务
import re
import json
import dmdownloader.functional.fileservice as fs
import dmdownloader.downloader.sitelib.siteapi as api
import dmdownloader.functional.decorators as dc
import dmdownloader.downloader.sitelib.siteparse as paser
import dmdownloader.converter.conv as converter
import dmdownloader.converter.filelib.asscreater as asscreater

def search(url: str, config: dict) -> dict:
    """ search background task """
    print("search from {}".format(url))

    match = re.search("(sn=|ss|ep)([0-9]+)", url)
    if match == None: 
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


def download(vid: str, site: str, ofile: str, config: dict) -> None:
    """ 
        Download backgournd task.\n
        Download the danmuku from the giving site with giving video id.
    """
    print("download from {}@vid={} to {}".format(site, vid, ofile))

    # replace illegal chars of filepath
    valid_ofile = re.sub(pattern="\/|\\|\*|\?|\"|<|>|:|\|", repl="-", string=ofile)

    ofile = config["download_path"] + "\\" + valid_ofile
    ifile = "(web={}*) ".format(site) + valid_ofile # for log

    if site == "baha":
        headers = { "User-Agent": config["user_agent"], "Cookie": config["cookie"] }
        text = baha_download(vid, headers)
    elif site == "bili":
        text = bili_download(vid)
    else:
        raise ValueError("未知网站")

    # converter module
    if config["download_origin"]:
        path = ofile + (site == "bili" and ".xml" or ".json")
        fs.write_file(path, text)
        print('下载完毕: "{}" -----> "{}"'.format(ifile, path))
    else:
        cfg = config.copy()
        ## 主要用于日志输入 和 IO
        cfg["ifile"] = ifile
        cfg["ofile"] = ofile
        cfg["raw"] = site
        dias = converter.do(cfg, text)
        dc.printReportPrinterDecorater(asscreater.create_file, asscreater.asscreater_template)(cfg, dias)

def baha_download(sn: str, headers: dict) -> str:
    """ get the baha danmaku """
    return api.get_baha_danmaku(sn, headers)

def bili_download(cid: str) -> dict:
    """ get the bili danmaku """
    return api.get_bili_danmaku(cid)
