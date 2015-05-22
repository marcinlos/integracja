#!/usr/bin/env python
# encoding: utf-8

import sqlalchemy
from sqlalchemy import orm
from data.model import Event
import numpy as np
import matplotlib.pyplot as plt
import calendar
from analysis.data import DataSet

def get_data(path):
    engine = sqlalchemy.create_engine('sqlite:///' + path)
    session_factory = orm.sessionmaker(engine)
    session = session_factory()
    items = session.query(Event).all()
    session.close()
    return DataSet(items)

def monthly(data):
    by_month = data.group_by('date.month')

    fig, ax = plt.subplots(figsize=(6, 4))
    xs = np.arange(1, 13)
    width = 0.35

    ax.set_xticks(xs + width)
    ax.set_xticklabels(calendar.month_name[1:], rotation=90)

    values = [len(by_month[i]) for i in xs]
    ax.bar(xs, values)

    plt.tight_layout(pad=0.25)
    fig.savefig('summary.png')


def yearly_with_months(data, out):

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlabel('year')
    total = []

    base = 1920
    years = range(base, 2016)
    n = len(years)

    data = data.filter(lambda d: 1920 <= d.date.year < 2015)
    by_month = data.group_by('date.month')
    for _, es in by_month:
        pairs = es.group_by('date.year').map(len).pairs().order_by(0)
        vals = [0] * n
        for year, count in pairs:
            vals[year - base] = count

        total.append(vals)

    for i in xrange(n):
        N = sum(t[i] for t in total)
        if N > 0:
            for t in total:
                t[i] = t[i] / float(N)

    stack = np.row_stack(total)
    ax.stackplot(years, stack)
    ax.set_ylim(0, 1)

    ax.legend(loc='upper left', fontsize=10)
    plt.tight_layout(pad=0.25)
    fig.savefig(out + '.png')

def yearly(data, out):
    pairs = data.group_by('date.year').map(len).pairs().order_by(0)
    years, values = zip(*pairs)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlabel('year')
    ax.plot(years, values)

    plt.tight_layout(pad=0.25)
    fig.savefig(out + '.png')

def countries(data, out):
    pairs = data.with_attr('country').group_by('country').map(len).pairs().order_by(1, reverse=True)

    n = 15
    cs, values = zip(*pairs[:n])

    fig, ax = plt.subplots(figsize=(6, 4))
    xs = np.arange(n)
    width = 0.35

    ax.set_xticks(xs + width)
    ax.set_xticklabels(cs, rotation=90)

    ax.bar(xs, values)

    plt.tight_layout(pad=0.25)
    fig.savefig(out + '.png')

if __name__ == '__main__':
    data = get_data('database').with_attr('date')
    data_no_ntsb = data.filter(lambda d: d.source != 'ntsb')
    monthly(data)
    yearly(data, 'years')
    yearly(data_no_ntsb, 'year_no_ntsb')
    yearly_with_months(data, 'years_months')
    yearly_with_months(data_no_ntsb, 'years_months_no_ntsb')
    countries(data, 'countries')
    countries(data_no_ntsb, 'countries_no_ntsb')


