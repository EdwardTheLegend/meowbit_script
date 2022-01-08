from script import Script


class FlagsScript(Script):
    def __init__(self, *args) -> None:
        super().__init__(*args, name="Flags")

        self.flags_list = [self.france, self.japan, self.italy]
        self.flag_index = 0

    def japan(self):
        self.screen.fill((255, 255, 255))
        self.screen.circle(80, 64, 40, (255, 0, 0), (0, 255, 0))

    def france(self):
        self.screen.fill((255, 255, 255))
        self.screen.rect(
            0, 0, self.screen_width // 3, self.screen_height, (0, 0, 255), (0, 0, 255)
        )
        self.screen.rect(
            (self.screen_width // 3) * 2,
            0,
            self.screen_width // 3,
            self.screen_height,
            (255, 0, 0),
            (255, 0, 0),
        )

    def italy(self):
        self.screen.fill((255, 255, 255))
        self.screen.rect(
            0, 0, self.screen_width // 3, self.screen_height, (0, 255, 0), (0, 255, 0)
        )
        self.screen.rect(
            (self.screen_width // 3) * 2,
            0,
            self.screen_width // 3,
            self.screen_height,
            (255, 0, 0),
            (255, 0, 0),
        )

    # main function
    def main(self):
        self.flags_list[self.flag_index]()
        while True:
            if self.sensor.btnValue("right") == 1:
                print("right")
                self.flag_index = (self.flag_index + 1) % len(self.flags_list)
                self.flags_list[self.flag_index]()
            elif self.sensor.btnValue("left") == 1:
                print("left")
                self.flag_index = (self.flag_index - 1) % len(self.flags_list)
                self.flags_list[self.flag_index]()
            elif self.sensor.btnValue("b"):
                break
