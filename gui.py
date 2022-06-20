import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
screen = app.screens()[0]
# dpi = screen.physicalDotsPerInch()
dpi = 100

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gif_gen.gif_main
import mergemap
from model.map import *
from model.update import Update
from utils import *
from model.SETTINGS import *
from poll_observe import *


def gui():
    global generalMap
    isDrawingBlocker = False
    iteration = 0

    x, z = 0, 0

    height, width = window_size
    frames = [[[WALL_COLOR for x in range(width + 1)] for z in range(height + 1)] for _ in range(n_layers)]
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
            for cid in k_handlers:
                canvas.mpl_disconnect(cid)

            print("FOREVERLOOP, ONLY GOD CAN HELP US")
            while (True):
                update()
                redraw()

        if not isDrawingBlocker:
            print("redrawing")
            redraw()

    def update():
        if observing:
            observe()
        Update(generalMap)
        nonlocal iteration
        iteration += 1

    root = tk.Tk()
    root.wm_title("cracow smoker")
    fig = plt.Figure(figsize=(float(width / (dpi * 1.15)), float(height / (dpi * 1.15))),
                     dpi=dpi)  # no idea why its not fullwindow image with just *1, but somehow 1.15 gave the best results
    # fig.patch.set_facecolor('xkcd:mint green')
    print(fig.get_figwidth(), fig.get_figheight())
    _fr = generalMap[cur_layer].getPixels(x, z, x + width, z + height)

    if observing and draw_observers:
        drawObservers(_fr)

    _fr = np.uint8(_fr)

    printIfDBG(("   framesstart", type(_fr), _fr.shape), TIMEPRINT)
    image = fig.figimage(Image.fromarray(_fr, mode="RGBA"))
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    def redraw():
        # clears the screen and
        # if multiple layers flag is true ...
        # draws (and saves if gif creation is enabled)
        # all layers from the lowest to the one active
        # all with alpha  .5

        # otherwise
        # draws only one active layer without any global alpha

        printIfDBG(("start", timeCheck()), TIMEPRINT)
        nonlocal isDrawingBlocker  # if new image is being drawn, block any incoming redraw commands
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

                # observers are not implemented fully, so it has no impact
                if observing and draw_observers:
                    drawObservers(frames[_i])

                frames[_i] = np.uint8(frames[_i])
                printIfDBG(("   uinted", timeCheck()), TIMEPRINT)
                printIfDBG(("   frames", type(frames[_i]), frames[_i].shape), TIMEPRINT)
                image = Image.fromarray(frames[_i], mode="RGBA")
                printIfDBG(("   imaged", timeCheck()), TIMEPRINT)
                if gif_create:
                    _pth = gif_path + "\\" + str(_i) + "\\" + str(iteration) + ".png"
                    image.save(_pth)
                    printIfDBG(("saved img", _pth), TIMEPRINT)
                fig.figimage(image, alpha=0.5)
                print("drawed")
        else:
            _i = cur_layer
            generalMap[_i].getPixelsToArray(x, z, x + width, z + height, frames, _i, moved)
            printIfDBG(("   gotPixels", timeCheck()), TIMEPRINT)
            if observing and draw_observers:
                drawObservers(frames[_i])
            frames[_i] = np.uint8(frames[_i])
            printIfDBG(("   uinted", timeCheck()), TIMEPRINT)
            image = Image.fromarray(frames[_i], mode="RGBA")
            printIfDBG(("   imaged", timeCheck()), TIMEPRINT)

            fig.figimage(image)
            printIfDBG(("   drawed", timeCheck()), TIMEPRINT)

        if gif_create:
            fig.savefig(gif_path + "\\full\\" + str(iteration) + ".png")
        printIfDBG(("   drawed", timeCheck()), TIMEPRINT)
        printIfDBG(("frames shape:", frames.shape), TIMEPRINT)
        canvas.draw()
        isDrawingBlocker = False
        moved = False

    k_handlers = []
    k_handlers.append(canvas.mpl_connect(
        "key_press_event", handle_keys
    ))
    k_handlers.append(canvas.mpl_connect("key_press_event", key_press_handler))
    button_quit = tk.Button(master=root, text="Quit", command=root.quit)

    button_quit.pack(side=tk.BOTTOM)
    # slider_update.pack(side=tk.BOTTOM)
    # toolbar.pack(side=tk.BOTTOM, fill=tk.X)
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


# Main function
def run():
    if observing:
        observeInit()
    if gif_create:
        global gif_path
        gif_path = gif_gen.gif_main.gifMain()
    print("started")
    load()
    print("loadeddata")
    gui()


run()
