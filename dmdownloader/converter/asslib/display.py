from unicodedata import east_asian_width

class DisplayBase:
    def __init__(self, config, danmaku):
        self.danmaku = danmaku
        self.config = config
        self.screen_x, self.screen_y = map(int, config["resolution"].split("*"))
        self.line = 1

        self.text_length = self._text_length()
        self.height = self.config["font_size"]
        self.width = self._width()

        self.vertical = self._vertical()
        self.horizontal = self._horizontal()

        self.start_time = self.danmaku.time
        self.leave_time = self._leave_time()

    def _text_length(self):
        """ 文本字符总数，ascill 字符为1，否则为2 """
        width = 0
        for char in self.danmaku.text:
            width += east_asian_width(char) == "Na" and 1 or 2
        return width + 1 # +1 当作左右边框
    
    def _width(self):
        """ 文本长度，像素 """
        return self.config["font_size"] * (self.text_length / 2)
    
    def _horizontal(self):
        """ 水平轴 起始坐标 及 结束坐标 """
        x = self.screen_x // 2
        return (x, x) # x1, x2

    def _vertical(self):
        """ 垂直轴 起始坐标 及 结束坐标 """
        y = self.screen_y // 2
        return (y, y) # y1, y2

    def _leave_time(self):
        """ 弹幕离开屏幕时间 """
        return self.start_time + self.duration()

    def relayout(self, offset ,line):
        """ 根据 offset 和 line 重新布局 """
        self.start_time = self.start_time + offset
        self.line = line
        self.vertical = self._vertical()
        self.leave_time = self._leave_time()
    
    # 提供给顶底弹幕
    def duration(self):
        """ 弹幕持续时间 """
        # TODO, custom_tune_duration
        base = 2
        if self.text_length < 4:
            base += 1
        elif self.text_length < 8:
            base +=2
        else:
            base += 3
        
        return base * 1000 # in ms
    
    def leave_collision_time(self):
        """ 离开碰撞时间，不会遮挡下个弹幕的最小时间 """
        return self.start_time + self.duration()

class TopDisplay(DisplayBase):

    def _vertical(self):
        y = self.line * self.height
        return (y, y)

class BottomDisplay(DisplayBase):

    def _vertical(self):
        line = self.line - 1 + self.config["bottom_offset"]
        y = self.screen_y - (line * self.height)
        return (y, y)

class FlowDisplay(DisplayBase):

    def _vertical(self):
        y = self.line * self.height
        return (y, y)

    def _horizontal(self): # x
        # ass 字幕基准点取决于行对齐，默认为字幕下方正中间
        base = self.width / 2
        x1 = self.screen_x + base # 让起始坐标刚好在屏幕外面
        x2 = - base # 结束时刚好全部出去
        return (x1, x2)
    
    def speed(self):
        """ 弹幕速度，pixel / s """
        # TODO, custom_tune_duration
        return self.screen_x / 12.0
        
    def duration(self):
        # 路程(起始坐标到结束坐标) / 速度
        x1, x2 = self.horizontal
        distance = x1 - x2
        return int(distance / self.speed()) * 1000
    
    def leave_collision_time(self):
        # 滚动弹幕离开碰撞时间就是完全进入屏幕时，即走过自身长度所需的时间
        return self.start_time + (self.width / self.speed() * 1000)
    
def display_factor(config, danmaku):
    type = danmaku.type
    match(type):
        case 0: return FlowDisplay(config, danmaku)
        case 1: return TopDisplay(config, danmaku)
        case 2: return BottomDisplay(config, danmaku)
        case _: raise NotImplementedError("未知弹幕类型")