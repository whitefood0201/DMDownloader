from dmdownloader.converter.asslib.collision import Collision
from dmdownloader.converter.asslib.dialogue import Dialogue
import dmdownloader.converter.asslib.display as ds
import dmdownloader.functional.FLfunctions as fl
import dmdownloader.functional.decorators as dc

# TODO 这边也有点乱感觉
def do(global_config:dict, dmks:list[dict]) -> tuple[list[Dialogue], dict[str, int]]:
        '''
            Convert the parsed danmaku data to ass dialogue

            args:
                global_config.
                parsed danmakus data.

            return:
                dialogues, see: `dmconverter.asslib.dialogue.Dialogue`.
                report detail: dict{total, left, discard}
        '''
        collision = Collision(global_config["line_count"])

        ds_factory = dc.globalConfigDecorater(ds.display_factory, global_config)
        def detector(display: ds.DisplayBase) -> ds.DisplayBase:
            '''
            Collision detection    

            returns:    
              The detected `diaplay`    
              None if the offset exceeds the tolerance limit    
            '''
            track_index, offset = collision.detect(display)
            if offset > global_config["offset"]:     
                return None
            display.relayout(offset, track_index+1)
            collision.update(display.danmaku["type"], track_index, display.leave_collision_time())
            return display
        
        funcs = [
            fl.curried_filter(lambda dmk: dmk["type"]>3),
            fl.curried_map(ds_factory),
            fl.curried_map(detector),
            fl.curried_filter(lambda disp: disp==None),
            fl.curried_map(Dialogue)
        ]

        dias = fl.pipe(funcs)(dmks)
        report_detail = get_report(dmks, dias)
        return (dias, report_detail)

converter_report_template: str = "丢弃 %(discard)d 条弹幕 - 共 %(total)d 条，剩余 %(left)d 条"
def get_report(dmks, dias):
    report = {}
    report["total"] = len(dmks)
    report["left"] = len(dias)
    report["discard"] = len(dmks) - len(dias)
    return report