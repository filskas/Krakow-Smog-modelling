from numpy import sign
from model.type import Type
from model.velocity import Velocity, other_axes
from random import random
from random import shuffle
from model.SETTINGS import wind
from model.SETTINGS import car_vertical_blast
from model.SETTINGS import street_generation_rate
from model.SETTINGS import drawing_precision
from model.SETTINGS import street_generation_diff

def reverse_direction(direction):
    return tuple((-element for element in direction))

WALL_COLOR=[1,1,1,255]

class Cube:
    NUMBER_OF_DIMENSIONS = 3
    DIFFUSION_COEFFICIENT = 0.05
    WIND_FACTOR = 1.2 #was 1
    THRESHOLDS = (0, 0.1, 0.3, 0.6, 0.9, 1)
    GRAVITY = 0.5

    def __init__(self, type, coordinates, size, pollution_rate, velocity, pressure):
        self._type = type
        self._coordinates = coordinates
        self._size = size
        self.pollution_rate = pollution_rate
        # self.new_pollution_rate = 0
        self._velocity = velocity
        self.neighbors = dict()
        self.neighborsFromDirection = dict()
        self.pressure = pressure
        self._nextAir = None
        self._isStreet = False
        self._updated = False
        self._isBorder = False

        self._clock = 11

    @property
    def nextAir(self):
        return self._nextAir

    @nextAir.setter
    def nextAir(self, nnext):
        self._nextAir = nnext

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in [Type.WALL,Type.GROUND,Type.AIR]:
            raise ValueError("No such cube type.")
        self._type = value

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        if value is not type(tuple) or len(value) != self.NUMBER_OF_DIMENSIONS:
            raise ValueError("3D coordinates needed.")
        self._coordinates = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value is not type(tuple) or len(value) != self.NUMBER_OF_DIMENSIONS:
            raise ValueError("3D dimensions needed.")
        self._size = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if value is not type(Velocity):
            raise ValueError("Velocity object needed.")
        self._velocity = value

    def capacity(self):
        return sum([dimension for dimension in self.size])

    def add_neighbor(self, neighbor, relative_coordinates):
        self.neighbors[neighbor] = relative_coordinates
        self.neighborsFromDirection[relative_coordinates] = neighbor

    # def bounce_off(self, neighbor):
    #     if neighbor.type in (Type.WALL, Type.GROUND):
    #         for i in range(self.NUMBER_OF_DIMENSIONS):
    #             if sign(neighbor.coordinates[i] - self.coordinates[i]) == sign(self.velocity[i]):
    #                 self.velocity[i] *= -1

    def update(self):
        self._clock += 1
        self._clock = self._clock % 24
        if self.type == Type.AIR:
            self.pollute()
            # for neighbor in self.neighbors.keys():
            #     self.interact_with_neighbor(neighbor)
            list_of_keys = list(self.neighbors.keys())
            shuffle(list_of_keys)
            for neighbor in list_of_keys:
                self.interact_with_neighbor(neighbor)
            if self.pollution_rate < 0: self.pollution_rate = 0
            if self.pollution_rate > 1: self.pollution_rate = 1


    def interact_with_neighbor(self, neighbor):
        if neighbor.type in (Type.WALL, Type.GROUND):
            self.spread(neighbor)
        else:
            self.update_from_neighbor(neighbor)

    # might be too slow (one move is spread and the next is impacting the other cells)
    def spread(self, neighbor):
        if neighbor.type in (Type.WALL, Type.GROUND):
            if neighbor.isBorder:
                for v in other_axes(self.neighbors[neighbor]):
                    updated = {v: 0}
                    self.velocity.velocities.update(updated)
                self.velocity.velocities.update({self.neighbors[neighbor]: 0})
                self.pollution_rate = 0
                return
            velocity = self.velocity.velocities[self.neighbors[neighbor]]
            velocity_part = velocity // 4
            for v in other_axes(self.neighbors[neighbor]):
                updated = {v: self.velocity.velocities[v] + velocity_part}
                self.velocity.velocities.update(updated)
            self.velocity.velocities.update({self.neighbors[neighbor]: 0})

    def update_from_neighbor(self, neighbor):
        if self.neighborsFromDirection[self.neighbors[neighbor]].isBorder:
            self.pollution_rate = 0
            print("happened")
            return

        change = self.transfer_coefficient_of_pollutant_from_neighbor(neighbor) \
                               * (neighbor.pollution_rate - self.pollution_rate)
        self.pollution_rate += change
        # neighbor.pollution_rate -= change
        self.neighborsFromDirection[self.neighbors[neighbor]].pollution_rate -= change
        # self.neighbors[neighbor].pollution_rate -= change

    def transfer_coefficient_of_pollutant_from_neighbor(self, neighbor):
        if self.neighbors[neighbor] == (0, 0, 1):
            return self.GRAVITY + self.WIND_FACTOR * neighbor.velocity.velocities[reverse_direction(self.neighbors[neighbor])] \
                   + self.DIFFUSION_COEFFICIENT
        return self.WIND_FACTOR * neighbor.velocity.velocities[reverse_direction(self.neighbors[neighbor])] \
               + self.DIFFUSION_COEFFICIENT

    def get_pollution_level(self):
        for i in range(len(self.THRESHOLDS) - 1):
            if self.THRESHOLDS[i] < self.pollution_rate <= self.THRESHOLDS[i + 1]:
                return self.THRESHOLDS[i + 1]
        return self.THRESHOLDS[0]

    def draw(self):
        if self.type in (Type.WALL, Type.GROUND):
            return WALL_COLOR
        # elif self.isStreet == True:
        #     return [0,0,255,255]
        else:
            return [255, 0, 0, min(self.pollution_rate * 255 * drawing_precision,255)]

    @property
    def isStreet(self):
        return self._isStreet

    @isStreet.setter
    def isStreet(self, value):
        self._isStreet = value

    def pollute(self):
        if self._isStreet:
            polluting = random()
            if polluting < street_generation_rate:
                if self._clock > 12:
                    self.pollution_rate += polluting/street_generation_diff
                else:
                    self.pollution_rate += polluting
                self.pollute_rate = min(self.pollution_rate,1.0)
                # self.velocity.velocities[(0,0,1)] += car_vertical_blast
                v = self.velocity.velocities[(0,0,1)] + car_vertical_blast
                self.velocity.velocities.update({(0,0,1): v})

    @property
    def isBorder(self):
        return self._isBorder

    @isBorder.setter
    def isBorder(self, value):
        self._isBorder = value

    def updateWind(self,coord,value):
        if self.velocity.velocities[coord] < value:
            v = self.velocity.velocities[coord] + random() / 2
            self.velocity.velocities.update({(coord): v})
