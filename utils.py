import time
from threading import Thread

times = [time.time()]


def timeCheck():
    t = time.time()
    t_1 = times[-1]
    times.append(t)
    return t - t_1


def isWithin(coord, rbl, rtr):
    x, y, z = coord
    return rtr[0] > x >= rbl[0] and rtr[1] > y >= rbl[1]
Thread()
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return

