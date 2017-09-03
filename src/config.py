# coding:utf-8

PORT = 9000
DEBUG = True
TITLE = 'FPage'
VERSION = '1.2.0'
TEMPLATE = 'mako'  # jinja2/mako/tornado
DATABASE_URI = "sqlite:///database.db"
COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

try:
    from private import *
except:
    pass
