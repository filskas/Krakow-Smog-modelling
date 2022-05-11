import numpy as np


def toarray(file, cols, noData,newNoData):
    DATA = []
    for y in range(cols):
        line = file.readline()
        val = [float(x) for x in line.split('  ')]
        val = list(map(lambda x: x if (x != noData) else newNoData, val))
        DATA.append(val)

    return np.array(DATA)


def reduce(DATA, times, rows, cols):
    result = []
    for y in range(rows // times):
        line = []
        for x in range(cols // times):
            oldvals = []
            for i in range(y*times, y*times + times):
                for j in range(x*times, x*times + times):
                    if i < rows and j < cols:
                        oldvals.append(DATA[i][j])
            newval = sum(oldvals) / len(oldvals)
            # newval = max(oldvals)
            line.append(newval)
        result.append(line)
    return np.array(result)


def readtable(name):
    file = open(name, "r")
    cols = file.readline()
    cols = int(cols[5:])
    rows = file.readline()
    rows = int(rows[5:])
    file.readline()
    file.readline()
    cellSize = file.readline()
    cellSize = float(cellSize[8:])
    noData = file.readline()
    noData = float(noData[13:])

    newNoData = 220

    DATA = toarray(file, rows, noData,newNoData)
    print(len(DATA))
    DATA = reduce(DATA, 8, rows, cols) #redukuje np 4*4 kwadratów do jednego np. komorke 0.5x0.5 -> 2x2
    np.savetxt(
        "testPradnik.csv",
        DATA,
        delimiter=';',
        newline='\n',
        comments='#',
        encoding=None
    )
    print(len(DATA))
    file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # readtable('67255_783018_M-34-64-D-d-1-2.asc')
    readtable('67255_783003_M-34-64-D-b-4-3.asc')
