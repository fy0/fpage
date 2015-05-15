# fpage

FPage 是一个tornado项目生成器。

能够自动创建基于 tornado + mako/jinja2 + sqlalchemy/peewee 的项目。


## 用法

```bash
python fpage.py startapp
```

## 特性

* 基于 tornado 

* MVT 架构(Model, View, Template)

* 基本的安全性开关 (secure cookie, xsrf)

* 支持 flask 风格的 url 装饰器 @route

* 简单 session 支持（基于 secure cookie）  

* 可选择模板引擎 mako 或 jinjia2 或 tornado 默认，已做好配置  

* 模板预定义模板变量：req static url_for csrf_token/xsrf_token  

* 集成 sqlalchemy/peewee 支持（二选一）  

* 集成类似 django 中 messages 或 flask 中 flash 的功能  


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

* 集成类似 django 中 messages 或 flask 中 flash 的功能  
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
  
## TODO-LIST

* 保持更新
