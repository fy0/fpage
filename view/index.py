# coding:utf-8

from view import route, View

@route('/')
class Index(View):
    def get(self):
        self.render()
