import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

font = pygame.font.Font(None, 36)  # create a font object
text = font.render("Hello, PyOpenGL!", True, (255, 255, 255), (0, 0, 0))  # create a surface with the text
texture = glGenTextures(1)  # generate a texture ID
glBindTexture(GL_TEXTURE_2D, texture)  # bind the texture
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # set texture parameters
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.get_width(), text.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE,
             pygame.image.tostring(text, "RGBA", True))  # load the surface as a texture

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glLoadIdentity()
glTranslatef(-0.5, 0.0, -1.0)  # move the quad to the desired position
glBindTexture(GL_TEXTURE_2D, texture)  # bind the texture
glBegin(GL_QUADS)  # draw a quad with the texture
glTexCoord2f(0.0, 0.0)
glVertex3f(0.0, 0.0, 0.0)
glTexCoord2f(1.0, 0.0)
glVertex3f(1.0, 0.0, 0.0)
glTexCoord2f(1.0, 1.0)
glVertex3f(1.0, 1.0, 0.0)
glTexCoord2f(0.0, 1.0)
glVertex3f(0.0, 1.0, 0.0)
glEnd()

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
