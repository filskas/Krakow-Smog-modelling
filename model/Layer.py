import numpy as np


class Layer:
    def __init__(self, y_bottom, h, cells):
        self.height = h
        self.y_bottom = y_bottom
        self.cells = cells
    def getPixels(self,x_bl,z_bl,x_tr,z_tr):
        list = [[self.cells[z_bl+z][x_bl+x].draw() for x in range(x_tr - x_bl)] for z in range(z_tr - z_bl)]
        #
        list = np.array(list, dtype=object)


        """
        for z in range(z_tr-z_bl):
            for x in range(x_tr - x_bl):
                list[z][x]= self.cells[z_bl+z][x_bl+x].draw()
        replaced for inline construction above"""

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
