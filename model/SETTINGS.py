from model.velocity import Velocity

air_velocity = Velocity(2, 5, 2, 5, 0, 0)
wall_velocity = Velocity(0, 0, 0, 0, 0, 0)
pollution_rate = 0.2
generalMap = []
#isDrawingBlocker = False
window_size = (500, 500)
n_layers = 5

gif_create=True
gif_path= None

#DRAWING
multiple_layers_draw = True

#DEBUG
TIMEPRINT = True

#MODE
#??

#POLLUTION
observing= False
draw_observers =False
pollution_observers = [(250,400)]
observe_dir = None
