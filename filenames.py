import preprocess
import os
from os import path

for file in os.listdir("/terrainmodelKrakowSample/DATA"):
    path = os.path.join("/terrainmodelKrakowSample/DATA",file)
    print(path)
    preprocess.readtable(path)

