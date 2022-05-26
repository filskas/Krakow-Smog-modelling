import os
import numpy as np
import plotCSV
import matplotlib.pyplot as plt

grid = [
    ["D-b-3-3", "D-b-3-4", "D-b-4-3", "D-b-4-4"],
    ["D-d-1-1", "D-d-1-2", "D-d-2-1", "D-d-2-2"],
    ["D-d-1-3", "D-d-1-4", "D-d-2-3", "D-d-2-4"],
    ["D-d-3-1", "D-d-3-2", "D-d-4-1", "D-d-4-2"],
    ["D-d-3-3", "D-d-3-4", "D-d-4-3", "D-d-4-4"],
]


def createFullMap():
    T = []
    test = []
    for i in range(len(grid)):
        row = []
        testrow = []
        for j in range(len(grid[0])):
            name = ''
            for file in os.listdir(os.getcwd()):
                if file[8:-4] == grid[i][j]:
                    f = open(file)
                    row.append(plotCSV.toarray(f)[1:-1, 1:-1])
                    f.close()
                    testrow.append(file[8:-4])
        T.append(row)
        test.append(testrow)
    if test != grid: return -1
    result = []
    for i in range(len(grid)):
        row = T[i][0]
        for j in range(1, len(grid[0])):
            row = np.concatenate((row, T[i][j]), axis=1)
        if i == 0:
            result = row
        else:
            result = np.concatenate((result, row), axis=0)

    return result


# DATA = createFullMap()
#
# plt.imshow(DATA, cmap='cool', interpolation='nearest')
# plt.title("2-D Heat Map")
# plt.show()
