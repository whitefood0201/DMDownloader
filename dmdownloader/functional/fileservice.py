""" IO functions of the program """

import os
import json

def write_file(path: str, text: str) -> None:
    """
        Write a string to the giving file.
        If the file already exists, will be overwritten.
    """
    dir_check(path)
    try:
        file = open(path, "w+", encoding="UTF-8")
        file.write(text)
        file.flush()
    except IOError as e:
        print(e.args)
        raise IOError("文件写入异常")

def read_file(path: str) -> str:
    """ Read the giving file. """
    try:
        file = open(path, "r", encoding="UTF-8")
        result = file.read()
    except IOError as e:
        print(e.args)
        raise IOError("文件写入异常")
    
    return result

def load_json(path: str) -> dict:
    """ load a json file from giving path """
    return json.loads(read_file(path))

def write_json(path: str, data: dict) -> None:
    """
        Write a json file to the giving file.
        If the file already exists, will be overwritten.
    """
    dir_check(path)
    write_file(path, json.dumps(data, indent=4))
    
def dir_check(path: str) -> None:
    """
        Check the dir of the giving file.
        If it doesn't, create it.
    """
    dirpath = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(dirpath): os.mkdir(dirpath)

def copy_to(scr, dest) -> None:
    """ Copy the scr to the dest """
    text = read_file(scr)
    write_file(dest, text)