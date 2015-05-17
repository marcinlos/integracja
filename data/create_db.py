#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from model import Base

def get_engine(name):
    return create_engine('sqlite:///{}'.format(name), echo=True)

e = get_engine('database')
Base.metadata.create_all(e)

