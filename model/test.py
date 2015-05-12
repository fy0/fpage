# coding:utf-8

from model import Model
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean


class Test(Model):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test = Column(String)

