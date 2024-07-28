import dmdownloader.converter.sitiolib.danmaku as danmaku
import dmdownloader.converter.sitiolib.filter as filter
import dmdownloader.converter.asslib.converter as converter
from dmdownloader.converter.asslib.dialogue import Dialogue
import dmdownloader.functional.FLfunctions as fl
import dmdownloader.functional.decorators as dc

def do(global_config: dict, str_danmakus: str) -> list[Dialogue]:
    '''
        The enter of the converter    
        will print the report using `print()`

        args:
            global_config,
            raw danmakus data: xml for bilibili, json for bahamut

        return:
          the dialogue data    
    '''
    funcs = [
        dc.globalConfigDecorater(danmaku.generate, global_config),
        dc.globalConfigDecorater(dc.printReportPrinterDecorater(filter.do, filter.filter_report_template), global_config),
        dc.globalConfigDecorater(dc.printReportPrinterDecorater(converter.do, converter.converter_report_template), global_config),
    ]
    return fl.pipe(funcs)(str_danmakus)