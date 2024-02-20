# 更新日志

## [Unreleased]


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