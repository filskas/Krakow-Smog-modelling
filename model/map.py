import threading

from model.SETTINGS import *
from model.cube import *
from model.layer import *
import numpy as np
import random
from streets import toArray

def createMap(data, minheight, maxheight, n_HorizontalCubes):
    cube_h = (maxheight - minheight) / n_HorizontalCubes
    layers = [[] for _ in range(n_HorizontalCubes)]
    relative_neighbors = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]

    def generate_layer(i):
        #print("data len", len(data), " data[0] len",len(data[i]))
        layerd = np.array([[Cube(Type.WALL if data[row][col] >= i * cube_h + minheight else Type.AIR,
                                 (row, col, i),
                                 (cube_h, cube_h, cube_h), 0.0, Velocity(*wall_velocity)
                                 if data[row][col] >= i * cube_h + minheight else Velocity(*air_velocity), 0)
                            for col in range(len(data[row]))] for row in range(len(data))])
        # calculating nextToIterate
        for y in range(len(layerd)):
            nextCube = None
            for x in reversed(range(len(layerd[y]))):
                layerd[y][x].nextAir = nextCube
                if layerd[y][x].type == Type.AIR:
                    nextCube = layerd[y][x]

        print("created Layer number:",i,"/",n_HorizontalCubes-1)
        layers[i] = Layer(i * cube_h + minheight, cube_h, layerd)

    threads = []
    for _i in range(n_HorizontalCubes):
            threads.append(
                threading.Thread(target=generate_layer, args=[_i]))
            threads[-1].start()
    for _i in range(n_layers):
            threads[_i].join()

    print(layers)

    streetmap = toArray()
    for y in range(len(layers[0].cells)):
        for x in range(len(layers[0].cells[y])):
            if streetmap[y][x] != 0:
                for z in range(len(layers)):
                    if layers[z].cells[y][x].type == Type.AIR:
                        layers[z].cells[y][x].isStreet = True
                        break

    for z in range(len(layers)):
        for y in range(len(layers[z].cells)):
            for x in range(len(layers[z].cells[y])):
                for rel in relative_neighbors:
                    if not( n_HorizontalCubes>z+rel[2]>=0 and len(layers[z].cells)>y+rel[1]>=0 and len(layers[z].cells[y])>x+rel[0]>=0):
                        layers[z].cells[y][x].type = Type.WALL

    for z in range(len(layers)):
        for y in range(len(layers[z].cells)):
            for x in range(len(layers[z].cells[y])):
                for rel in relative_neighbors:
                    if x == 0 or y == 0 or x == len(layers[z].cells[y])-1 or y == len(layers[z].cells)-1:
                        layers[z].cells[y][x].isBorder = True

    for y in range(len(layers[n_layers-1].cells)):
        for x in range(len(layers[n_layers-1].cells[y])):
            layers[n_layers-1].cells[y][x].isBorder = True

    for z in range(len(layers)):
        for y in range(len(layers[z].cells)):
            for x in range(len(layers[z].cells[y])):
                for rel in relative_neighbors:
                    if n_HorizontalCubes>z+rel[2]>=0 and len(layers[z].cells)>y+rel[1]>=0 and len(layers[z].cells[y])>x+rel[0]>=0:
                        layers[z].cells[y][x].add_neighbor(layers[z+rel[2]].cells[y+rel[1]][x+rel[0]], rel)


    return layers