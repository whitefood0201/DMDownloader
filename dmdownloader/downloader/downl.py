import sys
from datetime import datetime
import tkinter.messagebox as msg
import dmdownloader.downloader.gui as gui
import dmdownloader.functional.fileservice as fs

LOG = False
FAVORITES_PATH = ".\\resource\\favorites.json"
CONFIG_PATH = ".\\resource\\config.json"
LOG_PATH = ".\\log\\" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".log"
DEAFAULT_GLOBAL_CONFIG =  {  
    "bottom_filter": False,
    "top_filter": False,  
    "open_zhconv": True,  
    "offset": 1000,  
    "line_count": 5,  
    "bottom_offset": 2,  
    "font_size": 50,  
    "resolution": "1920*1080",  
    "font_name": "微软雅黑",  
    "ass_head": ".\\resource\\head.txt",
    "suffix": ".dm-chs",  
    "download_raw": False, 
    "download_path":".downloads\\",
    "user_agent": "",
    "cookie": ""
} 


def main():
    """ start window """
    
    if LOG:
        savedStdout = sys.stdout
        fs.dir_check(LOG_PATH)
        sys.stdout = open(LOG_PATH, "x")

    # 载入config
    try:
        global_config: dict = fs.load_json(CONFIG_PATH)
        if global_config.keys() != DEAFAULT_GLOBAL_CONFIG.keys(): raise KeyError("配置缺失")
    except (IOError, KeyError) as e:
        print(e.args)
        msg.showerror(title="错误", message="配置文件载入错误，使用默认配置。")
        global_config:dict = DEAFAULT_GLOBAL_CONFIG.copy()
        fs.copy_to(CONFIG_PATH, CONFIG_PATH+"_old")

    # 载入favorites
    favorites = {}
    try:
        favorites = fs.load_json(FAVORITES_PATH)
    except IOError:
        pass

    root = gui.DownloaderApp(cfg=global_config, favorites=favorites)
    root.mainloop()

    # 重新写入config
    fs.write_json(CONFIG_PATH, global_config)