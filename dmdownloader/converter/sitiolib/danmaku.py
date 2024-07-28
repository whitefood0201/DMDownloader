import json
import re
import dmdownloader.functional.FLfunctions as fl


def parse_baha(json_data: str) -> list[dict]:
    return json.loads(json_data)

def parse_bili(xml_data: str) -> list[tuple]:
    text = xml_data.replace('<d p="', '\n<d p="')
    match = re.compile('<d p="(.+)">(\\S+)<\\/d>')
    return match.findall(text)

'''
parsed danmaku data format:
{"text":, "color":, "time":, "type":}
'''
def baha_generate(data: dict) -> dict:
    dmk = {}
    dmk["text"] = data['text']
    dmk["color"] = data['color'][1:] # 16进制
    dmk["time"] = int((data['time'])*100) # baha单位为0.1秒
    dmk["type"] = int(data['position']) # 巴哈姆特的弹幕类型 0=滚动，1=顶部，2=底部
    return dmk
    
def bili_generate(data: tuple) -> dict:
    dmk = {}
    ''' 弹幕属性: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/danmaku/danmaku_xml.md '''
    attr_str, dmk["text"] = data
    attrs = attr_str.split(",")

    dmk["time"] = int(float(attrs[0]) * 1000) # b站单位秒，float类型
    dmk["color"] = hex(int(attrs[3])) # b站为十进制RGB888，int类型
    type = -1
    match(int(attrs[1])):
        case 1|2|3|6: type = 0
        case 5: type = 1
        case 4: type = 2
    dmk["type"] = type
    return dmk

def generate_factory(raw: str) -> list:
    '''
        Get the correspond generate function
    '''
    if "baha" == raw:
        return [fl.curried_map(baha_generate), parse_baha]
    elif "bili" == raw:
        return [fl.curried_map(bili_generate), parse_bili]
    else:
        raise NotImplementedError("Unkown raw: ", raw, ". Only support baha & bili")

def generate(global_config: dict, data: str) -> list[dict]:
    '''
        Parse the raw danmaku data
        
        return:
            The parsed danmaku data.    
            Parsed danmaku data format:     
            {"text":  ,"color":  ,"time":  ,"type":  }
    '''
    funcs =  [fl.curried_sort(lambda dmk: dmk["time"]), list]
    if(global_config["open_zhconv"]):
        def cht2(dmk:dict) -> dict:
            dmk["text"]=cht2chs(dmk["text"])
            return dmk
        funcs.append(fl.curried_map(cht2))
    funcs += generate_factory(global_config["raw"])
    
    return fl.compose(funcs)(data)

def cht2chs(str: str) -> str:
    try:
        import zhconv
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Can't found zhconv")
    return zhconv.convert(str, "zh-cn")