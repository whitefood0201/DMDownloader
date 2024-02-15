@ECHO OFF
SETLOCAL ENABLEEXTENSIONS
SET me=[%~n0]
SET parent=%~dp0

SET /P cookie="%me%cookie: "
SET /P user_agent="%me%user-agent: "

CD %parent%\resource

ECHO { > config.json
ECHO     "bottom_filter": false, >> config.json
ECHO     "top_filter": false, >> config.json
ECHO     "open_zhconv": true, >> config.json
ECHO     "offset": 1000, >> config.json
ECHO     "line_count": 5, >> config.json
ECHO     "bottom_offset": 1, >> config.json
ECHO     "font_size": 50, >> config.json
ECHO     "resolution": "1920*1080", >> config.json
ECHO     "font_name": "微软雅黑", >> config.json
ECHO     "ass_head": "./resource/head.txt", >> config.json
ECHO     "suffix": ".dm-chs", >> config.json
ECHO     "user_agent": "%user_agent%", >> config.json
ECHO     "cookie": "%cookie%" >> config.json
ECHO } >> config.json

cd %parent%

dmDownloader.pyw