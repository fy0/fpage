# coding:utf-8

from view import route, View

@route('/', name="index")
class Index(View):
    def get(self):
        self.render()

    def post(self):
        pass
