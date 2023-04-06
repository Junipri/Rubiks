import pygame
from OpenGL.GL import *


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.z = 1
        self.width = width
        self.height = height
        self.color = color
        self.text = text

        self.vertices = self.get_vertices()

    def get_vertices(self):
        top_left = (self.x, self.y, self.z)
        top_right = (self.x + self.width, self.y, self.z)
        bottom_right = (self.x, self.y + self.height, self.z)
        bottom_left = (self.x + self.width, self.y + self.height, self.z)
        return[top_left, top_right, bottom_right, bottom_left]

    def draw(self, display):

    def is_clicked(self, pos):
        x, y = pos
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return False
