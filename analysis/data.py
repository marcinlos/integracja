
from attributes import group_by, sorted_by


def as_list(data):
    if isinstance(data, list):
        return data
    else:
        return list(data)

class DataSet(object):
    def __init__(self, data):
        self.data = as_list(data)

    def group_by(self, criterion):
        sets = group_by(self.data, criterion)
        return GroupedData({k: DataSet(vals) for k, vals in sets.iteritems()})

    def filter(self, criterion):
        return DataSet(filter(criterion, self.data))

    def order_by(self, criterion, reverse=False):
        return DataSet(sorted_by(self.data, criterion, reverse))

    def with_attr(self, attr):
        def has_it(row): return getattr(row, attr) is not None
        return self.filter(has_it)

    def map(self, f):
        return DataSet(map(f, self.data))

    def reverse(self):
        return DataSet(reversed(self.data))

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, n):
        return self.data[n]

    def __eq__(self, other):
        try:
            return self.data == other.data
        except AttributeError:
            return False


class GroupedData(object):
    def __init__(self, groups):
        self.groups = groups

    def map(self, f):
        return GroupedData({k: f(v) for k, v in self})

    def pairs(self):
        return DataSet(self)

    def order_by(self, *args, **kw):
        return self.pairs().order_by(*args, **kw)

    def __getitem__(self, key):
        return self.groups[key]

    def __iter__(self):
        return self.groups.iteritems()

    def __len__(self):
        return len(self.groups)
