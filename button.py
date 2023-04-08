from typing import Tuple, List

import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluUnProject

from enums import RubiksCubeRotations
from rubiks_cube import RubiksCube


class Button:
    def __init__(self, rubiks_cube: RubiksCube, window_size,
                 x_px, y_px, width_px, height_px,
                 text_color, background_color,
                 text, face: str, angle: int):
        self.rubiks_cube: RubiksCube = rubiks_cube
        self.window_size: Tuple[int, int] = window_size
        self.x_px: float = x_px
        self.y_px: float = y_px
        self.z: float = 0.0
        self.width_px: int = width_px
        self.height_px: int = height_px
        self.text_color: Tuple[int, int, int, int] = text_color
        self.background_color: Tuple[int, int, int, int] = background_color
        self.text: str = text

        self.face = face
        self.angle = angle
        self.vertices: List[Tuple] = self.get_world_vertices()

    @staticmethod
    def convert_screen_to_world(winx, winy, winz=0):
        glLoadIdentity()
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        world_x, world_y, world_z = gluUnProject(winX=winx, winY=winy, winZ=winz,
                                                 model=modelview, proj=projection, view=viewport)
        return world_x, world_y, world_z

    def get_world_vertices(self):
        # Need to make y relative to top instead of bottom
        winy = self.window_size[1] - self.y_px
        winy_bottom = winy - self.height_px

        top_left = (self.x_px, winy, self.z)
        bottom_left = (self.x_px, winy_bottom, self.z)
        bottom_right = (self.x_px + self.width_px, winy_bottom, self.z)
        top_right = (self.x_px + self.width_px, winy, self.z)

        screen_vertices = [top_left, bottom_left, bottom_right, top_right]

        return [self.convert_screen_to_world(*_) for _ in screen_vertices]

    def draw(self):
        # Create font and render text onto a surface
        font = pygame.font.Font(None, size=200)
        text_surface = font.render(self.text, True, self.text_color, self.background_color)

        # Create texture from the text surface
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, pygame.image.tostring(text_surface, "RGBA", True))
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # Enable alpha blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Bind texture and render quad
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        t = 1
        quad_tex_coords = [
            (0.0, t),
            (0.0, 0.0),
            (t, 0.0),
            (t, t),
        ]
        glBegin(GL_QUADS)
        glColor4f(1, 1, 1, 1)
        for i, vertex in enumerate(self.vertices):
            glTexCoord2f(*quad_tex_coords[i])
            glVertex3fv(vertex)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def is_clicked(self, pos):
        x, y = pos
        if self.x_px <= x <= self.x_px + self.width_px and self.y_px <= y <= self.y_px + self.height_px:
            return True
        return False

    def on_click(self):
        self.rubiks_cube.rotate(self.face, self.angle)
