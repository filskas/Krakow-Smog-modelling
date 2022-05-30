from numpy import sign
from Type import Type
from Velocity import Velocity, other_axes


def reverse_direction(direction):
    return tuple((-element for element in direction))


class Cube:
    NUMBER_OF_DIMENSIONS = 3
    DIFFUSION_COEFFICIENT = 0.4
    WIND_FACTOR = 1
    THRESHOLDS = (0.1, 0.3, 0.6, 0.9)

    def __init__(self, type, coordinates, size, pollution_rate, velocity, pressure):
        self._type = type
        self._coordinates = coordinates
        self._size = size
        self.pollution_rate = pollution_rate
        self.previous_pollution_rate = pollution_rate
        self._velocity = velocity
        self.neighbors = dict()
        self.pressure = pressure

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in Type.list():
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

    def bounce_off(self, neighbor):
        if neighbor.type in (Type.WALL, Type.GROUND):
            for i in range(self.NUMBER_OF_DIMENSIONS):
                if sign(neighbor.coordinates[i] - self.coordinates[i]) == sign(self.velocity[i]):
                    self.velocity[i] *= -1

    # might be too slow (one move is spread and the next is impacting the other cells)
    def spread(self, neighbor):
        if neighbor.type in (Type.WALL, Type.GROUND):
            velocity = self.velocity.velocities[self.neighbors[neighbor]]
            velocity_part = velocity // 4
            for v in other_axes(self.neighbors[neighbor]):
                updated = {v: self.velocity.velocities[v] + velocity_part}
                self.velocity.velocities.update(updated)
            self.velocity.velocities.update({self.neighbors[neighbor]: 0})

    def transfer_coefficient_of_pollutant_from_neighbor(self, neighbor):
        return self.WIND_FACTOR * neighbor.velocity.velocities[reverse_direction(self.neighbors[neighbor])] \
               + self.DIFFUSION_COEFFICIENT

    def update_from_neighbor(self, neighbor):
        self.pollution_rate += self.transfer_coefficient_of_pollutant_from_neighbor(neighbor) \
                               * (neighbor.previous_pollution_rate - self.previous_pollution_rate)

    def interact_with_neighbor(self, neighbor):
        if neighbor.type in (Type.WALL, Type.GROUND):
            # self.bounce_off(neighbor)
            self.spread(neighbor)
        else:
            self.update_from_neighbor(neighbor)

    def move(self):
        if self.type == Type.AIR:
            self.previous_pollution_rate = self.pollution_rate
            for neighbor in self.neighbors.keys():
                self.interact_with_neighbor(neighbor)
