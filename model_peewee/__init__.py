# coding:utf-8

import config
import peewee
from playhouse.db_url import connect

db = connect(config.DATABASE_URI)


class BaseModel(peewee.Model):
    class Meta:
        database = db
