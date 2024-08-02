import getopt

HELP_STR = '''
Convert the raw danmaku data to a loadable ass file. Only support `Bilibili` and `Bahamut`

--bottom_filter[swith]  -b  Open the bottom filter.
--top_filter[swith]     -t  Open the top filter.
--open_zhconv[swith]        Convert the zh_tw to zh_cn.
--ifile=[str]           -i  the input file.
--ofile=[str]           -o  The out file.
--offset=[int]          -d  The Max. offset of the danmakus, in ms. Default 1000ms.
--line_count=[int]      -c  The max. line(track) of the danmakus.
--bottom_offset=[int]       The line count that the bottom danmaku will elevate. Default 2 lines.
--font_size=[int]           The font size, deafault 50px.
--resolution=[int*int]      The resolution of video, default "1920*1080".
--font_name=[str]           Font.
--ass_head=[str]            The path will the ass head be, default ".\\resource\\head.txt".
--suffix=[str]              The suffix will add to the out file, default ".dm-chs".    
'''

CONFIG = {
    "bottom_filter": False,
    "top_filter": False,
    "open_zhconv": True,
    "offset": 1000, # in ms
    "line_count": 5,
    "bottom_offset": 2, # 底部弹幕向上偏移n行
    "font_size": 50,
    "resolution": "1920*1080",
    "font_name": "微软雅黑",
    "ass_head": ".\\resource\\head.txt",
    "suffix": ".dm-chs",
    "ifile": "",
    "ofile": ""
}

# 开关索引
OPTIONS = (0, 2)
# int参数索引
INT_PARAMS = (3, 7)

# Long opts, using the keys of the dict. And like some "opt" require a "input value", so should add a "=" in the end
# also see "getopt.getopt()"
# switch opts + config opts
LONG_OPTS = list(CONFIG.keys())[OPTIONS[0]:OPTIONS[1]+1] + list(map(lambda str: str+"=", CONFIG.keys()))[OPTIONS[1]+1:]

SHORT_MAPPING = {
    "b": "bottom_filter",
    "t": "top_filter",
    "i": "ifile",
    "o": "ofile",
    "c": "line_count",
    "d": "offset"
}
 
# short opts, using the keys of the mapping dict. But like some "opt" require a "input value", so should add a ":" in the end
# also see "getopt.getopt()"
# config opts + switch opts
SHORT_OPTS = "h" + "".join(list(map(lambda str: str+":", SHORT_MAPPING.keys()))[-4:] + list(SHORT_MAPPING.keys())[:-4])

def get_args(argv):

    try:
        opts, args = getopt.getopt(argv[1:], SHORT_OPTS, LONG_OPTS)
    except getopt.GetoptError:
        print("Error in command line arguments.")
        print('A basic usage example: ', argv[0], ' -i <inputfile>', sep='')
        return -1
    
    if (argv[1:] == []) | ("-h" in argv) | (opts == []):
        print(HELP_STR)
        return -1
    
    for opt, val in opts:
        # remove "-"
        opt = opt.replace("-", "");
        # mapping to long, if it's short
        if opt in SHORT_MAPPING.keys():
            opt = SHORT_MAPPING.get(opt)

        if (opt == "ifile") & (CONFIG["ofile"] == ""):
            # set the default out file
            CONFIG["ifile"] = val
            name = val.split(".")[:-1]
            CONFIG["ofile"] = ".".join(name)

        if val == "": # mean it's a switch opt
            val = True
        elif opt in list(CONFIG.keys())[INT_PARAMS[0]: INT_PARAMS[1]+1]: # it's a int
            val = int(val)

        CONFIG[opt] = val

    return CONFIG