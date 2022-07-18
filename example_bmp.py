from framebuf import FrameBuffer, RGB565
from pyb import wfi
from micropython import opt_level

opt_level(3)


class ExampleBMPScript:
    name = "example bmp"

    def __init__(self, screen, sensor, led1, led2):
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2

    def main(self):
        image_path = "images/sky_tree_ground.bmp"

        # # load the image
        # self.screen.loadBmp(image_path)

        self._fb = FrameBuffer(bytearray(160 * 128 * 2), 160, 128, RGB565)
        self._fb.loadbmp(image_path, 0, 0)

        self.screen._fb.blit(self._fb, 0, 0)

        # loop until b is pressed
        while True:
            wfi()
            if self.sensor.btnValue("b"):
                break
