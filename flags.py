from micropython import opt_level
from pyb import wfi

opt_level(3)


class FlagsScript:
    screen_width = 160
    screen_height = 128

    name = "flags"

    def __init__(self, screen, sensor, led1, led2) -> None:
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2

    def japan(self):
        self.screen.fill((255, 255, 255), update=False)
        self.screen.circle(80, 64, 40, (255, 0, 0), (0, 255, 0), update=False)
        self.screen.refresh()

    def france(self):
        self.screen.fill((255, 255, 255), update=False)
        self.screen.rect(
            0,
            0,
            self.screen_width // 3,
            self.screen_height,
            (0, 0, 255),
            (0, 0, 255),
            update=False,
        )
        self.screen.rect(
            (self.screen_width // 3) * 2,
            0,
            self.screen_width // 3,
            self.screen_height,
            (255, 0, 0),
            (255, 0, 0),
            update=False,
        )
        self.screen.refresh()

    def italy(self):
        self.screen.fill((255, 255, 255), update=False)
        self.screen.rect(
            0,
            0,
            self.screen_width // 3,
            self.screen_height,
            (0, 255, 0),
            (0, 255, 0),
            update=False,
        )
        self.screen.rect(
            (self.screen_width // 3) * 2,
            0,
            self.screen_width // 3,
            self.screen_height,
            (255, 0, 0),
            (255, 0, 0),
            update=False,
        )
        self.screen.refresh()

    # main function
    def main(self):
        self.flags_list = [self.france, self.japan, self.italy]
        self.flag_index = 0
        self.flags_list[self.flag_index]()
        while True:
            wfi()
            if self.sensor.btnValue("right") == 1:
                self.flag_index = (self.flag_index + 1) % len(self.flags_list)
                self.flags_list[self.flag_index]()
            elif self.sensor.btnValue("left") == 1:
                self.flag_index = (self.flag_index - 1) % len(self.flags_list)
                self.flags_list[self.flag_index]()
            elif self.sensor.btnValue("b"):
                break
