from dmdownloader.converter.asslib.collision import Collision
from dmdownloader.converter.asslib.dialogue import Dialogue
import dmdownloader.converter.asslib.display as ds

class Converter:

    def __init__(self, config, danmakus):
        self.config = config
        self.danmakus = danmakus

    def convert(self):
        dias = []
        collision = Collision(self.config["line_count"])
        for dmk in self.danmakus:
            if dmk.type > 3: continue
            display = ds.display_factor(self.config, dmk)

            track_index, offset = collision.detect(display)
            if offset > self.config["offset"]: continue

            # update, line = tarck_index+ 1
            display.relayout(offset, track_index+1)
            collision.update(dmk.type, track_index, display.leave_collision_time())

            dias.append(Dialogue(display))
        
        self.dialogues = dias
    
    def get_dialogues(self):
        return self.dialogues

    def get_report(self):
        report = {}
        report["total"] = len(self.danmakus)
        report["left"] = len(self.dialogues)
        report["filted"] = len(self.danmakus) - len(self.dialogues)
        return report