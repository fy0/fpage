#!/usr/bin/env python
# coding:utf-8

import lib.patch
import tornado.web
import tornado.ioloop
from os import path
from sys import argv

import config
import view.views
import model.models
from view import route


application = tornado.web.Application(
    route.urls,
    debug=config.DEBUG,
    static_path=path.join(path.dirname(path.abspath(__file__)), 'static'),
    template_path="templates",
    cookie_secret=config.COOKIE_SECRET,
    xsrf_cookies=True,
)

config.app = application

if __name__ == "__main__":
    if len(argv) > 1 and  argv[1][:6] == '-port=':
        config.PORT = int(argv[1][6:])

    application.listen(config.PORT)
    print('Server started at port %s' % config.PORT)
    tornado.ioloop.IOLoop.instance().start()
