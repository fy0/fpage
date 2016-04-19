# coding:utf-8

import time
from peewee import *
from hashlib import md5
from random import Random
from model import BaseModel


def random_str(random_length=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str+=chars[random.randint(0, length)]
    return str


class USER_LEVEL:
    BAN = 0
    NORMAL = 10
    ADMIN = 100


class User(BaseModel):
    username = TextField(index=True, unique=True)
    password = TextField()
    salt = TextField()

    key = TextField(index=True)
    level = IntegerField()

    reg_time = BigIntegerField()
    key_time = BigIntegerField()

    class Meta:
        db_table = 'users'

    def is_admin(self):
        return self.level == USER_LEVEL.ADMIN

    def refresh_key(self):
        self.key = random_str(32)
        self.key_time = int(time.time())
        self.save()

    def set_password(self, new_password):
        salt = random_str()
        password_md5 = md5(new_password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        self.salt = salt
        self.password = password_final
        self.save()

    @classmethod
    def new(cls, username, password):
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_LEVEL.ADMIN if cls.count() == 0 else USER_LEVEL.NORMAL  # 首个用户赋予admin权限
        the_time = int(time.time())
        return cls.create(username=username, password=password_final, salt=salt, level=level, key=random_str(32),
                          key_time = the_time, reg_time = the_time)

    @classmethod
    def auth(cls, username, password):
        try:
            u = cls.get(cls.username==username)
        except DoesNotExist:
            return False
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + u.salt).encode('utf-8')).hexdigest()
        if u.password == password_final:
            return u

    @classmethod
    def password_change(cls, username, password, new_password):
        u = cls.auth(username, password)
        if u:
            u.set_password(new_password)
            u.refresh_key()
            return u

    @classmethod
    def exist(cls, username):
        return cls.select().where(cls.username==username).exists()

    @classmethod
    def get_by_key(cls, key):
        try:
            return cls.get(cls.key == key)
        except DoesNotExist:
            return None

    @classmethod
    def get_by_username(cls, username):
        try:
            return cls.get(cls.username == username)
        except DoesNotExist:
            return

    @classmethod
    def count(cls):
        return cls.select(cls.level>0).count()
