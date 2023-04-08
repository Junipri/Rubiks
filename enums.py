from enum import IntEnum, StrEnum, Enum
from typing import Tuple

import numpy as np


def with_values(cls):
    value_list = [member.value for member in cls]
    cls.values = lambda: value_list
    return cls


def with_dict(cls):
    enum_dict = {i.name: i.value for i in cls}
    cls.dict = lambda: enum_dict
    return cls


@with_values
class PygameWindow(IntEnum):
    WIDTH = 1000
    HEIGHT = (9 / 16) * WIDTH


class GlColors4f(Enum):
    WHITE_SOLID = (1, 1, 1, 1)
    YELLOW_SOLID = (1, 1, 0, 1)
    GREEN_SOLID = (0, 1, 0, 1)
    BLUE_SOLID = (0, 0, 1, 1)
    RED_SOLID = (1, 0, 0, 1)
    ORANGE_SOLID = (1, 0.5, 0, 1)

    BLACK_SOLID = (0, 0, 0, 1)


@with_dict
@with_values
class Edges(Enum):
    LEFT_TOP = (2, 3)
    LEFT_BOTTOM = (0, 1)
    LEFT_FRONT = (0, 2)
    LEFT_BACK = (1, 3)

    RIGHT_TOP = (6, 7)
    RIGHT_BOTTOM = (4, 5)
    RIGHT_FRONT = (4, 6)
    RIGHT_BACK = (5, 7)

    TOP_FRONT = (2, 6)
    TOP_BACK = (3, 7)
    BOTTOM_FRONT = (0, 4)
    BOTTOM_BACK = (1, 5)


@with_dict
@with_values
class Surfaces(Tuple[int, int, int, int], Enum):
    FRONT = (1, 3, 7, 5)
    BACK = (0, 2, 6, 4)
    LEFT = (0, 1, 3, 2)
    RIGHT = (4, 6, 7, 5)
    TOP = (2, 3, 7, 6,)
    BOTTOM = (0, 1, 5, 4)


@with_values
class RubiksCubeRotations(StrEnum):
    F = 'F'
    B = 'B'
    U = 'U'
    D = 'D'
    L = 'L'
    R = 'R'


@with_dict
class RubiksAxes(Enum):
    X = (1, 0, 0)
    Y = (0, 1, 0)
    Z = (0, 0, 1)


@with_dict
class RubiksFaceRotation(Enum):
    F = RubiksAxes.Z.value
    B = RubiksAxes.Z.value
    U = RubiksAxes.Y.value
    D = RubiksAxes.Y.value
    L = RubiksAxes.X.value
    R = RubiksAxes.X.value

