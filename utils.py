import time

times =[time.time()]
def timeCheck():
    t =time.time()
    t_1 = times[-1]
    times.append(t)
    return t-t_1