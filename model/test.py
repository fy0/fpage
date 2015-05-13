# coding:utf-8

from model import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean


class Test(BaseModel):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test = Column(String)

