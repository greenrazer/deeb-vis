def frange(start, stop, inc):
    i = start
    while i < stop:
        yield i
        i += inc