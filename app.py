#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.ioloop
from os import path
from sys import argv
import view
import view.views
import config

application = tornado.web.Application(
    view.route.urls,
    debug=config.DEBUG,
    static_path=path.join(path.dirname(path.abspath(__file__)), 'static'),
    cookie_secret="6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC",
)

if __name__ == "__main__":
    if len(argv) > 1 and  argv[1][:6] == '-port=':
        config.PORT = int(argv[1][6:])
    print('Server started.')
    application.listen(config.PORT)
    tornado.ioloop.IOLoop.instance().start()
