# 解析网站 api 发过来的数据
import dmdownloader.functional.FLfunctions as fl

def parse_baha_anime_info(json: dict) -> dict:
    if json.get("error", None) != None:
        raise ValueError("api参数错误")

    anime = json["data"]["anime"]
    volumes = list(anime["volumes"].values())

    def parse_eps(vols):
        def parse_ep(vol):
            sn = vol["video_sn"]
            video_title = anime["title"][:-4] + " 第 {} 集".format(vol["volume"])
            return {"title": video_title, "id": sn}
        return fl.map(parse_ep, vols)
    def rennames(vols):
        def spec_rename(vol):
            vol["title"] = "特别篇 - " + vol["title"]
            return vol
        return fl.map(spec_rename, vols)
    
    funcs = [fl.curried_map(parse_eps), lambda x: x[0] + fl.map(rennames, x[1:]), fl.concat]
    eps = fl.pipe(funcs)(volumes)
    
    anime_info = {}
    anime_info["title"] = anime["title"]
    anime_info["from"] = "baha"
    anime_info["eps"] = eps
    
    return anime_info

def parse_bili_anime_info(json: dict) -> dict:
    if json["code"] != 0:
        raise ValueError("api参数错误")
    result = json["result"]
    volumens = result["episodes"]

    def parse_ep(vol):
        cid = vol["cid"]
        title = vol["share_copy"]
        return {"title": title, "id": cid}
    eps = fl.map(parse_ep, volumens)

    anime_info = {}
    anime_info["title"] = result["title"]
    anime_info["from"] = "bili"
    anime_info["eps"] = eps

    return anime_info