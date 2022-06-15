from model.velocity import Velocity

wind = [1]
wind_directions = [(0,1,0)]
air_velocity = 0, wind[0], 0, 0, 0.5, 0
wall_velocity = 0, 0, 0, 0, 0.5, 0

pollution_rate = 0.2
car_vertical_blast = 0.1
street_generation_rate = 0.15
street_generation_diff = 20
generalMap = []
isDrawingBlocker = False
window_size = (719, 555)
n_layers = 6

gif_create=True
gif_path= None

#DRAWING
multiple_layers_draw = True
drawing_precision = 10

#DEBUG
TIMEPRINT = True

#MODE

#POLLUTION
observing= False
draw_observers =False
pollution_observers = [(250,400)]
observe_dir = None
