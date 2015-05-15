# coding:utf-8


class JsDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self): return '<jsDict ' + dict.__repr__(self) + '>'
