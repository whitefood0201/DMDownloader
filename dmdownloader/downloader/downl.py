import logging
import os
from datetime import datetime
import dmdownloader.downloader.gui as gui

def main():
    """ init loggin """
    if not os.path.exists("./log/"): os.mkdir("./log/")
    now = datetime.now()
    filename = ".\\log\\" + now.strftime("%d-%m-%Y_%H-%M-%S") + ".log"
    logging.basicConfig(filename=filename, filemode="a", level=0, encoding="GBK")
    
    """ start window """
    root = gui.DownloaderApp()
    root.mainloop()