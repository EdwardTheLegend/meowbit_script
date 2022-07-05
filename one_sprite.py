from framebuf import RGB565, FrameBuffer
from micropython import const, opt_level
from pyb import wfi
from screen import Screen

opt_level(3)


class OneSpriteScript:
    screen_width = const(160)
    screen_height = const(128)
    name = "one sprite"

    def __init__(self, screen, sensor, led1, led2) -> None:
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2

    def main(self):
        self.sprite = FrameBuffer(bytearray(20 * 20 * 2), 20, 20, RGB565)
        self.sprite.fill(Screen.getColHex((255, 255, 255)))
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        pause_time = const(5)
        step_size = const(20)
        while True:
            wfi()

            if self.sensor.btnValue("right", time=pause_time) == 1:
                self.x += step_size
                if self.x >= self.screen_width:
                    self.x = self.screen_width - 1

            if self.sensor.btnValue("left", time=pause_time) == 1:
                self.x -= step_size
                if self.x < 0:
                    self.x = 0

            if self.sensor.btnValue("up", time=pause_time) == 1:
                self.y -= step_size
                if self.y < 0:
                    self.y = 0

            if self.sensor.btnValue("down", time=pause_time) == 1:
                self.y += step_size
                if self.y >= self.screen_height:
                    self.y = self.screen_height - 1

            if self.sensor.btnValue("b"):
                break

            self.screen.clear(update=False)
            self.screen._fb.blit(self.sprite, self.x, self.y)
            self.screen.refresh()
