import tkinter as tk
# from pyglet.window import key

import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotCSV
import threading
import mergemap
from model.Cube import Cube
from model.Velocity import Velocity
from model.Type import Type
from model.Layer import Layer
from utils import ThreadWithReturnValue
from model.Update import Update
import utils

air_velocity = Velocity(2, 5, 2, 5, 0, 0)
wall_velocity = Velocity(0, 0, 0, 0, 0, 0)
pollution_rate = 0.2;
generalMap = []
isDrawingBlocker = False
window_size = (500, 500)


def coordinates_within_bounds(point, bound1, bound2, bound3):
    return bound1[0] <= point[0] <= bound1[1] and bound2[0] <= point[1] <= bound2[1] and bound3[0] <= point[2] <= \
           bound3[1]


def createMap(data, minheight, maxheight, n_HorizontalCubes):
    cube_h = (maxheight - minheight) / n_HorizontalCubes
    layers = []
    relative_neighbors = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    for i in range(n_HorizontalCubes):
        layerd = np.array([[Cube(Type.WALL if data[row][col] >= i * cube_h + minheight else Type.AIR, (row, col, i),
                                 (cube_h, cube_h, cube_h), pollution_rate, air_velocity
                                 if data[row][col] >= i * cube_h + minheight else wall_velocity, 0)
                            for col in range(len(data[row]))] for row in range(len(data))])
        # calculating nextToIterate
        for y in range(len(layerd)):
            nextCube = None
            for x in reversed(range(len(layerd[y]))):
                layerd[y][x].nextAir = nextCube
                if layerd[y][x].type == Type.AIR:
                    nextCube = layerd[y][x]

        layers.append(Layer(i * cube_h + minheight, cube_h, layerd))
    # for i in range(n_HorizontalCubes):
    #     for layerd in layers[i].cells:
    #         for row in layerd:
    #             for elem in row:
    #                 elem.

    return layers


def gui():
    global generalMap
    x, z = 0, 0

    height, width = window_size

    n = len(generalMap)
    cur_layer = 2
    max_x = len(generalMap[cur_layer].cells[0]) - 1
    max_z = len(generalMap[cur_layer].cells) - 1
    print(max_x, max_z)

    def switch(_):
        nonlocal cur_layer
        cur_layer += _
        if cur_layer < 0:
            cur_layer += n
        cur_layer %= n
        print("switched to layer:", cur_layer)

    def handle_keys(event):
        nonlocal x
        nonlocal z
        jump = 5
        if event.key == 'm':
            switch(1)
        if event.key == 'n':
            switch(-1)
        if event.key == "left":
            x -= jump
            if x < 0:
                x = 0
        if event.key == "right":
            x += jump
            if x + width > max_x:
                x = max_x - width
        if event.key == "down":
            z += jump
            if z + height > max_z:
                z = max_z - height
        if event.key == "up":
            z -= jump
            if z < 0:
                z = 0
        print(type(event.key))
        print(event.key)

        print(x, z)
        if not isDrawingBlocker:
            redraw()

    root = tk.Tk()
    root.wm_title("tytul")
    fig = plt.Figure(figsize=(5, 5), dpi=100)
    image = fig.figimage(
        Image.fromarray(np.uint8(generalMap[cur_layer].getPixels(x, z, x + width, z + height)), mode="RGBA"))
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    def redraw():
        # print("start",timeCheck())
        global isDrawingBlocker
        isDrawingBlocker = True
        nonlocal image
        nonlocal x
        nonlocal z
        fig.clf()
        # print("scrClr",timeCheck())

        fig.figimage(Image.fromarray(np.uint8(generalMap[0].getPixels(x, z, x + width, z + height)), mode="RGBA"))
        # print("drawnBck",timeCheck())
        pxls =[[] for _i in range(cur_layer)]
        threads= []
        for _i in range(cur_layer):
            threads.append(threading.Thread( target=generalMap[_i].getPixelsToArray, args=(x, z, x + width, z + height,pxls,_i)))
            threads[-1].start()
        for _i in range(cur_layer):
            threads[_i].join()
            #print(pxls[_i])
        for _i in range(cur_layer):
            #pxls = generalMap[_i].getPixels(x, z, x + width, z + height)
            # print("gotPixels", timeCheck())
            pxls[_i] = np.uint8(pxls[_i])
            #  print("uinted", timeCheck())
            im = Image.fromarray(pxls[_i], mode="RGBA")
            #   print("imaged", timeCheck())
            fig.figimage(im, alpha=0.5)
            # print("drawed", timeCheck())

        # print("findraw", timeCheck())
        canvas.draw()
        isDrawingBlocker = False

    # pack_toolbar=False will make it easier to use a layout manager later on.
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()

    canvas.mpl_connect(
        "key_press_event", handle_keys
    )
    canvas.mpl_connect("key_press_event", key_press_handler)

    button_quit = tk.Button(master=root, text="Quit", command=root.quit)

    button_quit.pack(side=tk.BOTTOM)
    # slider_update.pack(side=tk.BOTTOM)
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
    print(DATA.shape)

    global generalMap
    generalMap = createMap(DATA, np.amin(DATA), np.amax(DATA), 4)


def run():
    load()
    gui()


run()
