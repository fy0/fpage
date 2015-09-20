# coding:utf-8

from model import db
from model.test import Test
from model.user import User

db.connect()
db.create_tables([Test, User], safe=True)
