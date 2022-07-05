from framebuf import RGB565, FrameBuffer
from micropython import const, opt_level
from pyb import wfi
from screen import Screen

opt_level(3)


class ScrollingBackgroundScript:
    screen_width = const(160)
    screen_height = const(128)
    name = "scrolling background"

    def __init__(self, screen, sensor, led1, led2) -> None:
        self.screen = screen
        self.sensor = sensor

        self.background_offset = 0

    def main(self):
        pause_time = const(5)
        while True:
            wfi()
            if self.sensor.btnValue("right", pause_time) == 1:
                self.background_offset -= 20
            elif self.sensor.btnValue("left", pause_time) == 1:
                self.background_offset += 20
            elif self.sensor.btnValue("b", pause_time):
                break

            self.background_offset %= self.screen_width

            self.screen.clear(update=False)
            self.screen.loadBmp("images/sky_tree_ground.bmp", self.background_offset)
            self.screen.refresh()
