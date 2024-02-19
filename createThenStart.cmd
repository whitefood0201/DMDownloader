@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
SET me=[%~n0]
SET parent=%~dp0
SET parent=%parent:~0,-1%

SET template=.\resource\config_template.json
SET out=.\resource\config.json

SET /P cookie="%me%cookie: "
SET /P ua="%me%user-agent: "

ECHO= > %out%
:: 根据配置模板生成配置文件
FOR /f "delims=" %%l IN (%template%) DO (
    SET str=%%l
    SET "str=!str:{UA}=%ua%!"
    SET "str=!str:{COOKIE}=%cookie%!"
    ECHO !str! >> %out%
)

dmDownloader.pyw