
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
    name = re.sub('[,.-_]', '', name)
    name = re.sub('inc', '', name)
    return name

def is_roman_numeral(string):
    digits = ["M", "D", "C", "L", "X", "V", "I"]
    return all(c in digits for c in string)

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

def damerau_levenshtein(a, b):
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
            opts = [
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + e
            ]
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                opts.append(d[i - 2][j - 2] + 1)
            d[i][j] = min(*opts)
    return d[n][m]

def best_match(s, strings):
    d = 10000
    best = None
    s = s.lower()
    for m in strings:
        dist = damerau_levenshtein(s, m.lower())
        # print u'For {} and {}: {}'.format(s, m.lower(), dist)
        if dist < d:
            d = dist
            best = m
    return best, d

def clean_string(name):
    if name and name != '?':
        return name.strip()

