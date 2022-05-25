import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def toarray(file):
    DATA = []
    counter = 0
    while file:
        line = file.readline()
        if line == "": break
        val = [float(x) for x in line.split(';')]
        DATA.append(val)

    return np.array(DATA)

if __name__ == '__main__':
    # file = open('testPradnik.csv', "r")
    file = open('testCentrum.csv', "r")
    DATA = toarray(file)
    plt.imshow(DATA, cmap='cool', interpolation='nearest')
    plt.title("2-D Heat Map")
    plt.show()
    file.close()