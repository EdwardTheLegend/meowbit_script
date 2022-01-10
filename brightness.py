from pyb import wfi
from micropython import opt_level, const

opt_level(3)


class BrightnessScript:
    screen_width = const(160)
    screen_height = const(128)

    name = "brightness"

    def __init__(self, screen, sensor, led1, led2) -> None:
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2

    # main function
    def main(self):
        self.screen.fill((255, 255, 255))
        self.screen.text(text="press b to go back", x=0, y=115, color=(0, 100, 0))
        while True:
            wfi()
            if self.sensor.btnValue("a"):
                brightness = self.sensor.getIntensity() // 16
                self.screen.fill((brightness, brightness, brightness))
            elif self.sensor.btnValue("b"):
                break
