import tkinter as tk

import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotCSV

class Cell:
    # type ->
    # -1 wall
    # [0,1] smoke
    condensation = 0

    def __init__(self, type):
        self.type = type

    def draw(self):
        if self.type == -1:
            return [255,255,255]
        else:
            return [0,0,0]



class Layer:
    def __init__(self, y_bottom, h, cells):
        self.height = h
        self.y_bottom = y_bottom
        self.cells = cells
    def getPixels(self,x_bl,z_bl,x_tr,z_tr):
        list = [[ self.cells[z][x].draw() for x in range(x_tr-x_bl)] for z in range(z_tr-z_bl)]
        arr = np.asarray(list)
        print("shape",arr.shape)
        print(arr)
        out = im.fromarray(arr, "RGB")
        #out.show()
        return out
    def wallCells(self):
        sum=0
        for _ in self.cells:
            for __ in _:
                if __.type == -1:
                    sum+=1
        return sum

def createMap(data, minheight, maxheight, n_HorizontalCubes):
    cube_h = (maxheight - minheight) / n_HorizontalCubes
    layers = []

    for i in range(n_HorizontalCubes):
        layerd = np.array([[ Cell(-1 if data[row][col] >= i*cube_h+minheight else 0 ) for col in range(len(data[row]))] for row in range(len(data))])
        layers.append(Layer(i*cube_h+minheight,cube_h,layerd))
    return layers


def gui():
    root = tk.Tk(screenName="loremipsows")
    frame = tk.Frame(root, borderwidth=10)
    frame.grid()
    tk.Label(frame, text="siema eniu").grid(column=0, row=0)
    tk.Button(frame, text="Exit", command=root.destroy).grid(column=1, row=0)

    root.mainloop()


file = open('testPradnik.csv', "r")
# file = open('testCentrum.csv', "r")
DATA = plotCSV.toarray(file)
file.close()
print(DATA.shape)
map = createMap(DATA,np.amin(DATA),np.amax(DATA),4)
for m in map:
    print("walls:",m.wallCells())
    print("all",m.cells.shape[0]*m.cells.shape[1])
    #print(m.cells)
    imager = m.getPixels(0, 0, 500, 500)
    print(imager)
    plt.imshow(imager)
    plt.title("2-D Heat Map")
    plt.show()



