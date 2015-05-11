# coding:utf-8

import random
import string
import tornado.web
import config


#route
class Route(object):
    urls = []
    def __call__(self, url):
        def _(cls):
            self.urls.append((url, cls))
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
    def render(self, filename=None, **kwargs):
        if not filename:
            filename = '/%s/%s.html' % (
                '/'.join(self.__module__.split('.')[1:-1]), 
                self.__class__.__name__.lower()
            )

        if lookup:
            tmpl = lookup.get_template(filename.replace(r'\\', r'/'))
            self.finish(tmpl.render(req=self, **kwargs))
        else:
            super(View, self).render(self, filename, **kwargs)
