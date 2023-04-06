import json
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

from OpenGL.GL import *
import numpy as np

from enums import GlColors4f, Surfaces


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


class Cube(GLObject):
    def __init__(self,
                 center_pos: Tuple[float, float, float],
                 edge_length: float,
                 location_index: Tuple[int, int, int],
                 surface_colors_in: Dict[str, GlColors4f] = None):
        super(Cube, self).__init__(center_pos)

        surface_colors: Dict[str, GlColors4f] = {surface.name: GlColors4f.BLACK_SOLID.value for surface in Surfaces}
        if surface_colors_in:
            for k, v in surface_colors_in.items():
                surface_colors[k] = v

        self.__edge_length: float = edge_length
        self.__location_index: Tuple[int, int, int] = location_index
        self.__colors: Dict[str, GlColors4f] = surface_colors

        self.__vertices: List[Tuple[float, float, float]] = self.get_vertices()

    def get_vertices(self) -> List[Tuple[float, float, float]]:
        """
        Returns: List of (x, y, z) coordinates for vertices of the cube.
        """
        half_edge_length: float = self.__edge_length / 2
        offsets: Tuple[float, float] = (-half_edge_length, half_edge_length)

        vertices: List[Tuple[float, float, float]] = []
        for x_offset in offsets:
            for y_offset in offsets:
                for z_offset in offsets:
                    vertex_pos: Tuple[float, float, float] = (self._center_pos[0] + x_offset,
                                                              self._center_pos[1] + y_offset,
                                                              self._center_pos[2] + z_offset)
                    vertices.append(vertex_pos)
        return vertices

    def render(self, *args, **kwargs):
        object_x_angle = kwargs['object_x_angle']
        object_y_angle = kwargs['object_y_angle']

        # Transparency
        glMatrixMode(GL_MODELVIEW)  # Applies subsequent matrix operations to the modelview matrix stack.
        glLoadIdentity()

        glBegin(GL_QUADS)
        for surface in Surfaces:
            color = self.__colors[surface.name]
            glColor4f(*color)
            vertices: Tuple[float, float, float, float] = tuple(surface.value)
            for vertex in vertices:
                glVertex3fv([_ * 0.98 for _ in self.__vertices[vertex]])
        glEnd()


class RubiksCube(GLObject):
    def __init__(self,
                 center_pos: Tuple[float, float, float],
                 piece_edge_length: float = 1.0):
        super(RubiksCube, self).__init__(center_pos)

        self.__piece_edge_length: float = piece_edge_length

        self.__surface_colors = self.get_piece_colors()
        self.__pieces = self.get_pieces()

    @staticmethod
    def get_piece_colors() -> np.ndarray[(3, 3, 3), dict]:
        surface_colors: np.ndarray[(3, 3, 3), dict] = np.empty((3, 3, 3), dtype=dict)
        # Bottom layer
        surface_colors[0, 0, 0] = {
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value
        }
        surface_colors[1, 0, 0] = {
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value,
        }
        surface_colors[2, 0, 0] = {
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        surface_colors[0, 0, 1] = {
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value
        }
        surface_colors[1, 0, 1] = {
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value,
        }
        surface_colors[2, 0, 1] = {
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        surface_colors[0, 0, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value
        }
        surface_colors[1, 0, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value,
        }
        surface_colors[2, 0, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.BOTTOM.name: GlColors4f.YELLOW_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        # Middle layer
        surface_colors[0, 1, 0] = {
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
        }
        surface_colors[1, 1, 0] = {
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
        }
        surface_colors[2, 1, 0] = {
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        surface_colors[0, 1, 1] = {
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
        }
        surface_colors[1, 1, 1] = {
        }
        surface_colors[2, 1, 1] = {
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        surface_colors[0, 1, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
        }
        surface_colors[1, 1, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
        }
        surface_colors[2, 1, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        # TOP layer
        surface_colors[0, 2, 0] = {
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value
        }
        surface_colors[1, 2, 0] = {
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value,
        }
        surface_colors[2, 2, 0] = {
            Surfaces.FRONT.name: GlColors4f.RED_SOLID.value,
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        surface_colors[0, 2, 1] = {
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value
        }
        surface_colors[1, 2, 1] = {
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value,
        }
        surface_colors[2, 2, 1] = {
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        surface_colors[0, 2, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.LEFT.name: GlColors4f.GREEN_SOLID.value,
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value
        }
        surface_colors[1, 2, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value,
        }
        surface_colors[2, 2, 2] = {
            Surfaces.BACK.name: GlColors4f.ORANGE_SOLID.value,
            Surfaces.TOP.name: GlColors4f.WHITE_SOLID.value,
            Surfaces.RIGHT.name: GlColors4f.BLUE_SOLID.value
        }
        return surface_colors

    def get_pieces(self) -> np.ndarray[(3, 3, 3), Cube]:
        cubes: np.ndarray[(3, 3, 3), Cube] = np.empty((3, 3, 3), dtype=Cube)
        offsets: np.ndarray[float] = np.array([r * self.__piece_edge_length * 1.1 for r in range(-1, 2)])

        for j, y_offset in enumerate(offsets):
            for i, x_offset in enumerate(offsets):
                for k, z_offset in enumerate(reversed(offsets)):
                    cube_pos: Tuple[float, float, float] = (self._center_pos[0] + x_offset,
                                                            self._center_pos[1] + y_offset,
                                                            self._center_pos[2] + z_offset)
                    location_index: Tuple[int, int, int] = (i, j, k)
                    surface_colors: dict = self.__surface_colors[i, j, k]
                    cube: Cube = Cube(center_pos=cube_pos,
                                      edge_length=self.__piece_edge_length,
                                      location_index=location_index,
                                      surface_colors_in=surface_colors)
                    cubes[i, j, k] = cube
        return cubes

    def render(self, *args, **kwargs):
        object_xy_angle = kwargs['object_xy_angle']
        object_x_angle = object_xy_angle[0]
        object_y_angle = object_xy_angle[1]
        vectorized_fun = np.vectorize(Cube.render)
        vectorized_fun(self.__pieces, object_x_angle=object_x_angle, object_y_angle=object_y_angle)
