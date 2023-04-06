from typing import Tuple, List

import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.event import Event
from pygame.locals import *

from button import Button
from data_classes import GluPerspectiveDC, GameState
from enums import GlColors4f
from rubiks_cube import Cube, RubiksCube


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

        self.buttons: List[Button] = [Button(10, 10, 100, 50, (255, 0, 0), 'Click Me')]

    def init_display(self):
        def get_camera_matrix():
            model_view = np.zeros((4, 4), dtype=np.float32)
            projection = np.zeros((4, 4), dtype=np.float32)
            glGetDoublev(GL_MODELVIEW_MATRIX, model_view)
            glGetDoublev(GL_PROJECTION_MATRIX, projection)
            view = np.dot(model_view, projection)
            inv_view = np.linalg.pinv(view)
            camera_pos = inv_view[:3, 3]
            camera_dir = inv_view[:3, :3] @ np.array([0, 0, -1])
            return camera_pos, camera_dir
        pygame.init()
        self.display = pygame.display.set_mode(size=self.__window_size,
                                flags=DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Rubiks Cube Explore")
        glEnable(GL_DEPTH_TEST)

        # Setup cameras
        glMatrixMode(GL_PROJECTION)  # Applies subsequent matrix operations to the projection matrix stack.
        gluPerspective(*self.__glu_perspective)
        glTranslatef(*self.__camera_pos)
        print(get_camera_matrix())

        # Setup Rubik's Cube
        glMatrixMode(GL_MODELVIEW)  # Applies subsequent matrix operations to the modelview matrix stack.
        self.__rubiks_cube: RubiksCube = RubiksCube(center_pos=(0.0, 0.0, 0.0))

    def draw_object(self):
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*GlColors4f.WHITE_SOLID.value)

        # glRotatef(self.__state.object_xy_angle[1], 1.0, 0.0, 0.0)
        # glRotatef(self.__state.object_xy_angle[0], 0.0, 1.0, 0.0)
        self.__rubiks_cube.render(object_xy_angle=self.__state.object_xy_angle)

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

            # Buttons
            [button.draw(self.display) for button in self.buttons]

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons[0].is_clicked(pygame.mouse.get_pos()):
                        print('Button clicked')

            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)

    def update_state(self):
        self.__state.time_delta = (pygame.time.get_ticks() - self.__state.last_frame_tick) / 1000.0
        self.__state.last_frame_tick = pygame.time.get_ticks()

        pygame.display.flip()
        pygame.time.wait(10)

    def run(self):
        self.init_display()

        while True:
            self.handle_event()
            self.update_state()
            self.draw_object()
