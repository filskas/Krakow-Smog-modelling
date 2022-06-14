import os
import random
from os.path import isdir

import imageio

import model.SETTINGS


def gifMain():
    rootPath,program =  os.path.split(os.path.realpath(__file__))
    path = rootPath+"\\gifs\\"+str(random.randint(1,10000))
    while isdir(path):
        path = str(random.randint(1, 10000))
        print("fck, path:",path," already exist, trying to find another random name...")
    print("okay, this path should be ok: ",path)
    os.mkdir(path)
    for i in range(model.SETTINGS.n_layers):
        os.mkdir(path+"\\"+str(i))
    os.mkdir(path+"\\full")

    return path

def createGif(folderNumber):
    for root, dirs, files in os.walk(".\\gifs\\"+folderNumber, topdown=False):

        images = []
        for f in files:
            if f[-3:] == "png":
                print("reading: ... ",os.path.join(root, f))
                images.append(imageio.imread(os.path.join(root, f)))
        if len(images) != 0:
            imageio.mimsave(os.path.join(root, "GIF.gif"), images)



#createGif("6974")
