from framebuf import RGB565, FrameBuffer
from pyb import LED, SCREEN, wfi

import flags
import empty

from screen import Screen
from sensor import Sensor
from micropython import const

# initialize all the components
screen = Screen(
    tft=SCREEN(),
    fb=FrameBuffer(bytearray(160 * 128 * 2), 160, 128, RGB565),
)
sensor = Sensor()
led1 = LED(1)
led2 = LED(2)

# clear the screen
screen.clear()

give_to_scripts = [screen, sensor, led1, led2]

scripts = [
    flags.FlagsScript(*give_to_scripts),
    empty.EmptyScript(*give_to_scripts),
    flags.FlagsScript(*give_to_scripts),
    empty.EmptyScript(*give_to_scripts),
]

# menu system
cursor_index = 0
menu_spacing = const(12)
updated = True
while True:
    wfi()
    if sensor.btnValue("up"):
        cursor_index = (cursor_index - 1) % len(scripts)
        updated = True
    elif sensor.btnValue("down"):
        cursor_index = (cursor_index + 1) % len(scripts)
        updated = True
    elif sensor.btnValue("a"):
        scripts[cursor_index].main()
        screen.clear()
        updated = True

    if updated:
        for i in range(len(scripts)):
            if i == cursor_index:
                screen.text(
                    text="[_] " + scripts[i].name,
                    x=0,
                    y=(i * menu_spacing),
                    update=False,
                )
            else:
                screen.rect(
                    x=8,
                    y=(i * menu_spacing),
                    w=8,
                    h=menu_spacing,
                    color=(0, 0, 0),
                    fill=True,
                    update=False,
                )
                screen.text(
                    text="[ ] " + scripts[i].name, x=0, y=i * menu_spacing, update=False
                )

        screen.refresh()
        updated = False
