import gc

from pyb import delay, wfi

from empty import EmptyScript
from utils.sprite import Sprite


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 0, 0)
        self.visible = False

    def set_color(self, r, g, b):
        self.color = (r, g, b)

    def render(self, screen, update=True):
        if self.visible:
            print("about to render block rectangle")
            # draw the block
            screen.rect(
                x=self.x * 32,
                y=self.y * 32,
                w=32,
                h=32,
                color=self.color,
                fill=True,
                update=update,
            )


class WalkScript(EmptyScript):
    screen_width = 160
    screen_height = 128

    name = "walk"

    def __init__(self, screen, sensor, led1, led2) -> None:
        self.screen = screen
        self.sensor = sensor
        self.led1 = led1
        self.led2 = led2
        self.changed = True

    def main(self):
        # create 10x8 grid of blocks
        self.grid = [[Block(x, y) for x in range(5)] for y in range(4)]

        # set the bottom row to be visible and brown
        for block in self.grid[-1]:
            block.visible = True
            block.color = (201, 41, 25)

        # create the spite
        self.sprite = Sprite(
            sprite_path="images/Norris.bmp",
            width=16,
            screen=self.screen,
            x=48,
            y=64,
            height=32,
        )

        # main loop
        while True:
            wfi()

            if self.changed:
                # clear the screen
                self.screen.clear(update=False)

                # render the grid
                self.render_blocks()

                # render the sprite
                self.sprite.render()

                self.screen.refresh()
                self.changed = False

            delay(50)

            if self.sensor.btnValue("left"):
                self.sprite.x -= 10
                self.changed = True

            if self.sensor.btnValue("right"):
                self.sprite.x += 10
                self.changed = True

            if self.sensor.btnValue("b"):
                break

    def render_blocks(self):
        for row in self.grid:
            for block in row:
                block.render(self.screen, update=False)
