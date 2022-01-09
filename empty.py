from pyb import wfi
from micropython import opt_level

opt_level(3)


class EmptyScript:
    screen_width = 160
    screen_height = 128

    name = "empty"

    def __init__(self, screen, sensor, led1, led2) -> None:
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2

    # main function
    def main(self):
        self.screen.fill((255, 255, 255))
        self.screen.text(text="press b to go back", x=0, y=0, color=(0, 100, 0))
        while True:
            wfi()
            if self.sensor.btnValue("b"):
                break
