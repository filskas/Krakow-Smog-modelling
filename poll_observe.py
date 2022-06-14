import csv
from datetime import datetime
from os.path import isdir

from model.SETTINGS import *
import os


def observeInit():
    rootPath, program = os.path.split(os.path.realpath(__file__))
    if not isdir(rootPath + "\\observe_data"):
        os.mkdir(rootPath + "\\observe_data")
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
    os.mkdir(rootPath + "\\observe_data\\" + dt_string)
    return rootPath + "\\observe_data\\" + dt_string


def observe():
    if observe_dir is not None:
        for obs in pollution_observers:
            x, y = obs
            row = []
            for l in range(len(generalMap.layers)):
                row.append(generalMap.layers[l].cells[y][x].pollution_rate)

            with open(observe_dir + "\\" + str(x) + str(y) + str(y)+".csv", 'a+') as f:
                # create the csv writer
                writer = csv.writer(f)
                # write a row to the csv file
                writer.writerow(row)

def drawObservers(arr):
    for obs in pollution_observers:
        x, y = obs
        arr[y][x+1] = [0,255,0,255]
        arr[y+1][x] = [0,255,0,255]
        arr[y][x-1] = [0,255,0,255]
        arr[y-1][x] = [0,255,0,255]
        arr[y-1][x-1] = [0,255,0,255]
