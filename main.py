from framebuf import RGB565, FrameBuffer
from pyb import LED, SCREEN, wfi

from screen import Screen
from sensor import Sensor
from micropython import const, opt_level

opt_level(3)

# initialize all the components
screen = Screen(
    tft=SCREEN(),
    fb=FrameBuffer(bytearray(const(160 * 128 * 2)), const(160), const(128), RGB565),
)
sensor = Sensor()
led1 = LED(1)
led2 = LED(2)

# clear the screen
screen.clear()

from flags import FlagsScript
from empty import EmptyScript
from one_pixel import OnePixelScript
from brightness import BrightnessScript

scripts = [
    FlagsScript,
    EmptyScript,
    OnePixelScript,
    BrightnessScript,
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
        current_script = scripts[cursor_index](screen, sensor, led1, led2)
        current_script.main()
        del current_script
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
