def other_axes(unit_vector):
    if unit_vector[0] != 0:
        return [(0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    elif unit_vector[1] != 0:
        return [(-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1)]
    elif unit_vector[2] != 0:
        return [(0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0)]


class Velocity:
    def __init__(self, smaller_x, greater_x, smaller_y, greater_y, smaller_z, greater_z):
        self.velocities = {
            (-1, 0, 0): smaller_x,
            (1, 0, 0): greater_x,
            (0, -1, 0): smaller_y,
            (0, 1, 0): greater_y,
            (0, 0, -1): smaller_z,
            (0, 0, 1): greater_z
        }
