import sys
import os
import logging
from datetime import datetime
import dmdownloader.converter.argparser as argparser
from dmdownloader.converter.sitiolib.processor import Processor
from dmdownloader.converter.asslib.converter import Converter
from dmdownloader.converter.asslib.asscreater import AssCreater

def convert(cfg: dict, gui_config: dict=None) -> None:
    config = cfg.copy()
    ## 主要用于日志输入 和 IO
    if gui_config != None:
        config["ifile"] = gui_config["ifile"]
        config["ofile"] = gui_config["ofile"]

    logging.info("convert for {}".format(config["ifile"]))

    # 预处理
    pro = Processor(config, gui_config)
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
    # init logging
    if not os.path.exists("./log/"): os.mkdir("./log/")
    now = datetime.now()
    filename = "./log/" + now.strftime("%d-%m-%Y_%H-%M-%S") + ".log"
    logging.basicConfig(filename=filename, filemode="a", encoding="GBK")

    cfg = argparser.get_args(sys.argv)
    if(cfg == -1):
        sys.exit(0)
    convert(cfg=cfg)