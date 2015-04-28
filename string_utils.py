
import re

def unicodize(data, encoding='latin-1'):
    if encoding is None:
        f = unicode
    else:
        f = lambda s: s.decode(encoding)
    return {k: f(v) for k, v in data.items()}

def orNone(string):
    return string if string else None

def intOrNone(string):
    try:
        return int(string)
    except:
        pass

def flatten_name(name):
    name = name.lower()
    name = re.sub(r'\s+', '', name)
    name = re.sub('[,.]', '', name)
    name = re.sub('inc', '', name)
    return name

def levenshtein(a, b):
    n = len(a)
    m = len(b)
    d = [[0] * (m + 1) for _ in xrange(n + 1)]

    for i in xrange(1, n + 1):
        d[i][0] = i

    for j in xrange(1, m + 1):
        d[0][j] = j

    for i in xrange(1, n + 1):
        for j in xrange(1, m + 1):
            e = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + e)
    return d[n][m]

