def frange(start, stop, inc):
    i = start
    while i < stop:
        yield i
        i += inc

def linear_interp(self, m1, m2, amnt):
    out = []
    for i in range(len(m1)):
        out.append((1.0 - amnt)*m1[i] + amnt*m2[i])
    return out