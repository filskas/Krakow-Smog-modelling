import tkinter as tk
from pyglet.window import key

import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotCSV
import mergemap

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
        list = [[ self.cells[z_bl+z][x_bl+x].draw() for x in range(x_tr-x_bl)] for z in range(z_tr-z_bl)]

        arr = np.asarray(list)
        #print(arr.shape)#print("shape",arr.shape)
        #print(arr)
        #out = im.fromarray(arr, "L")
        #out.show()
        return arr
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

