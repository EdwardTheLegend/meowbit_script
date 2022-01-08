class Script:
    def __init__(self, screen, sensor, led1, led2, name: str = "Script") -> None:
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2

        self.screen_width = 160
        self.screen_height = 128

        self.name = name

    def main(self):
        self.screen.text(text="this is just the default script", x=0, y=0)