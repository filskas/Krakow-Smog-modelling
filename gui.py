import tkinter as tk
# from pyglet.window import key

import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotCSV
import mergemap
from model.Cube import Cube
from model.Velocity import Velocity
from model.Type import Type

air_velocity = Velocity(2, 5, 2, 5, 0, 0)
wall_velocity = Velocity(0, 0, 0, 0, 0, 0)
pollution_rate = 0.2

generalMap=[]

class Cell:
    # type ->
    # -1 wall
    # [0,1] smoke
    condensation = 0

    def __init__(self, type):
        self.type = type

    def draw(self):
        if self.type == -1:
            return 0
        else:
            return 1



class Layer:
    def __init__(self, y_bottom, h, cells):
        self.height = h
        self.y_bottom = y_bottom
        self.cells = cells
    def getPixels(self,x_bl,z_bl,x_tr,z_tr):
        list = [[ 0 for x in range(x_tr-x_bl)] for z in range(z_tr-z_bl)]
#
        list = np.asarray(list)
        for z in range(z_tr-z_bl):
            for x in range(x_tr - x_bl):
                list[z][x]= self.cells[z_bl+z][x_bl+x].draw()
        #print(arr.shape)#print("shape",arr.shape)
        #print(arr)
        #out = im.fromarray(arr, "L")
        #out.show()
        return list
    def wallCells(self):
        sum=0
        for _ in self.cells:
            for __ in _:
                if __.type == -1:
                    sum+=1
        return sum


def coordinates_within_bounds(point, bound1, bound2, bound3):
    return bound1[0] <= point[0] <= bound1[1] and bound2[0] <= point[1] <= bound2[1] and bound3[0] <= point[2] <= bound3[1]


def createMap(data, minheight, maxheight, n_HorizontalCubes):
    cube_h = (maxheight - minheight) / n_HorizontalCubes
    layers = []
    relative_neighbors = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    for i in range(n_HorizontalCubes):
        layerd = np.array([[Cube(Type.AIR if data[row][col] >= i*cube_h+minheight else Type.WALL, (row, col, i),
                                 (cube_h, cube_h, cube_h), pollution_rate, air_velocity
                                 if data[row][col] >= i*cube_h+minheight else wall_velocity, 0)
                            for col in range(len(data[row]))] for row in range(len(data))])
        layers.append(Layer(i*cube_h+minheight,cube_h,layerd))
    # for i in range(n_HorizontalCubes):
    #     for layerd in layers[i].cells:
    #         for row in layerd:
    #             for elem in row:
    #                 elem.

    return layers


def gui():
    global generalMap
    x,z= 0,0

    height,width = 500,500

    n = len(generalMap)
    cur_layer = 0
    max_x =len(generalMap[cur_layer].cells[0])-1
    max_z = len(generalMap[cur_layer].cells)-1
    print(max_x, max_z)

    def switch(_):
        nonlocal cur_layer
        cur_layer +=_
        if cur_layer<0:
            cur_layer+=n
        cur_layer %=n
        print("switched to layer:",cur_layer)


    def handle_keys(event):
        nonlocal x
        nonlocal z
        jump=5
        if event.key == 'm':
            switch(1)
        if event.key == 'n':
            switch(-1)
        if event.key == "left":
            x-=jump
            if x<0:
                x=0
        if event.key == "right":
            x += jump
            if x+width > max_x:
                x = max_x-width
        if event.key == "down":
            z += jump
            if z+height > max_z:
                z = max_z-height
        if event.key == "up":
            z -= jump
            if z < 0:
                z = 0
        print(type(event.key))
        print(event.key)

        print(x,z)
        redraw()

    root = tk.Tk()
    root.wm_title("tytul")
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    image = fig.figimage(generalMap[cur_layer].getPixels(x, z, x + width, z + height))
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    def redraw():
        nonlocal image
        nonlocal x
        nonlocal z
        fig.clf()
        newframe =generalMap[cur_layer].getPixels(x, z, x+width, z+height)
        image = fig.figimage(newframe)
        canvas.draw()


    # pack_toolbar=False will make it easier to use a layout manager later on.
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()

    canvas.mpl_connect(
        "key_press_event", handle_keys
    )
    canvas.mpl_connect("key_press_event", key_press_handler)

    button_quit = tk.Button(master=root, text="Quit", command=root.quit)

    button_quit.pack(side=tk.BOTTOM)
    #slider_update.pack(side=tk.BOTTOM)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    tk.mainloop()
"""
    frame = tk.Frame(root, borderwidth=10)
    frame.grid()
    tk.Label(frame, text="siema eniu").grid(column=0, row=0)
    tk.Button(frame, text="Exit", command=root.destroy).grid(column=1, row=0)
"""


def load():
    DATA = mergemap.createFullMap()
    global generalMap
    generalMap = createMap(DATA, np.amin(DATA), np.amax(DATA), 4)

def run():
    load()
    gui()
run()
