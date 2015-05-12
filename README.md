# fpage

一个轻量级的 tornado web 项目模板。

像创建一个 Flask 项目一样轻松的创建一个 Tornado 项目。

## 用法

下载之，置于一个新目录，稍微编辑一下config.py

开始使用。

## 特性

* 基于 tornado 

* MVT 架构(Model, View, Template)

* 简单 session 支持（基于 cookie）

* 可选择模板引擎 mako 或 jinjia2，已做好配置

* 支持 flask 风格的 url 装饰器 @route

* 模板预定义三个变量：req url_for static

* 集成 sqalchemy 支持

* [WIP]集成类似 flask 中 flash 或 django 中 messages 的功能

## TODO-LIST

* peewee 支持

* 添加 messages(flask) 支持

