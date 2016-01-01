# fpage

FPage is a tornado project generator.

Quick start a project with tornado + mako/jinja2 + peewee/sqlalchemy。


## Use

```bash
python fpage.py startapp
```

1. Type your project name.

2. Choose template engine (**M**ako/**J**inja2/**T**ornado)

3. Choose the ORM you like best(**P**eewee/**S**QLChemy)

4. Enter Y to confirm.

Now here is a directory, it's protype of your project.

python app.py to run, and access http://127.0.0.1:9000 to check.


## Features

* based on tornado  

* MVT Pattern (Model, View, Template)  

* compatible with python 3 & python 2  

* secure support (secure cookie, xsrf)  

* URL Route decorator like flask (@route)  

* simple session support（based on secure cookie）  

* choose your favourite template engine (mako/jinjia2/tornado)  

* defined template variable: req static url_for csrf_token/xsrf_token config  

* choose your favourite ORM sqlalchemy/peewee  

* message flashing (like of messages django, and flash of flask）  

* simple user system  

* page title helper tool  


## directories

* model

* view

* templates

* lib - tools


## Feature Example

* URL Route decorator like flask (@route)  
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

* Simple session support（based on secure cookie）  
  ```python
  @route('/')
  class Index(View):
      def get(self):
          self.session['test'] = 'session test 1'
          del self.session['test']
          self.session['test'] = 'session test 2'
          self.render(s=self.session['test'])
  ```
  
* Choose your favourite template engine (mako/jinjia2/tornado)  
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

* Defined template variable: req static url_for csrf_token/xsrf_token config  
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

* Choose your favourite ORM sqlalchemy/peewee  
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

* Message flashing (like of messages django, and flash of flask）  
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

* Page title helper tool  

  config
  ```python
  config.TITLE = 'FPage'
  ```

  View
  ```python
  self.render(page_title=page_title('Test Board', 'Forum')
  ```
  
  The title of page: Test Board » Forum » FPage


## TODO-LIST

* file upload  

* paginator (SQLAlchemy ver)

* auto tests

* setup.py
