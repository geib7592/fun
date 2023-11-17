def foo(a=1, b=2, c=3, d=4):
    return a + b + c + d


def bar(a=1, b=2, c=3, d=4, e=5, f=6):
    r = foo(a=a, b=b, c=c, d=d)
    return r + e + f

