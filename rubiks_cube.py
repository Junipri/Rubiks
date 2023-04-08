import json
import time
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

from OpenGL.GL import *
import numpy as np

from enums import GlColors4f, Surfaces, RubiksAxes, RubiksFaceRotation, RubiksCubeRotations
from globject import GLObject
from rubiks_piece import RubiksPiece


class RubiksCube(GLObject):
    def __init__(self,
                 center_pos: Tuple[float, float, float],
                 piece_edge_length: float = 1.0):
        super(RubiksCube, self).__init__(center_pos)

        self.elapsed_angle = None
        self.rotation_face = None
        self.elapsed_rotation_time = None
        self.rotation_angle = None
        self.rotation_axis = None
        self.rotation_start_time = None
        self.is_rotating: bool = False

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

    def get_pieces(self) -> np.ndarray[(3, 3, 3), RubiksPiece]:
        cubes: np.ndarray[(3, 3, 3), RubiksPiece] = np.empty((3, 3, 3), dtype=RubiksPiece)
        offsets: np.ndarray[float] = np.array([r * self.__piece_edge_length * 1.1 for r in range(-1, 2)])
        for j, y_offset in enumerate(offsets):
            for i, x_offset in enumerate(offsets):
                for k, z_offset in enumerate(reversed(offsets)):
                    faces = []
                    if j == 0:
                        faces.append('D')
                    elif j == 2:
                        faces.append('U')
                    if i == 0:
                        faces.append('L')
                    elif i == 2:
                        faces.append('R')
                    if k == 0:
                        faces.append('F')
                    elif k == 2:
                        faces.append('B')
                    cube_pos: Tuple[float, float, float] = (self._center_pos[0] + x_offset,
                                                            self._center_pos[1] + y_offset,
                                                            self._center_pos[2] + z_offset)
                    location_index: Tuple[int, int, int] = (i, j, k)
                    surface_colors: dict = self.__surface_colors[i, j, k]
                    print(faces)
                    cube: RubiksPiece = RubiksPiece(rubiks_cube_center=self.center_pos,
                                                    center_pos=cube_pos,
                                                    edge_length=self.__piece_edge_length,
                                                    location_index=location_index,
                                                    faces=faces,
                                                    surface_colors_in=surface_colors)
                    cubes[i, j, k] = cube
        return cubes

    def rotate(self, face: str, angle):

        self.rotation_start_time = time.time()
        self.is_rotating = True

        self.rotation_face: str = face
        self.rotation_angle = angle



    def render(self, *args, **kwargs):
        if self.is_rotating:
            self.elapsed_rotation_time = time.time() - self.rotation_start_time
            duration_in_sec = 0.5
            rotation_completion = self.elapsed_rotation_time / duration_in_sec
            self.elapsed_angle = self.rotation_angle * rotation_completion

            vectorized_fun = np.vectorize(RubiksPiece.render)
            vectorized_fun(self.__pieces,
                           elapsed_angle=self.elapsed_angle,
                           rotation_face=self.rotation_face)

            if rotation_completion >= 1:
                self.is_rotating = False
                self.rotation_axis = None
                self.elapsed_angle = 0
        else:
            vectorized_fun = np.vectorize(RubiksPiece.render)
            vectorized_fun(self.__pieces)
