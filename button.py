from typing import Tuple, List

import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluUnProject

from rubiks_cube import RubiksCube


class Button:
    def __init__(self, rubiks_cube: RubiksCube, window_size, display, x_px, y_px, width_px, height_px, color, text=''):
        self.rubiks_cube: RubiksCube = rubiks_cube
        self.window_size: Tuple[int, int] = window_size
        self.display = display
        self.x_px: float = x_px
        self.y_px: float = y_px
        self.z: float = 0.0
        self.width_px: int = width_px
        self.height_px: int = height_px
        self.color: Tuple[int, int, int] = color
        self.text: str = text

        self.vertices: List[Tuple] = self.get_world_vertices()
        print(self.vertices)

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

    def get_vertices(self):
        top_left = (self.x_px, self.y_px, self.z)
        bottom_left = (self.x_px, self.y_px + self.height_px, self.z)
        bottom_right = (self.x_px + self.width_px, self.y_px + self.height_px, self.z)
        top_right = (self.x_px + self.width_px, self.y_px, self.z)

        return [top_left, bottom_left, bottom_right, top_right]

    def draw(self):
        glLoadIdentity()
        font = pygame.font.Font(None, 36)  # create a font object
        text = font.render(self.text, True, (255, 255, 255), (0, 0, 0))  # create a surface with the text
        texture = glGenTextures(1)  # generate a texture ID
        glBindTexture(GL_TEXTURE_2D, texture)  # bind the texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # set texture parameters
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.get_width(), text.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     pygame.image.tostring(text, "RGBA", True))  # load the surface as a texture

        glLoadIdentity()
        glBindTexture(GL_TEXTURE_2D, texture)

        glBegin(GL_QUADS)
        glColor3f(*self.color)
        for vertex in self.vertices:
            glVertex3fv(vertex)
        glEnd()

    def is_clicked(self, pos):
        x, y = pos
        if self.x_px <= x <= self.x_px + self.width_px and self.y_px <= y <= self.y_px + self.height_px:
            return True
        return False
