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

import gif_gen.gif_main
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
    isDrawingBlocker = False
    iteration = 0

    x, z = 0, 0

    height, width = window_size
    frames = [[[WALL_COLOR for x in range(width)] for z in range(height)] for _ in range(n_layers)]
    frames = np.uint8(frames)
    frames = np.array(frames)

    n = len(generalMap)
    cur_layer = 2
    max_x = len(generalMap[cur_layer].cells[0]) - 1
    max_z = len(generalMap[cur_layer].cells) - 1
    moved = True

    def switch(_):
        nonlocal cur_layer
        cur_layer += _
        if cur_layer < 0:
            cur_layer += n
        cur_layer %= n
        print("switched to layer:", cur_layer)

    move_keys = ["left", "right", "up", "down"]

    def handle_keys(event):
        nonlocal x
        nonlocal z
        nonlocal moved
        key = event.key.lower()
        jump = 5
        if key == 'm':
            switch(1)
        if key == 'n':
            switch(-1)
        if key in move_keys:
            moved = True
            if key == "left":
                x -= jump
                if x < 0:
                    x = 0
            if key == "right":
                x += jump
                if x + width > max_x:
                    x = max_x - width
            if key == "down":
                z += jump
                if z + height > max_z:
                    z = max_z - height
            if key == "up":
                z -= jump
                if z < 0:
                    z = 0
            print(event.key)
            print(x, z)
        if key == 'u':
            print("trying to update")
            update()
        if key == 's':
            for  cid in k_handlers:
                canvas.mpl_disconnect(cid)

            print("FOREVERLOOP, ONLY GOD CAN HELP US")
            while(True):
                update()
                redraw()

        if not isDrawingBlocker:
            print("redrawing")
            redraw()

    def update():
        Update(generalMap)
        nonlocal iteration
        iteration += 1

    root = tk.Tk()
    root.wm_title("tytul")
    fig = plt.Figure(figsize=(5, 5), dpi=100)
    _fr =np.uint8(    generalMap[cur_layer].getPixels(x, z, x + width, z + height))
    printIfDBG(("   framesstart", type(_fr), _fr.shape), TIMEPRINT)
    image = fig.figimage( Image.fromarray(_fr, mode="RGBA"))

    #generalMap[cur_layer].getPixelsToArray(x, z, x + width, z + height,frames,cur_layer,True)
    #frames[cur_layer] = np.uint8(frames[cur_layer])
    #image = fig.figimage( Image.fromarray(frames[cur_layer], mode="RGBA"))
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    def redraw():
        printIfDBG(("start", timeCheck()), TIMEPRINT)
        nonlocal isDrawingBlocker
        nonlocal frames
        nonlocal image
        nonlocal x
        nonlocal z
        nonlocal moved
        isDrawingBlocker = True

        fig.clf()
        printIfDBG(("scrClr", timeCheck()), TIMEPRINT)

        threads = []
        if multiple_layers_draw:
            for _i in range(cur_layer):
                threads.append(threading.Thread(target=generalMap[_i].getPixelsToArray,
                                                args=(x, z, x + width, z + height, frames, _i, moved)))
                threads[-1].start()
            for _i in range(cur_layer):
                threads[_i].join()

            for _i in range(cur_layer):
                printIfDBG(("   gotPixels", timeCheck()), TIMEPRINT)
                frames[_i] = np.uint8(frames[_i])
                printIfDBG(("   uinted", timeCheck()), TIMEPRINT)
                printIfDBG(("   frames", type(frames[_i]), frames[_i].shape), TIMEPRINT)
                image = Image.fromarray(frames[_i], mode="RGBA")
                printIfDBG(("   imaged", timeCheck()), TIMEPRINT)
                image.save(gif_path+"\\"+str(_i)+"\\"+str(iteration)+".png")
                fig.figimage(image, alpha=0.5)
                print("drawed")
        else:
            _i = cur_layer
            generalMap[_i].getPixelsToArray(x, z, x + width, z + height, frames, _i, moved)
            printIfDBG(("   gotPixels", timeCheck()), TIMEPRINT)
            frames[_i] = np.uint8(frames[_i])
            printIfDBG(("   uinted", timeCheck()), TIMEPRINT)
            image = Image.fromarray(frames[_i], mode="RGBA")
            printIfDBG(("   imaged", timeCheck()), TIMEPRINT)
            fig.figimage(image)
            printIfDBG(("   drawed", timeCheck()), TIMEPRINT)

        fig.savefig(gif_path + "\\full\\" + str(iteration) + ".png")
        printIfDBG(("   drawed", timeCheck()), TIMEPRINT)
        printIfDBG( ("frames shape:", frames.shape ), TIMEPRINT)
        canvas.draw()
        isDrawingBlocker = False
        moved = False

    # pack_toolbar=False will make it easier to use a layout manager later on.
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()
    k_handlers = []
    k_handlers.append(canvas.mpl_connect(
        "key_press_event", handle_keys
    ))
    k_handlers.append(canvas.mpl_connect("key_press_event", key_press_handler))
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
    print("merged data as :", DATA.shape)

    global generalMap
    print("creating map")
    generalMap = createMap(DATA, np.amin(DATA), np.amax(DATA), n_layers)


def run():
    if gif_create:
        global gif_path
        gif_path = gif_gen.gif_main.gifMain()
    print("started")
    load()
    print("loadeddata")
    gui()


run()
