import sys
import logging
import dmdownloader.converter.argparser as argparser
from dmdownloader.converter.sitiolib.processor import Processor
from dmdownloader.converter.asslib.converter import Converter
from dmdownloader.converter.asslib.asscreater import AssCreater

def convert(config: dict) -> None:
    logging.info("convert: {}".format(config["ifile"]))
    
    # 预处理
    pro = Processor(config)
    pro.do_filter()
    print("过滤 %(filted)d 条弹幕\n共 %(total)d 条，剩余 %(left)d 条" % pro.report())
    logging.info("过滤 %(filted)d 条弹幕\n共 %(total)d 条，剩余 %(left)d 条" % pro.report())

    # 将 danmaku 转换为 ass 语句
    dmks = pro.get_left()
    converter = Converter(config, dmks)
    converter.convert()
    print("丢弃 %(filted)d 条弹幕 - 共 %(total)d 条，剩余 %(left)d 条" % converter.get_report())
    logging.info("丢弃 %(filted)d 条弹幕 - 共 %(total)d 条，剩余 %(left)d 条" % converter.get_report())

    # 生成 ass 文件
    dialogues = converter.get_dialogues()
    creater = AssCreater(config, dialogues)
    
    config["ofile"] = creater.create_file()
    print('转换完毕: "%(ifile)s" -----> "%(ofile)s"' % config)
    logging.info('转换完毕: "%(ifile)s" -----> "%(ofile)s"' % config)

def main():
    cfg = argparser.get_args(sys.argv)
    if(cfg == -1):
        sys.exit(0)
    
    text, site = load_danmaku_file(cfg["ifile"])
    cfg["text"] = text
    cfg["from"] = site
    convert(config=cfg)

def load_danmaku_file(ifile) -> tuple:
    """ Load a danmaku file, return the content and the site of it"""
    with open(ifile, 'r', encoding="UTF-8") as file:
        text = file.read()
    
    if ifile.endswith(".json"): # baha 
        return text, "baha"
    elif ifile.endswith(".xml"): # bilibili
        return text, "bili"

    raise NotImplementedError("未知文件")
    
