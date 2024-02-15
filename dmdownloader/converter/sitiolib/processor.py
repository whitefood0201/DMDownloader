import json

class Danmaku:

    def __init__(self, data, raw='baha'):
        if(raw == 'baha'):
            self.baha_init(data)
        elif(raw == 'bilibili'):        
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
    
    def bili_init(self, data):
        raise NotImplementedError

# 预处理
class Processor:
    def __init__(self, config: dict, gui_config: dict=None):
        self.config = config

        if gui_config != None:
            self.danmakus = self.load_from_gui(gui_config)
        else:
            self.danmakus = self.load_from_file()

    def load_from_gui(self, gui_config: dict) -> list:
        self.text = gui_config["text"]

        if "baha" == gui_config["from"]: # baha 
            return self.load_baha()
        elif "bili" == gui_config["from"]: # bilibili
            return self.load_bili()
    
        raise NotImplementedError("未知数据")
    
    def load_from_file(self) -> list:
        with open(self.config["ifile"], 'r', encoding="UTF-8") as file:
            self.text = file.read()
            
        ifile = self.config["ifile"]
        if ifile.endswith(".json"): # baha 
            return self.load_baha()
        elif ifile.endswith(".xml"): # bilibili
            return self.load_bili()
        
        raise NotImplementedError("未知文件")
        
    def load_baha(self) -> list:
        datas = json.loads(self.text)
        # 繁转简
        if self.config["open_zhconv"]:
            def t2s(data):
                data["text"] = cht2chs(data["text"])
                return data
            datas = map(t2s, datas)
            
        return list(map(Danmaku, datas))

    def load_bili(self) -> list:
        # self.danmakus = list(map(lambda x: Danmaku(x, raw="bili"), datas))
        raise NotImplementedError("b站获取暂未实现，请等待后续更新")
    
    def do_filter(self):
        top_filter = lambda dmk: dmk.type == 1
        bottom_filter = lambda dmk: dmk.type == 2
        # TODO: more filter
        filter_objs = []
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