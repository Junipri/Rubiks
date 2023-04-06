from dataclasses import dataclass, astuple
from typing import Tuple


@dataclass
class GluPerspectiveDC:
    fov_y: int
    aspect_ratio: float
    z_near: float
    z_far: float

    def __iter__(self):
        return iter(astuple(self))


@dataclass
class GameState:
    last_frame_tick: int = 0
    time_delta: float = 0

    object_xy_angle: Tuple[float, float] = (0.0, 0.0)

    mouse_xy_delta: Tuple[float, float] = (0.0, 0.0)
    mouse_pressed: bool = False
