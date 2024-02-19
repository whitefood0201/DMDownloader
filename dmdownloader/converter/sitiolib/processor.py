import json
import re

class Danmaku:

    def __init__(self, data, raw='baha'):
        if(raw == 'baha'):
            self.baha_init(data)
        elif(raw == 'bili'):        
            self.bili_init(data)
        else:
            raise NotImplementedError
    
    def baha_init(self, data):
        self.color = data['color'][1:] # 16进制
        self.text = data['text']
        self.time = int((data['time'])*100) # 出现时间，单位 ms。baha单位为0.1秒
        # 巴哈姆特的弹幕类型 0=滚动，1=顶部，2=底部
        # 弹幕类型 0: 滚动 1: 上浮 2: 下浮 -1: 不支持
        self.type = int(data['position'])
    
    def bili_init(self, data: tuple):
        ''' 弹幕属性: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/danmaku/danmaku_xml.md '''
        attr_str, content = data
        attrs = attr_str.split(",")

        self.text = content
        self.time = int(float(attrs[0]) * 1000) # b站单位秒，float类型
        self.color = hex(int(attrs[3])) # b站为十进制RGB888，int类型

        match(int(attrs[1])):
            case 1|2|3|6: self.type = 0
            case 5: self.type = 1
            case 4: self.type = 2
            case _: self.type = -1

# 预处理
class Processor:
    def __init__(self, config: dict):
        self.config = config
        self.danmakus = self.load_danmaku(config)
        
    def load_danmaku(self, config: dict) -> list:
        self.text = config["text"]

        if "baha" == config["from"]: # baha 
            return self.load_baha()
        elif "bili" == config["from"]: # bilibili
            return self.load_bili()
    
        raise NotImplementedError("未知数据")
        
    def load_baha(self) -> list:
        datas = json.loads(self.text)
        # 繁转简
        if self.config["open_zhconv"]:
            def t2s(data):
                data["text"] = cht2chs(data["text"])
                return data
            datas = map(t2s, datas)
            
        dmks = list(map(Danmaku, datas))
        dmks.sort(key=lambda dmk: dmk.time)
        return dmks

    def load_bili(self) -> list:
        text = self.text.replace('<d p="', '\n<d p="')
        match = re.compile('<d p="(.+)">(\\S+)<\\/d>')
        datas = match.findall(text)

        dmks = list(map(lambda data: Danmaku(data, raw="bili"), datas))
        dmks.sort(key=lambda dmk: dmk.time)
        return dmks

    
    def do_filter(self):
        top_filter = lambda dmk: dmk.type == 1
        bottom_filter = lambda dmk: dmk.type == 2
        none_filter = lambda dmk: dmk.type == -1
        # TODO: more filter
        filter_objs = []
        filter_objs.append(none_filter)
        if self.config["top_filter"]:
            filter_objs.append(top_filter)
        if self.config["bottom_filter"]:
            filter_objs.append(bottom_filter)

        danmakus = self.danmakus
        left = []
        for danmaku in danmakus:
            keep = True
            for filter in filter_objs:
                if filter(danmaku):
                    keep = False
                    break
            if keep:
                left.append(danmaku)
        
        self.left_danmakus = left

    def get_left(self):
        return self.left_danmakus

    def report(self):
        report = {}
        report["total"] = len(self.danmakus)
        report["left"] = len(self.left_danmakus)
        report["filted"] = len(self.danmakus) - len(self.left_danmakus)

        return report
    
def cht2chs(str):
    try:
        import zhconv
    except ModuleNotFoundError:
        raise ModuleNotFoundError("zhconv 繁转简模块未找到")
    return zhconv.convert(str, "zh-cn")