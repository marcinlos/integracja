
import attributes as att


class Filter(object):

    def inverse(self):
        return InverseFilter(self)

    def on(self, criterion):
        return FocusedFilter(criterion, self)

    def __call__(self, item):
        raise AssertionError('Not implemented')


class PredicateFilter(Filter):
    def __init__(self, pred):
        self.pred = pred

    def __call__(self, item):
        return self.pred(item)


class InverseFilter(Filter):
    def __init__(self, wrapped_filter):
        self.filter = wrapped_filter

    def __call__(self, item):
        return not self.filter(item)

    def inverse(self):
        return self.filter


class FocusedFilter(Filter):
    def __init__(self, criterion, wrapped_filter):
        self.filter = wrapped_filter
        self.f = att.criterion_to_fun(criterion)

    def __call__(self, item):
        value = self.f(item)
        return self.filter(value)


class ValueSetFilter(Filter):
    def __init__(self, values):
        self.values = set(values)

    def __call__(self, item):
        return item in self.values

class BinOpFilter(Filter):
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

    def __combine(self, a, b):
        raise AssertionError('Abstract method')

    def __call__(self, item):
        return self.__combine(self.f1(item), self.f2(item))


class AndFilter(BinOpFilter):
    def __init__(self, f1, f2):
        super(AndFilter, self).__init__(f1, f2)

    def __combine(self, a, b):
        return a and b


class OrFilter(BinOpFilter):
    def __init__(self, f1, f2):
        super(AndFilter, self).__init__(f1, f2)

    def __combine(self, a, b):
        return a or b

def exclude_if(criterion, pred):
    return PredicateFilter(pred).on(criterion).inverse()

def exclude_values(criterion, values):
    return ValueSetFilter(values).on(criterion).inverse()

def include_only_values(criterion, values):
    return ValueSetFilter(values).on(criterion)

def exclude_sources(*sources):
    return exclude_values('source', set(sources))

def only_sources(*sources):
    return include_only_values('source', set(sources))

def __only_lethal(item):
    deaths = item.deaths_total
    return deaths is not None and deaths > 0

only_lethal = PredicateFilter(__only_lethal)
