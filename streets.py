import folium
import matplotlib.pyplot as plt
import shapely.affinity
import shapely.geometry
from geopandas import GeoDataFrame
from shapely.geometry import Polygon
import numpy as np
from PIL import Image
from mergemap import createFullMap
from matplotlib.colors import ListedColormap


def getRoadsData(path='gis_osm_roads_free_1.shp'):
    data = []
    shp_path = path
    roads = GeoDataFrame.from_file(shp_path, encoding='utf-8',rows=10)
    print(roads.keys())

    center = [50.0521, 19.8875]
    top = 50.1042
    bottom = 50.0000
    left = 19.8750
    right = 20.0002


    rectangular = Polygon([(left, bottom), (right,bottom), (right,top), (left,top)])
    ellipse = shapely.affinity.scale(rectangular)

    ellipse_map = folium.Map(location=center, zoom_start=10, tiles='CartoDB positron')

    folium.PolyLine(list([c[::-1] for c in ellipse.exterior.coords])).add_to(ellipse_map)

    roads = roads.loc[roads['geometry'].apply(lambda g: ellipse.contains(g))].copy()


    def plot_and_save(linewidth,path,dpi=1000):
        nonlocal data
        roads.plot(linewidth=linewidth)
        t = plt.subplot()

        ratio = 1.5
        x_left, x_right = t.get_xlim()
        y_low, y_high = t.get_ylim()
        t.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)


        plt.savefig(path, dpi=dpi)
        plt.show()


    plot_and_save(0.05,'cracowstrrets3.png',dpi=1000)
    return data



def toArray(path="cracowstrrets.png"):
    map = createFullMap()
    newsize = (len(map[0]), len(map))
    im = Image.open(path)
    pix = im.load()

    im_r = im.resize(newsize)
    im_r = im_r.getdata()
    im_r = np.array(im_r)

    im_r = [0
            if im_r[i][0] > 240
               and im_r[i][1] > 240
               and im_r[i][2] > 240
            else 1
            for i in range(len(im_r))
            ]

    im_r = np.array(im_r)
    im_r = np.reshape(im_r,(newsize[1],newsize[0]))

    # im_r.save('cracowstreetsreduced.png')


    return im_r



def plot():
    map = createFullMap()
    roads = toArray()

    plt.imshow(map,cmap='Blues_r', interpolation='nearest')
    cmap = ListedColormap([[1.0, 1.0, 0.0, 0.0],[1.0, 1.0, 0.0, 0.5]])
    plt.imshow(roads,cmap=cmap, interpolation='nearest')
    plt.show()





if __name__ == '__main__':
    plot()