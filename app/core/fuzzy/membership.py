def triangle(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def trapezoid(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (d - x) / (d - c)