from unicodedata import east_asian_width

class DiaplyBase:
    def __init__(self, config, danmaku):
        self.danmaku = danmaku
        self.config = config
        self.screen_x, self.screen_y = map(int, config["resolution"].split("*"))
        self.line = 0

        self.text_length = self.text_length()
        self.width = self.width()
        self.height = self.config["font_size"]

        self.start_point = self.get_start_point()
        self.end_point = self.get_end_point()

        self.start_time = self.danmaku.time
        self.leave_time = self.get_leave_time()

    def relayout(self, offset ,line):
        self.start_time = self.start_time + offset
        self.line = line
        self.start_point = self.get_start_point()
        self.end_point = self.get_end_point()
        self.leave_time = self.get_leave_time()

    def text_length(self):
        width = 0
        for char in self.danmaku.text:
            width += east_asian_width(char) == "Na" and 1 or 2
        return width
    
    def width(self):
        # 实际上算出来的也还是不够精确，有些偏小
        # 手动乘1.2
        return self.config["font_size"] * (self.text_length / 2) * 1.2
    
    def get_start_point(self):
        return (0, 0)

    def get_end_point(self):
        return (0, 0)
    
    # 提供给顶底弹幕
    def duration(self):
        base = 2
        if self.text_length < 4:
            base += 1
        elif self.text_length < 8:
            base +=2
        else:
            base += 3
        
        return base * 1000 # in ms
    
    def get_leave_time(self):
        return self.start_time + self.duration()
    
    def get_leave_collision_time(self):
        return self.start_time + self.duration()

class TopDisplay(DiaplyBase):

    def get_start_point(self):
        line = self.line
        return self.screen_x // 2, line * self.config["font_size"]

    def get_end_point(self):
        return self.get_start_point()


class BottomDisplay(DiaplyBase):

    def get_start_point(self):
        line = self.line + 1
        return (self.screen_x // 2, 
                self.screen_y - ((line + self.config["bottom_offset"]) * self.height))

    def get_end_point(self):
        return self.get_start_point()
    

class FlowDisplay(DiaplyBase):

    def get_start_point(self):
        return (self.screen_x + self.width,
                self.line * self.config["font_size"])

    def get_end_point(self):
        return (-self.width,
            self.line * self.config["font_size"])
    
    def speed(self):
        """ pixel / s """
        return self.screen_x / 12.0
        
    def duration(self):
        return int((self.screen_x + self.width) / self.speed()) * 1000
    
    def get_leave_collision_time(self):
        return self.start_time + (self.width / self.speed() * 1000)
    
def display_factor(config, danmaku):
    type = danmaku.type
    match(type):
        case 0: return FlowDisplay(config, danmaku)
        case 1: return TopDisplay(config, danmaku)
        case 2: return BottomDisplay(config, danmaku)
        case _: raise NotImplementedError