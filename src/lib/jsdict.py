# coding:utf-8


class JsDict(dict):
    def __getitem__(self, item):
        return self.get(item)

    def __repr__(self):
        return '<jsDict ' + dict.__repr__(self) + '>'

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getattr__ = __getitem__

