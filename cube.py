# import pygame
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
#
# from enums import Vertices, Edges, Surfaces
#
# edges = [_.value for _ in Edges]
# vertices = [_.value for _ in Vertices]
# surfaces = [_.value for _ in Surfaces]
#
#
# def Cube(x, y, z):
#     glLoadIdentity()
#     glTranslatef(x, y, z)
#     glBegin(GL_QUADS)
#     glColor4f(0.0, 1.0, 0.0, 1.0)
#     for surface in [_.value for _ in Surfaces]:
#         for vertex in surface:
#             glVertex3fv(vertices[vertex])
#     glEnd()
#     glBegin(GL_LINES)
#     glColor4f(0.0, 0.0, 1.0, 1.0)
#     for edge in edges:
#         for vertex in edge:
#             glVertex3fv(vertices[vertex])
#     glEnd()
