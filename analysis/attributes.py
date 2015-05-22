import operator
from collections import defaultdict


def __make_chained_attrgetter(path):
    parts = path.split('.')
    funs = map(operator.attrgetter, parts)
    return compose(*funs)


def __compose2(f, g):
    return lambda x: g(f(x))

def compose(*funs):
    if not funs:
        return lambda x: x
    else:
        return reduce(__compose2, funs)

def criterion_to_fun(criterion):
    if isinstance(criterion, str):
        return __make_chained_attrgetter(criterion)
    elif isinstance(criterion, (int, long)):
        return operator.itemgetter(criterion)
    elif hasattr(criterion, '__call__'):
        return criterion
    else:
        raise ValueError('Not an attribute, index nor callable object', criterion)

def group_by_fun(data, fun):
    groups = defaultdict(list)
    for item in data:
        groups[fun(item)].append(item)
    return groups

def group_by(data, criterion):
    fun = criterion_to_fun(criterion)
    return group_by_fun(data, fun)

def with_attr(data, attr):
    fun = operator.attrgetter(attr)
    return [item for item in data if fun(item) is not None]

def sort_by(data, criterion, reverse=False):
    fun = criterion_to_fun(criterion)
    data.sort(key=fun, reverse=reverse)

def sorted_by(data, criterion, reverse=False):
    data_copy = data[:]
    sort_by(data_copy, criterion, reverse=reverse)
    return data_copy
