import tkinter as tk
# from pyglet.window import key
import random
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
from model.cube import Cube
from model.map import *
from model.velocity import Velocity
from model.type import Type
from model.layer import Layer
from model.update import Update
from utils import *
from model.SETTINGS import *


def gui():
    global generalMap
    x, z = 0, 0

    height, width = window_size

    n = len(generalMap)
    cur_layer = 2
    max_x = len(generalMap[cur_layer].cells[0]) - 1
    max_z = len(generalMap[cur_layer].cells) - 1


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
        key = event.key.lower()
        jump = 5
        if key == 'm':
            switch(1)
        if key == 'n':
            switch(-1)
        if key == "left":
            x -= jump
            if x < 0:
                x = 0
            print(event.key)
            print(x, z)
        if key == "right":
            x += jump
            if x + width > max_x:
                x = max_x - width
            print(event.key)
            print(x, z)
        if key == "down":
            z += jump
            if z + height > max_z:
                z = max_z - height
            print(event.key)
            print(x, z)
        if key == "up":
            z -= jump
            if z < 0:
                z = 0
            print(event.key)
            print(x, z)
        if key == 'u':
            print("trying to update")
            Update(generalMap)


        if not isDrawingBlocker:
            print("redrawing")
            redraw()

    root = tk.Tk()
    root.wm_title("tytul")
    fig = plt.Figure(figsize=(5, 5), dpi=100)
    image = fig.figimage(
        Image.fromarray(np.uint8(generalMap[cur_layer].getPixels(x, z, x + width, z + height)), mode="RGBA"))
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    def redraw():
        printIfDBG(("start",timeCheck()),TIMEPRINT)
        global isDrawingBlocker
        isDrawingBlocker = True
        nonlocal image
        nonlocal x
        nonlocal z
        fig.clf()
        printIfDBG(("scrClr",timeCheck()),TIMEPRINT)

        pxls = [[] for _i in range(cur_layer)]
        pxl = []
        threads= []

        if multiple_layers_draw:
                        for _i in range(cur_layer):
                            threads.append(threading.Thread( target=generalMap[_i].getPixelsToArray, args=(x, z, x + width, z + height,pxls,_i)))
                            threads[-1].start()
                        for _i in range(cur_layer):
                            threads[_i].join()
                        for _i in range(cur_layer):

                            printIfDBG(("   gotPixels", timeCheck()), TIMEPRINT)
                            pxls[_i] = np.uint8(pxls[_i])
                            printIfDBG(("   uinted", timeCheck()),TIMEPRINT)
                            im = Image.fromarray(pxls[_i], mode="RGBA")
                            printIfDBG(("   imaged", timeCheck()),TIMEPRINT)
                            fig.figimage(im, alpha=0.5)
                            print("drawed")
        else:
            _i = cur_layer
            pxls = generalMap[_i].getPixels(x, z, x + width, z + height)
            printIfDBG(("   gotPixels", timeCheck()),TIMEPRINT)
            pxls = np.uint8(pxls)
            printIfDBG(("   uinted", timeCheck()),TIMEPRINT)
            im = Image.fromarray(pxls, mode="RGBA")
            printIfDBG(("   imaged", timeCheck()),TIMEPRINT)
            fig.figimage(im)
            printIfDBG(("   drawed", timeCheck()),TIMEPRINT)

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
    print("merged data as :",DATA.shape)

    global generalMap
    print("creating map")
    generalMap = createMap(DATA, np.amin(DATA), np.amax(DATA), n_layers)


def run():
    print("started")
    load()
    print("loadeddata")
    gui()

    for i in range(5):
        Update(generalMap)


run()