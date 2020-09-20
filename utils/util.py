def frange(start, stop, inc):
    i = start
    while i < stop:
        yield i
        i += inc

def linear_interp(m1, m2, amnt):
    out = []
    for i in range(len(m1)):
        out.append((1.0 - amnt)*m1[i] + amnt*m2[i])
    return out

def replace_with_all(string, in_out_tuples):
    temp = string
    for in_s, out_s in in_out_tuples:
        temp = temp.replace(in_s, out_s)
    return temp