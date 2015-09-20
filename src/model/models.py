# coding:utf-8

from model import BaseModel, db
import model.test
import model.user

BaseModel.metadata.create_all(db)
