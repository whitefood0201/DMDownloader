import sys
import dmdownloader
import os
from datetime import datetime
import logging

if __name__ != "__main__":
    raise NotImplementedError("dmDowloader can be a module")

""" init loggin """
if False:
    if not os.path.exists("./log/"): os.mkdir("./log/")
    now = datetime.now()
    filename = ".\\log\\" + now.strftime("%d-%m-%Y_%H-%M-%S") + ".log"
    logging.basicConfig(filename=filename, filemode="a", level=0, encoding="UTF-8")

if sys.stdin and sys.stdin.isatty():
    dmdownloader.start_conv()
else:
    dmdownloader.start_downl()