# coding:utf-8

import json
import random
import string
import tornado.web
import config
from lib.jsdict import JsDict


# route
class Route(object):
    urls = []

    def __call__(self, url, name=None):
        def _(cls):
            self.urls.append(tornado.web.URLSpec(url, cls, name=name))
            return cls
        return _


route = Route()


# 模板
def get_lookup_mako():
    import mako.lookup

    _lookup = mako.lookup.TemplateLookup(
            directories=['./templates'],
            module_directory='/tmp/mako' + ''.join(random.sample(string.ascii_letters + string.digits, 8)),
            input_encoding='utf-8',
    )
    return _lookup


def get_lookup_jinja2(_globals={}, extensions=[]):
    from jinja2 import Environment, FileSystemLoader

    _lookup = Environment(
        loader=FileSystemLoader(['./templates'], encoding='utf-8'),
        extensions=extensions
    )
    # mako 没有全局变量特性，这里为了一致性 jinjia 向 mako 妥协
    #_lookup.globals['url_for'] = url_for
    _lookup.globals['config'] = config
    _lookup.globals.update(_globals)
    return _lookup

if config.TEMPLATE == 'mako':
    lookup = get_lookup_mako()
elif config.TEMPLATE == 'jinja2':
    lookup = get_lookup_jinja2()
else:
    lookup = None


# Session
class SimpleSession(object):
    def __init__(self, request):
        self._request = request
        self._data = self.load()

    def __delitem__(self, key):
        del self._data[key]

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        self._data[key] = value

    def load(self):
        _s = self._request.get_secure_cookie('session') or '{}'
        try: _s = _s.decode('utf-8') # fix:py2
        except: pass
        return json.loads(_s)

    def flush(self):
        self._request.set_secure_cookie('session', json.dumps(self._data))


# 消息闪现支持
class Messages(object):

    MESSAGE_LEVEL = JsDict(
        DEBUG=10,
        INFO=20,
        SUCCESS=25,
        WARNING=30,
        ERROR=40,
    )

    DEFAULT_TAGS = {
        MESSAGE_LEVEL.DEBUG: 'debug',
        MESSAGE_LEVEL.INFO: 'info',
        MESSAGE_LEVEL.SUCCESS: 'success',
        MESSAGE_LEVEL.WARNING: 'warning',
        MESSAGE_LEVEL.ERROR: 'error',
    }

    def __init__(self):
        self.messages = []

    def _add_message(self, level, message):
        self.messages.append([level, message])

    def debug(self, message):
        self._add_message(self.MESSAGE_LEVEL.DEBUG, message)

    def info(self, message):
        self._add_message(self.MESSAGE_LEVEL.INFO, message)

    def success(self, message):
        self._add_message(self.MESSAGE_LEVEL.SUCCESS, message)

    def warning(self, message):
        self._add_message(self.MESSAGE_LEVEL.WARNING, message)

    def error(self, message):
        self._add_message(self.MESSAGE_LEVEL.ERROR, message)


class View(tornado.web.RequestHandler):
    def render(self, fn=None, **kwargs):
        if not fn:
            fn = ('/%s/%s.html' % (
                '/'.join(self.__module__.split('.')[1:-1]), 
                self.__class__.__name__.lower()
            )).replace(r'//', r'/')

        kwargs.update({
            'req': self,
            'static': self.static_url,
            'url_for': self.reverse_url,
            'get_messages': self.get_messages,
            'xsrf_token': self.xsrf_form_html(),
            'csrf_token': self.xsrf_form_html(),
        })

        if lookup:
            tmpl = lookup.get_template(fn)
            self.finish(tmpl.render(**kwargs))
        else:
            if fn.startswith('/'):
                fn = '.' + fn
            super(View, self).render(fn, config=config, **kwargs)

    def get_messages(self):
        msg_lst = self.messages.messages + (self.session['_messages'] or [])
        _messages = []

        for i in msg_lst:
            tag, txt = i
            try: txt = txt.decode('utf-8') # 为py2做个转换
            except: pass
            _messages.append(JsDict(tag=Messages.DEFAULT_TAGS[tag], txt=txt))

        self.messages.messages = []
        return _messages

    def initialize(self):
        self.messages = Messages()
        self.session = SimpleSession(self)
        super(View, self).initialize()

    def flush(self, include_footers=False, callback=None):
        self.session['_messages'] = self.messages.messages
        self.session.flush()
        super(View, self).flush(include_footers, callback)


# sugar
def url_for(name, *args):
    return config.app.reverse_url(name, *args)

