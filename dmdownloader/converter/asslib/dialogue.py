# 描述ass中的dialogue

class Dialogue:

    TEMPLATE = "Dialogue: {},{},{},Default,,0000,0000,0000,,{}{}"

    def __init__(self, display):
        self.display = display
        self.type = display.danmaku.type
        self.text = display.danmaku.text
        self.start_time = to_ass_time(display.start_time)
        self.leave_time = to_ass_time(display.leave_time)
        self.paramenter = self.get_parameter()
        
    def get_parameter(self):        
        display = self.display
        
        params = []
        # Color 参数
        color = display.danmaku.color
        if "ffffff" != color.lower(): # 全白(ffffff)不需要添加
            params.append("\\c&H%s%s%s&" % (color[4:6], color[2:4], color[0:2]))

        if self.type == 0: # 滚动弹幕
            # move 参数
            x1, x2 = display.horizontal
            y1, y2 = display.vertical
            params.append("\\move(%d, %d, %d, %d)" % (x1, y1, x2, y2))
        elif self.type in [1, 2]: # 顶底弹幕
            # pos 参数
            x1, x2 = display.horizontal
            y1, y2 = display.vertical
            params.append("\\pos(%d, %d)" % (x1, y1))

        return "".join(params)
        

    def __str__(self):
        return self.TEMPLATE.format(self.type, self.start_time, self.leave_time, 
                            "{"+self.paramenter+"}", self.text)
    
# sec in ms
def to_ass_time(time):
    if time <= 0:
        return "0:00:00.00"

    s, ms = divmod(time, 1000) ## [long_s], [ms]
    min, s = divmod(s, 60) # [long_min], [s]
    hour, min = divmod(min, 60) # [hour], [min]
    return ("%d:%02d:%02d.%02d" % (hour, min, s, ms/10))