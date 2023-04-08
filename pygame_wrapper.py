from typing import Tuple, List

import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.event import Event
from pygame.locals import *

from button import Button
from data_classes import GluPerspectiveDC, GameState
from enums import GlColors4f, RubiksCubeRotations
from rubiks_cube import RubiksPiece, RubiksCube


class PygameWrapper:
    def __init__(self,
                 window_size: Tuple[int, int],
                 glu_perspective: GluPerspectiveDC,
                 camera_pos: Tuple[float, float, float]):
        self.display = None
        self.__rubiks_cube: RubiksCube = None
        self.__window_size: Tuple[int, int] = window_size
        self.__glu_perspective: GluPerspectiveDC = glu_perspective
        self.__camera_pos: Tuple[float, float, float] = camera_pos

        self.__state: GameState = GameState(last_frame_tick=pygame.time.get_ticks())

        self.init_display()

        self.buttons: List[Button] = self.get_buttons()

    def get_buttons(self):
        top_left_coords = (10, 10)

        button_width_px = 100
        button_height_px = 50
        button_x_spacing_factor = 1.1
        button_y_spacing_factor = 1.1
        buttons: List[Button] = []

        variations = ["", "'", '2']
        var_angles = [-90, 90, -180]
        for i, r in enumerate(RubiksCubeRotations.values()):
            y = top_left_coords[1] + i * button_y_spacing_factor * button_height_px
            for j, (v, angle) in enumerate(zip(variations, var_angles)):
                text = f'{r}{v}'
                x = top_left_coords[0] + j * button_x_spacing_factor * button_width_px
                if r == 'B' or r == 'D' or r == 'L':
                    angle *= -1
                button = Button(self.__rubiks_cube, window_size=self.__window_size,
                                x_px=x, y_px=y, width_px=button_width_px, height_px=button_height_px,
                                text_color=(255, 255, 255, 255), background_color=(0, 255, 0, 0),
                                text=text, face=r, angle=angle)
                buttons.append(button)
        return buttons

    def init_display(self):
        pygame.init()
        self.display = pygame.display.set_mode(size=self.__window_size,
                                               flags=DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Rubiks Cube Explore")
        glEnable(GL_DEPTH_TEST)

        # Setup cameras
        glMatrixMode(GL_PROJECTION)  # Applies subsequent matrix operations to the projection matrix stack.
        gluPerspective(*self.__glu_perspective)
        glTranslatef(*self.__camera_pos)

        # Setup Rubik's Cube
        glMatrixMode(GL_MODELVIEW)  # Applies subsequent matrix operations to the modelview matrix stack.
        self.__rubiks_cube: RubiksCube = RubiksCube(center_pos=(3.0, 0.0, 0.0))

    def draw_object(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*GlColors4f.WHITE_SOLID.value)
        # Buttons
        [button.draw() for button in self.buttons]
        self.__rubiks_cube.render()

    def handle_mouse_motion(self, event: Event):
        if self.__state.mouse_pressed:
            # Calculate the mouse movement since the last frame
            self.__state.mouse_xy_delta = event.rel
            mouse_xy_delta = list(self.__state.mouse_xy_delta)

            # Update the object yaw and pitch angles based on the mouse movement
            object_xy_angle = list(self.__state.object_xy_angle)
            object_xy_angle[0] += mouse_xy_delta[0] * 0.2
            object_xy_angle[1] += mouse_xy_delta[1] * 0.2
            self.__state.object_xy_angle = object_xy_angle

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        button.on_click()

            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)

    def update_state(self):
        self.__state.time_delta = (pygame.time.get_ticks() - self.__state.last_frame_tick) / 1000.0
        self.__state.last_frame_tick = pygame.time.get_ticks()

        pygame.display.flip()
        pygame.time.wait(10)

    def run(self):

        while True:
            self.handle_event()
            self.update_state()
            self.draw_object()
