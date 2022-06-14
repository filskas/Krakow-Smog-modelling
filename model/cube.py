from numpy import sign
from model.type import Type
from model.velocity import Velocity, other_axes
from random import random
from random import shuffle


def reverse_direction(direction):
    return tuple((-element for element in direction))

WALL_COLOR=[1,1,1,255]

class Cube:
    NUMBER_OF_DIMENSIONS = 3
    DIFFUSION_COEFFICIENT = 0.01
    WIND_FACTOR = 1
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
        self.pressure = pressure
        self._nextAir = None
        self._isStreet = False
        self._updated = False
        self.pollute_rate = None
        self.is_boarder_pollution_source = False

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

    # def bounce_off(self, neighbor):
    #     if neighbor.type in (Type.WALL, Type.GROUND):
    #         for i in range(self.NUMBER_OF_DIMENSIONS):
    #             if sign(neighbor.coordinates[i] - self.coordinates[i]) == sign(self.velocity[i]):
    #                 self.velocity[i] *= -1

    def update(self):
        if self.type == Type.AIR:
            self.pollute()
            # previous version
            # for neighbor in self.neighbors.keys():
            #     self.interact_with_neighbor(neighbor)
            list_of_keys = list(self.neighbors.keys())
            shuffle(list_of_keys)
            for neighbor in list_of_keys:
                self.interact_with_neighbor(neighbor)

            if self.is_boarder_pollution_source:
                self.pollution_rate = 0

    def interact_with_neighbor(self, neighbor):
        if neighbor.type in (Type.WALL, Type.GROUND):
            self.spread(neighbor)
        else:
            self.update_from_neighbor(neighbor)

    # might be too slow (one move is spread and the next is impacting the other cells)
    def spread(self, neighbor):
        if neighbor.type in (Type.WALL, Type.GROUND):
            velocity = self.velocity.velocities[self.neighbors[neighbor]]
            velocity_part = velocity // 4
            for v in other_axes(self.neighbors[neighbor]):
                updated = {v: self.velocity.velocities[v] + velocity_part}
                self.velocity.velocities.update(updated)
            self.velocity.velocities.update({self.neighbors[neighbor]: 0})

    def update_from_neighbor(self, neighbor):
        self.pollution_rate += self.transfer_coefficient_of_pollutant_from_neighbor(neighbor) \
                               * (neighbor.pollution_rate - self.pollution_rate)

    def transfer_coefficient_of_pollutant_from_neighbor(self, neighbor):
        if self.neighbors[neighbor] == (0, 0, -1):
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
            return [255, 0, 0, min(self.pollution_rate * 255 * 10,255)]

    @property
    def isStreet(self):
        return self._isStreet

    @isStreet.setter
    def isStreet(self, value):
        self._isStreet = value

    def pollute(self):
        if self._isStreet:
            polluting = random()
            if polluting < 0.2:
                self.pollution_rate += polluting
                self.pollute_rate = min(self.pollution_rate, 1.0)
                self.velocity.velocities[(0, 0, 1)] += 0.001

        elif self.is_boarder_pollution_source:
            polluting = random()
            if polluting < 0.2:
                self.pollution_rate += polluting
                self.pollute_rate = min(self.pollution_rate, 1.0)
                # directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
                # for direction in directions:
                #     if direction not in self.neighbors.values():
                #         self.velocity.velocities[direction] += 0.001


