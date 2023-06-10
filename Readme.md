# 周赛

## 概述
这是一个专门记录周赛题目的repo.

本地使用 [obsidian](https://obsidian.md/) 组织和书写, 并没有添加任何社区插件, 只是调整了一下字体和其他一些显示上的设置, 因此没有上传 `.obsidian` 目录.

周赛以目录形式组织, 每场对应一个目录, 每个目录下有汇总的`Readme`作为跳转. 同时每个题目也有固定的模板.

每个题目通过开头的[YAML front matter](https://help.obsidian.md/Advanced+topics/YAML+front+matter) 添加 `tag` ,  以此进行分类和聚合.

## 一些工具

### 周赛模板
添加新的场次, 可以使用[tool/new_week](https://github.com/hxzhao527/leetcode-weekly/blob/main/tools/new_week.py) 快捷创建, 比如 `./tools/new_week.py 83` 即可根据模板创建好相应文件和目录, 同时附有相关题目的连接, 不用再打开竞赛的页面即可查看相应题目.
支持单周赛和双周赛.

### 转化html
> [!warning]-
> 需要在根目录的 `Readme` 中引用周赛对应的文件才能创建索引.

使用工具[obsidianhtml](https://obsidian-html.github.io/) 将仓储转化为html, 然后利用[Github Actions](https://github.com/features/actions)发布到[Github Pages](https://pages.github.com/).

#### 查看方式
1. 左侧场次目录, 右侧 `TOC`
2. 页面下方有 `graph` 可以查看关系图
3. 顶部导航支持搜索, 设置主题, 查看`tag`
4. 题目详情内下方, 也有 `tag` 的链接

## 周赛目录
- [第83场周赛](./week-83/Readme.md)
- [第84场周赛](./week-84/Readme.md)
- [第85场周赛](./week-85/Readme.md)
- [第86场周赛](./week-86/Readme.md)
- [第87场周赛](./week-87/Readme.md)
- [第88场周赛](./week-88/Readme.md)
- [第89场周赛](./week-89/Readme.md)
- [第90场周赛](./week-90/Readme.md)
- [第91场周赛](./week-91/Readme.md)
