# coding:utf-8

import random
import string
import tornado.web
import config


#route
class Route(object):
    urls = []

    def __call__(self, url, name=None):
        def _(cls):
            self.urls.append(tornado.web.URLSpec(url, cls, name=name))
            return cls
        return _


route = Route()


#模板
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


class View(tornado.web.RequestHandler):
    def render(self, fn=None, **kwargs):
        if not fn:
            fn = ('/%s/%s.html' % (
                '/'.join(self.__module__.split('.')[1:-1]), 
                self.__class__.__name__.lower()
            )).replace(r'//', r'/')

        if lookup:
            tmpl = lookup.get_template(fn)
            self.finish(tmpl.render(req=self, static=self.static_url, url_for=self.reverse_url, **kwargs))
        else:
            super(View, self).render(self, fn, req=self, static=self.static_url, url_for=self.reverse_url, **kwargs)
