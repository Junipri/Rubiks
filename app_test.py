import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL|pygame.RESIZABLE)

    # Set up OpenGL perspective
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Create font and render text onto a surface
    font = pygame.font.Font(None, 48)
    text_surface = font.render("Click Me", True, (255, 255, 255, 255), (0, 0, 0, 0))

    # Create texture from the text surface
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(text_surface, "RGBA", True))
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # Create quad vertices
    quad_vertices = [
        (-0.5, -0.5, 0.0),
        (0.5, -0.5, 0.0),
        (0.5, 0.5, 0.0),
        (-0.5, 0.5, 0.0),
    ]

    # Create quad texture coordinates
    quad_tex_coords = [
        (1.0, 1.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (0.0, 0.0),
    ]

    # Enable alpha blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Clicked!")

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Translate quad to center of screen
        glTranslatef(0.0, 0.0, -5.0)

        # Bind texture and render quad
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord2f(*quad_tex_coords[i])
            glVertex3f(*quad_vertices[i])
        glEnd()
        glDisable(GL_TEXTURE_2D)

        pygame.display.flip()

if __name__ == '__main__':
    main()
