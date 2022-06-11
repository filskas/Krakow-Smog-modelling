import time
from threading import Thread

times = [time.time()]


def timeCheck():
    t = time.time()
    t_1 = times[-1]
    times.append(t)
    return t - t_1

def printIfDBG(msg,dbg):
    if dbg:
        print(msg)


def isWithin(coord, rbl, rtr):
    x, y, z = coord
    return rtr[0] > x >= rbl[0] and rtr[1] > y >= rbl[1]

def coordinates_within_bounds(point, bound1, bound2, bound3):
    return bound1[0] <= point[0] <= bound1[1] and bound2[0] <= point[1] <= bound2[1] and bound3[0] <= point[2] <= \
           bound3[1]
