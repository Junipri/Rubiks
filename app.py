from typing import Tuple

from enums import PygameWindow
from pygame_wrapper import GluPerspectiveDC, PygameWrapper


def main():
    window_size: Tuple[int, int] = PygameWindow.values()
    glu_perspective: GluPerspectiveDC = GluPerspectiveDC(fov_y=45,
                                                         aspect_ratio=window_size[0] / window_size[1],
                                                         z_near=0.1,
                                                         z_far=50.0)
    camera_pos: Tuple[float, float, float] = (0.0, -1.0, -10.0)

    pygame_wrapper = PygameWrapper(window_size=window_size,
                                   glu_perspective=glu_perspective,
                                   camera_pos=camera_pos)
    pygame_wrapper.run()


if __name__ == "__main__":
    main()
