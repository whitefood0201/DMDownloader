import sys
import dmdownloader.functional.decorators as dc
import dmdownloader.converter.filelib.asscreater as asscreater
import dmdownloader.converter.argparser as argparser
import dmdownloader.converter.conv as converter


def main():
    cfg = argparser.get_args(sys.argv)
    if(cfg == -1):
        sys.exit(0)
    
    danmaku_data, site = load_danmaku_file(cfg["ifile"])
    cfg["raw"] = site

    dias = converter.do(cfg, danmaku_data)
    dc.printReportPrinterDecorater(asscreater.create_file, asscreater.asscreater_template)(cfg, dias)

def load_danmaku_file(ifile: str) -> tuple[str, str]:
    """ Load a danmaku file, return the content and the site of it"""
    with open(ifile, 'r', encoding="UTF-8") as file:
        text = file.read()
    
    if ifile.endswith(".json"): # baha 
        return text, "baha"
    elif ifile.endswith(".xml"): # bilibili
        return text, "bili"

    raise NotImplementedError("未知文件")