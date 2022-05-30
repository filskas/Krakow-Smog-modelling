from enum import Enum


class Type(Enum):
    AIR = 1
    WALL = -1
    GROUND = -1

    @classmethod
    def list(cls):
        return [element.name for element in Type]
