# coding:utf-8

from model import BaseModel, db
import model.test

BaseModel.metadata.create_all(db)
