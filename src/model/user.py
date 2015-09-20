# coding:utf-8

import time
from hashlib import md5
from random import Random
from model import BaseModel, DBSession
from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey, Boolean


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
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True)
    password = Column(String)
    salt = Column(String)

    key = Column(String, index=True)
    level = Column(Integer)

    reg_time = Column(BigInteger)
    key_time = Column(BigInteger)

    __tablename__ = 'users'

    def is_admin(self):
        return self.level == USER_LEVEL.ADMIN
        
    def refresh_key(self):
        session = DBSession()
        self.key = random_str(32)
        self.key_time = int(time.time())
        session.add(self)
        session.commit()

    @classmethod
    def new(cls, username, password):
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_LEVEL.ADMIN if cls.count() == 0 else USER_LEVEL.NORMAL  # 首个用户赋予admin权限
        the_time = int(time.time())

        session = DBSession()
        ret = cls(username=username, password=password_final, salt=salt, level=level, key=random_str(32),
                          key_time = the_time, reg_time = the_time)
        session.add(ret)
        session.commit()
        session.close()
        return ret

    @classmethod
    def auth(cls, username, password):
        session = DBSession()
        u = session.query(cls).filter(cls.username==username).first()
        if not u:
            return False
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + u.salt).encode('utf-8')).hexdigest()

        if u.password == password_final:
            return u

    @classmethod
    def exist(cls, username):
        session = DBSession()
        return session.query(cls).filter(cls.username==username).count() > 0

    @classmethod
    def get_by_key(cls, key):
        session = DBSession()
        return session.query(cls).filter(cls.key==str(key or b'', 'utf-8')).first()

    @classmethod
    def count(cls):
        session = DBSession()
        return session.query(cls).filter(cls.level>0).count()
