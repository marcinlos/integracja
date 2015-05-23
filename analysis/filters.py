
import attributes as att

def exclude_if(criterion, pred):
    f = att.criterion_to_fun(criterion)
    def exclude(item):
        return not pred(f(item))
    return exclude

def exclude_values(criterion, values):
    def pred(v): return v in values
    return exclude_if(criterion, pred)

def include_only_values(criterion, values):
    def pred(v): return v not in values
    return exclude_if(criterion, pred)

def exclude_sources(*sources):
    return exclude_values('source', set(sources))

def only_sources(*sources):
    return include_only_values('source', set(sources))

def only_lethal(item):
    deaths = item.deaths_total
    return deaths is not None and deaths > 0