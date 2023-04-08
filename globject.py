from abc import ABC, abstractmethod
from typing import Tuple

from OpenGL.GL import *


class GLObject(ABC):
    def __init__(self, center_pos: tuple[float, float, float]):
        self._center_pos: Tuple[float, float, float] = center_pos
        glTranslatef(*center_pos)

    @property
    def center_pos(self) -> Tuple[float, float, float]:
        return self._center_pos

    @abstractmethod
    def render(self, *args, **kwargs):
        pass
