from script import Script
from pyb import wfi

class OnePixel(Script):
    def __init__(self, screen, sensor, led1, led2, name: str = "OnePixel"):
        super().__init__(screen, sensor, led1, led2, name)

    def main(self):
        self.screen.fill(color=(0, 0, 0))
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        while True:
            wfi()
            if self.sensor.btnValue("right") == 1:
                self.x += 1
                if self.x >= self.screen_width:
                    self.x = self.screen_width - 1
            elif self.sensor.btnValue("left") == 1:
                self.x -= 1
                if self.x < 0:
                    self.x = 0
            elif self.sensor.btnValue("up") == 1:
                self.y -= 1
                if self.y < 0:
                    self.y = 0
            elif self.sensor.btnValue("down") == 1:
                self.y += 1
                if self.y >= self.screen_height:
                    self.y = self.screen_height - 1
            elif self.sensor.btnValue("b"):
                break

            self.screen.clear(update=False)
            self.screen.pixel(self.x, self.y, color=(255, 255, 255), update=False)
            self.screen.refresh()
