# fpage

FPage 是一个tornado项目生成器。

能够自动创建基于 tornado + mako/jinja2 + sqlalchemy/peewee 的项目。


## 使用

```bash
python fpage.py startapp
```

按照向导走，首先输入项目名。

然后选择一个模板引擎（**M**ako/**J**inja2/**T**ornado）

其次是ORM选择（**P**eewee/**S**QLChemy）

最后输入 y 确认

生成的目录就是你需要的，你可以试一下 python app.py 来运行他，然后访问 http://127.0.0.1:9000 来查看效果


## 特性

* 基于 tornado 

* MVT 架构(Model, View, Template)

* 兼容 python 2 & python 3

* 合理的安全性支持 (secure cookie, xsrf)

* 支持 flask 风格的 url 装饰器 @route

* 简单 session 支持（基于 secure cookie）  

* 可选择模板引擎 mako 或 jinjia2 或 tornado 默认，已做好配置  

* 模板预定义模板变量：req static url_for csrf_token/xsrf_token  

* 集成 sqlalchemy/peewee 支持（二选一）  

* 集成消息闪现功能（类似 django 中 messages 或 flask 中 flash）  

* 集成简单的用户系统

## 目录结构

* model 数据库交互

* view 逻辑

* templates 模板目录

* lib 存放一些全局使用的工具类


## 特性说明

* 支持 flask 风格的 url 装饰器 @route
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

* 简单 session 支持（基于 secure cookie）  
  ```python
  @route('/')
  class Index(View):
      def get(self):
          self.session['test'] = 'session test 1'
          del self.session['test']
          self.session['test'] = 'session test 2'
          self.render(s=self.session['test'])
  ```
  
* 可选择模板引擎 mako 或 jinjia2 或 tornado 默认，已做好配置  
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

* 模板预定义模板变量：req static url_for csrf_token/xsrf_token  
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

* 集成 sqlalchemy/peewee 支持（二选一）  
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

* 集成消息闪现功能（类似 django 中 messages 或 flask 中 flash）  
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

## 更新

### ver 1.1 update 2015.9.20

* 加入了用户模块

* 加入了与用户相关的两个基类：LoginView（登陆后可访问） 和 NoLoginView（非登陆可访问）

* 加入了一个不检查 xsrf 的基类 AjaxView

* 默认 ORM 切换为 peewee

* 一些小的修正

## TODO-LIST

* 保持更新
