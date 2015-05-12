# coding:utf-8

from model import Model, db
import model.test

Model.metadata.create_all(db)
