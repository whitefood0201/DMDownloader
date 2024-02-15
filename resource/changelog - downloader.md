# 更新日志

## [Unreleased]

### Added
- 完成了对b站的解析及获取。
- 现在可以直接获取未经转换的下载弹幕源文件。

### Changed
- 与`converter`解耦合

## [0.1.0] - 2024/02/13

### Added
- 完成了主要界面的编写。
- 支持对巴哈姆特的解析及获取。
- 支持在`./resource/favorites.json`中添加收藏。
- 将配置存储在`./resource/config.json`中了。
- 引入`converter`模块将弹幕转换为ass。
- 在命令行模式下调用将进入`converter`模块。