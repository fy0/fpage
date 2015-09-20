# coding:utf-8

from model import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean


class Test(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    test = Column(String)

    __tablename__ = 'test'
