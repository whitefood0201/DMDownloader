# 碰撞检测
from dmdownloader.converter.asslib.display import DisplayBase

class Collision:

    def __init__(self, line_count):
        self.tracks = [
            [0]*line_count, # flow
            [0]*line_count, # top
            [0]*line_count, # buttom
        ]

    def detect(self, display: DisplayBase) -> tuple[int, int]:
        """ 碰撞检测 """
        track = self.tracks[display.danmaku["type"]]
        leave_collision_times = []

        for i, leave_collision_time in enumerate(track):
            # 有空位
            if leave_collision_time <= display.start_time:
                return i, 0
            leave_collision_times.append(leave_collision_time)

        # 无空位，找最早空出来的
        mi = min(leave_collision_times)
        index = leave_collision_times.index(mi)
        offset = mi - display.start_time
        return index, offset

    # 更新轨道，因为检测后是否应用的判断(offset判断)在外面，所以需要提供函数更新轨道
    def update(self, type, index, leave_collision_time):
        self.tracks[type][index] = leave_collision_time