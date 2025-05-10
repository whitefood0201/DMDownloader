# 更新日志

## [Unreleased]

## [2.2.1] - 2025/05/10

### Fixed
- 修复颜色错误的问题

时隔9个月，现在才发现。主要是现在看番不搞弹幕了，感觉挡画面。


## [2.2.0] - 2024/08/03

### Added
- 现在开始能读取到baha番剧页面的特别篇了

### Changed
- 优化网站番剧解析

### Fixed
- 修复在`favorites`文件读取错误时程序退出的问题
- 修复无法下载的问题


## [2.1.1] - 2024/08/01

### Fixed
- 修复配置内容缺失时程序启动失败的错误
- 将代码内的`/`字符换为`\`

## [2.1.0] - 2024/08/01

### Added
- 添加开关类设置
- 添加数字类设置
- 添加文本类设置
- 将所有配置放入设置页面

### Changed
- 将`download_origin`设置更名为`download_raw`
- 统一程序 IO 出入口
- 完善设置页面构造逻辑
- 完善设置读取、保存逻辑
- 将默认底部弹幕偏移改为 2


## [2.0.0] - 2024/07/28

### Changed
- 使用函数式/声明式更改`converter`模块内部逻辑。
- 移除`logging`，使用重定向`print()`输出 log 。默认关闭，由`dmdownloader.downloader.downl.py`中的`log`变量控制

### Added
- 添加了设置页面，目前能对`ua`和`cookie`进行设置。
- 完善了`converter`的`-h`命令
- 现在可以对下载路径进行设置了


## [1.0.2] - 2024/04/06

### Fixed
- 修复弹幕颜色错误问题，原因为ass中使用的16进制颜色顺序为BGR，而不是常用的RGB。


## [1.0.1] - 2024/03/01

### Fixed
- 修复当展示页面内番剧条目大于8小于10时的显示问题


## [1.0.0] - 2024/02/19

### Added
- 完成了对b站的解析及获取。
- 完成了对b站弹幕的解析和转换
- 现在可以选择下载未经转换的弹幕源文件。
- 写了个 cmd 用于将 cookie 写入 config 文件，并添加了配套的`config_template.json`文件
- 合并了 converter 的与 downloader 的 changelog

### Changed
- 修改了 converter 模块的调用方式，降低了与 downloader 的耦合度


## [0.2.0] - 2024/02/17

### Changed
- 移除 Request 库，改用 Python 内置 urllib 库

### Fix
- 修复转为 ass 文件时的逻辑错误
- 将默认底部弹幕偏移改为 0


## [0.1.0] - 2024/02/13

### Added
- 完成了主要界面的编写。
- 支持对巴哈姆特的解析及获取。
- 支持对巴哈姆特的解析及转换。
- python 命令执行程序时将直接进入 converter 模块，并(只)接收命令行参数进行配置。
- 支持在`./resource/favorites.json`中添加收藏。
- 将配置存储在`./resource/config.json`中了。
- 引入`converter`模块将弹幕转换为ass。
- 在命令行模式下调用将进入`converter`模块。