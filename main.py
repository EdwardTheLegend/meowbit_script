from framebuf import RGB565, FrameBuffer
from pyb import LED, SCREEN, wfi

from screen import Screen
from sensor import Sensor
from micropython import const, opt_level
import gc

opt_level(3)
gc.threshold(700)

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

scripts = [
    ["flags", "FlagsScript"],
    ["empty", "EmptyScript"],
    ["one_pixel", "OnePixelScript"],
    ["brightness", "BrightnessScript"],
    ["one_sprite", "OneSpriteScript"],
    ["example_bmp", "ExampleBMPScript"],
    ["scrolling_background", "ScrollingBackgroundScript"],
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
        exec("from " + scripts[cursor_index][0] + " import " + scripts[cursor_index][1])
        print(
            "from " + scripts[cursor_index][0] + " import " + scripts[cursor_index][1]
        )
        current_script = eval(scripts[cursor_index][1] + "(screen, sensor, led1, led2)")
        print(gc.mem_free())
        print(gc.mem_alloc())
        try:
            current_script.main()
        except Exception as e:
            print(current_script.name, "crashed")
            print(e)
        finally:
            del current_script
            exec("del " + scripts[cursor_index][1])
            gc.collect()
            # print(dir())
        screen.clear()
        updated = True

    if updated:
        for i in range(len(scripts)):
            if i == cursor_index:
                screen.text(
                    text="[_] " + scripts[i][0],
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
                    text="[ ] " + scripts[i][0], x=0, y=i * menu_spacing, update=False
                )

        screen.refresh()
        updated = False
