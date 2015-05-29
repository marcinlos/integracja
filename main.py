#!/usr/bin/env python
# encoding: utf-8

import sqlalchemy
from sqlalchemy import orm
from data.model import Event
from analysis import DataSet
import reports as r
import analysis.filters as flt

def get_data(path):
    engine = sqlalchemy.create_engine('sqlite:///' + path)
    session_factory = orm.sessionmaker(engine)
    session = session_factory()
    items = session.query(Event).all()
    session.close()
    return DataSet(items)

if __name__ == '__main__':
    data = get_data('database').with_attr('date')

    filters = [
        flt.exclude_sources('ntsb'),
        flt.only_lethal
    ]
    rep = r.CountryReport(data, filters=filters)
    rep.show()


