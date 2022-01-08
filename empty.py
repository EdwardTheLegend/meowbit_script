from script import Script
from pyb import wfi

class EmptyScript(Script):
    def __init__(self, *args) -> None:
        super().__init__(*args, name="Empty")

    # main function
    def main(self):
        self.screen.fill((255, 255, 255))
        self.screen.text(text="press b to go back", x=0, y=0, color=(0, 100, 0))
        while True:
            wfi()
            if self.sensor.btnValue("b"):
                break

