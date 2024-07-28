import os
import json

def write_file(path: str, text: str) -> None:
    dir_check(path)
    try:
        file = open(path, "w", encoding="UTF-8")
        file.write(text)
        file.flush()
    except IOError:
        raise IOError("文件写入异常")

def load_json(path: str) -> dict:
    """ load a json file from giving path """
    try:
        file = open(path, "r", encoding="UTF-8")
        result = json.loads(file.read())
    except (IOError, json.JSONDecodeError):
        #logging.warning("file not found: {}".format(path))
        raise IOError("请检查文件")
    
    return result

def write_json(path: str, data: dict) -> None:
    """ write a json file to the giving path"""
    dir_check(path)
    try:
        file = open(path, "w+", encoding="UTF-8")
        file.write(json.dumps(data, indent=4))
    except (IOError, json.JSONDecodeError):
        #logging.warning("file not found: {}".format(path))
        raise IOError("请检查文件")
    
def dir_check(path: str) -> None:
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath): os.mkdir(dirpath)