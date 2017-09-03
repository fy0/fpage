# coding:utf-8

import sys
import time
from hashlib import md5
from random import Random
from model import BaseModel, DBSession
from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey, Boolean
from lib.state_obj import StateObject

py_ver = sys.version_info.major

def random_str(random_length=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str+=chars[random.randint(0, length)]
    return str


class USER_STATE(StateObject):
    DEL = 0
    BAN = 30
    NORMAL = 50
    ADMIN = 100

    txt = {DEL: '删除', BAN: '封禁', NORMAL: '正常', ADMIN: '管理'}

USER_STATE.init()


class User(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True)
    password = Column(String)
    salt = Column(String)

    key = Column(String, index=True)
    state = Column(Integer)

    reg_time = Column(BigInteger)
    key_time = Column(BigInteger)

    __tablename__ = 'users'

    def is_admin(self):
        return self.state == USER_STATE.ADMIN
        
    def refresh_key(self):
        session = DBSession()
        self.key = random_str(32)
        self.key_time = int(time.time())
        session.add(self)
        session.commit()

    def set_password(self, new_password):
        username = username.lower()
        salt = random_str()
        password_md5 = md5(new_password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        
        session = DBSession()
        self.salt = salt
        self.password = password_final
        session.add(self)
        session.commit()

    @classmethod
    def new(cls, username, password):
        username = username.lower()
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        state = USER_STATE.ADMIN if cls.count() == 0 else USER_STATE.NORMAL  # first user is admin
        the_time = int(time.time())

        session = DBSession()
        ret = cls(username=username, password=password_final, salt=salt, state=state, key=random_str(32),
                          key_time = the_time, reg_time = the_time)
        session.add(ret)
        session.commit()
        return ret

    @classmethod
    def password_change(cls, username, password, new_password):
        username = username.lower()
        u = cls.auth(username, password)
        if u:
            u.set_password(new_password)
            u.refresh_key()
            return u

    @classmethod
    def auth(cls, username, password):
        username = username.lower()
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
        username = username.lower()
        session = DBSession()
        return session.query(cls).filter(cls.username==username).count() > 0

    @classmethod
    def get_by_key(cls, key):
        session = DBSession()
        if py_ver == 2:
            the_key = (key or b'').encode('utf-8')
        else:
            the_key = str(key or b'', 'utf-8')
        return session.query(cls).filter(cls.key==the_key).first()

    @classmethod
    def get_by_username(cls, username):
        username = username.lower()
        session = DBSession()
        return session.query(cls).filter(cls.username==username).first()

    @classmethod
    def count(cls):
        session = DBSession()
        return session.query(cls).filter(cls.state>0).count()
