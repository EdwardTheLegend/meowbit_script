from pyb import wfi
from micropython import opt_level

opt_level(3)


class ExampleBMPScript:
    name = "example_bmp"

    def __init__(self, screen, sensor, led1, led2):
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2

    def main(self):
        image_path = "images/example_bmp/sky_tree_ground.bmp"

        # load the image
        self.screen.loadBmp(image_path)

        # loop until b is pressed
        while True:
            wfi()
            if self.sensor.btnValue("b"):
                break
