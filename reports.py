
import calendar
import numpy as np
from analysis import Report


class MonthlyReport(Report):
    def __init__(self, *args, **kw):
        super(MonthlyReport, self).__init__(*args, **kw)

    def plot(self, data, fig, ax):
        by_month = data.group_by('date.month')

        xs = np.arange(1, 13)
        width = 0.35

        ax.set_xticks(xs + width)
        ax.set_xticklabels(calendar.month_name[1:], rotation=90)

        values = [len(by_month[i]) for i in xs]
        ax.bar(xs, values)


class YearlyReportWithMonths(Report):
    def __init__(self, *args, **kw):
        super(YearlyReportWithMonths, self).__init__(*args, **kw)

    @property
    def figsize(self): return (8, 4)

    def plot(self, data, fig, ax):
        ax.set_xlabel('year')
        total = []

        base = 1920
        years = range(base, 2016)
        n = len(years)

        data = data.filter(lambda d: 1920 <= d.date.year < 2015)
        by_month = data.group_by('date.month')
        for _, es in by_month:
            pairs = es.group_by('date.year').map(len).order_by(0)
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


class YearlyReport(Report):
    def __init__(self, *args, **kw):
        super(YearlyReport, self).__init__(*args, **kw)

    @property
    def figsize(self): return (8, 4)

    def plot(self, data, fig, ax):
        pairs = data.group_by('date.year').map(len).order_by(0)
        years, values = zip(*pairs)
        ax.set_xlabel('year')
        ax.plot(years, values)


class CountryReport(Report):
    def __init__(self, data, top_count=15, *args, **kw):
        super(CountryReport, self).__init__(data, *args, **kw)
        self.top_count = top_count

    def plot(self, data, fig, ax):
        pairs = data.with_attr('country').group_by('country').map(len).order_by(1, reverse=True)
        n = self.top_count
        cs, values = zip(*pairs[:n])

        xs = np.arange(n)
        width = 0.35
        ax.set_xticks(xs + width)
        ax.set_xticklabels(cs, rotation=90)

        ax.bar(xs, values)

