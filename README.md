# fpage

[![Travis](https://travis-ci.org/fy0/fpage.svg?branch=master)](https://travis-ci.org/fy0/fpage)
[![Code Climate](https://codeclimate.com/github/fy0/fpage/badges/gpa.svg)](https://codeclimate.com/github/fy0/fpage)

FPage 是一个传统的(即前后端分离之前)tornado项目生成器(CLI)。

能够自动创建基于 tornado + mako/jinja2 + peewee/sqlalchemy 的项目。

实例可参考 [StoryNote](https://github.com/fy0/storynote) [MyCTF](https://github.com/fy0/myctf) 等项目。


[English](README_EN.md)

## 使用

通过 pip：

```bash
pip install fpage

fpage new [项目名]
```

或者

clone后直接使用：

```bash
python fpage.py new [项目名]
```

接下来按照向导走，首先输入项目名。

然后选择一个模板引擎（**M**ako/**J**inja2/**T**ornado）

其次是ORM选择（**P**eewee/**S**QLChemy）

最后输入 y 确认

生成的目录就是你需要的，你可以试一下 python app.py 来运行他，然后访问 http://127.0.0.1:9000 来查看效果


实例：
```bash
# fpage new test_project

Project Name (test_project):
Template Engine [M/J/T]:
Database ORM [P/S]:

   Project Name: test_project
Template Engine: mako
   Database ORM: peewee

Sure (Y/n)?
Complete.

To get started:

    cd test_project
    python app.py

Served at http://localhost:9000
```



## 特性

* 基于 tornado 

* MVT 架构(Model, View, Template)

* 兼容 python 3 & python 2

* 合理的安全性支持 (secure cookie, xsrf)

* 支持 flask 风格的 url 路由装饰器 @route

* 简单 session 支持（基于 secure cookie）  

* 可选择模板引擎 mako 或 jinjia2 或 tornado 默认，已做好配置  

* 模板预定义模板变量：req static url_for csrf_token/xsrf_token config  

* 集成 sqlalchemy/peewee 支持（二选一）  

* 集成消息闪现功能（类似 django 中 messages 或 flask 中 flash）  

* 集成简单的用户系统

* 自动生成页面标题

* 可选的 Peewee 序列化扩展组件

* 内置分页工具


## 目录结构

* model 数据库交互

* view 逻辑

* templates 模板目录

* lib 存放一些全局使用的工具类


## 特性说明

* **支持 flask 风格的 url 装饰器 @route**
  ```python
  from view import route, url_for, View
  
  @route('/')
  class Index(View):
      def get(self):
          self.render()
  
      def post(self):
          pass
          
  @route('/about', name='about')
  class About(View):
      def get(self):
          self.render()

  ```

* **简单 session 支持（基于 secure cookie）**  
  ```python
  @route('/')
  class Index(View):
      def get(self):
          self.session['test'] = 'session test 1'
          del self.session['test']
          self.session['test'] = 'session test 2'
          self.render(s=self.session['test'])
  ```
  
* **可选择模板引擎 mako 或 jinjia2 或 tornado 默认，已做好配置**  
  ```mako
  <body>
      ${self.body()}
      <%block name="script"/>
  </body>
  ```
  ```jinja
  <body>
      {% block body %}{% endblock %}
      {% block script %}{% endblock %}
  </body>
  ```

* **模板预定义模板变量：req static url_for csrf_token/xsrf_token**  
  req -> request object
  ```mako
    ${ req.current_user }
  ```
  static -> static file
  ```mako
    <script src="${ static('js/main.js') }"></script>
    <link rel="stylesheet" href="${ static('css/style.css') }">
  ```
  url_for -> url reverse
  ```mako
    <p><a href="${ url_for('jump') }">Jump Page</a></p>
    <p><a href="${ url_for('about') }">About Page</a></p>
  ```
  csrf_token -> self.xsrf_form_html()
  ```mako
    <form method="post" class="am-form">
        ${csrf_token}
    </form>
  ```

* **集成 sqlalchemy/peewee 支持（二选一）**  
  config
  ```python
  DATABASE_URI = "sqlite:///database.db"
  ```
  sqlalchemy
  ```python
  from model import BaseModel
  from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
  
  
  class Test(BaseModel):
      __tablename__ = 'test'
      id = Column(Integer, primary_key=True, autoincrement=True)
      test = Column(String)
  ```
  peewee
  ```python
  from peewee import *
  from model import BaseModel
  
  
  class Test(BaseModel):
      test = TextField()
  ```

* **集成消息闪现功能（类似 django 中 messages 或 flask 中 flash）**  
  view
  ```python
  @route('/jump_test', name='jump')
  class Jump(View):
      def get(self):
          self.messages.error('Message Test: Error!!')
          self.redirect(url_for('about'))
  ```
  template
  ```mako
  % for msg in get_messages():
      % if msg.tag == 'success':
          <div class="ui-green">
              ${msg.txt}
          </div>
      % elif msg.tag == 'error':
          <div class="ui-red">
              ${msg.txt}
          </div>
      % endif
  % endfor
  ```

* **自动生成页面标题**  

  例如：config.TITLE = 'FPage'
  
  渲染模板时写入参数 page_title
  ```python
  self.render(page_title=page_title('测试板块', '社区')
  ```
  
  于是此页面网页标题就是：测试板块 » 社区 » FPage

* **内置分页工具**

    model.pagination_peewee / model.pagination_sqlalchemy
    
    参数大致如此：
    ```python
    def pagination(count_all, query, page_size, cur_page=1, nearby=2):
        pass
    ```

    输出大致如此：
    ```python
    {
        'cur_page': cur_page,
        'prev_page': prev_page,
        'next_page': next_page,

        'first_page': first_page,
        'last_page': last_page,

        'page_numbers': list(items),
        'page_count': page_count,

        'items': [...],
        'info': {
            'page_size': page_size,
            'count_all': count_all,
        }
    }
    ```


## 更新

### ver 1.2 update 2017.09.04

* 加入了分页工具

* 加入 pypi 软件源(早该如此……)


### ver 1.2alpha update 2016

* 现在 config 也作为模板中的一个预定义变量

* 加入新的 View 基类： AjaxLoginView

* 新的辅助函数：page_title，用来自定义标题

* peewee 的 BaseModel 加入了几个工具函数：to_dict（转为字典）、get_by_pk（根据主键取项，无则返回None）、exists_by_pk（根据主键判断是否存在）

* 修正了“记住密码”选项无效的问题

* 用户注册增加了“再次输入密码”的校验

* 登录和注册增加了参数 next，用来指定操作完成后跳转的url

* 加入了自动测试


### ver 1.1 update 2015.9.20

* 加入了用户模块

* 加入了与用户相关的两个View基类：LoginView（登陆后可访问） 和 NoLoginView（非登陆可访问）

* 加入了一个不检查 xsrf 的基类 AjaxView

* 默认 ORM 切换为 peewee

* 一些小的修正


## TODO-LIST

* 不再增加新功能，一个时代已经落幕
