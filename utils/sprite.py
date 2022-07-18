from screen import Screen
from framebuf import RGB565, FrameBuffer


class Sprite:
    def __init__(self, sprite_path, width, screen, x, y, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.h = height

        self._fb = FrameBuffer(bytearray(width * height * 2), width, height, RGB565)
        self._fb.loadbmp(sprite_path, 0, 0)

    def render(self):
        self.screen._fb.blit(
            self._fb,
            self.x,
            self.y,
        )
