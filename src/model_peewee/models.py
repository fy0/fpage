# coding:utf-8

from model import db
from model.test import Test

db.connect()
try: db.create_tables([Test])
except: pass
