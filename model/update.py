import threading



def Update(map):
    n_layers = len(map)
    threads = []
    for _i in range(n_layers):
        threads.append(
            threading.Thread(target=map[_i].calculateUpdate, args=()))
        threads[-1].start()
    for _i in range(n_layers):
        threads[_i].join()