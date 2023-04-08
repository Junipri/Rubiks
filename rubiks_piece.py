from typing import List, Tuple, Dict

from OpenGL.GL import *

from enums import GlColors4f, Surfaces, RubiksAxes
from globject import GLObject


class RubiksPiece(GLObject):
    def __init__(self,
                 rubiks_cube_center: Tuple[float, float, float],
                 center_pos: Tuple[float, float, float],
                 edge_length: float,
                 location_index: Tuple[int, int, int],
                 faces: list[str],
                 surface_colors_in: Dict[str, GlColors4f] = None):
        super(RubiksPiece, self).__init__(center_pos)

        surface_colors: Dict[str, GlColors4f] = {surface.name: GlColors4f.BLACK_SOLID.value for surface in Surfaces}
        if surface_colors_in:
            for k, v in surface_colors_in.items():
                surface_colors[k] = v

        self.rubiks_cube_center: Tuple[float, float, float] = rubiks_cube_center
        self.faces: list[str] = faces

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

    def rotate(self, elapsed_angle, rotation_face):
        face_rotation_dict = {
            'F': RubiksAxes.Z.value,
            'B': RubiksAxes.Z.value,
            'U': RubiksAxes.Y.value,
            'D': RubiksAxes.Y.value,
            'L': RubiksAxes.X.value,
            'R': RubiksAxes.X.value,
        }
        # Transparency
        glMatrixMode(GL_MODELVIEW)  # Applies subsequent matrix operations to the modelview matrix stack.
        glLoadIdentity()
        rotation_axis: Tuple[int, int, int] = face_rotation_dict[rotation_face]

        if rotation_face in self.faces:
            print(glGetInteger(GL_MODELVIEW_STACK_DEPTH))
            glTranslatef(*self.rubiks_cube_center)
            glRotatef(elapsed_angle, *rotation_axis)
            glTranslatef(*[-1 * _ for _ in self.rubiks_cube_center])
        self.render()

    def render(self, *args, **kwargs):
        if kwargs:
            elapsed_angle = kwargs['elapsed_angle']
            rotation_face = kwargs['rotation_face']
            self.rotate(elapsed_angle, rotation_face)

        glBegin(GL_QUADS)
        for surface in Surfaces:
            color = self.__colors[surface.name]
            glColor4f(*color)
            for vertex in surface.value:
                glVertex3fv([_ * 0.98 for _ in self.__vertices[vertex]])
        glEnd()
