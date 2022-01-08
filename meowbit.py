#
import math
import pyb, os
import framebuf
from screen import Screen
from sensor import Sensor
from pyb import Pin, Timer, delay #, ADC, Servo, UART
from time import ticks_ms
from micropython import const

noteMap = [440, 494, 262, 294, 330, 349, 392]

CORRECT = "c6:1 f6:2"
NOTICE = "d5:1 b4:1"
ERROR = "a3:2 r a3:2"
DADADADUM = "r4:2 g g g eb:8 r:2 f f f d:8 "
ENTERTAINER = "d4:1 d# e c5:2 e4:1 c5:2 e4:1 c5:3 c:1 d d# e c d e:2 b4:1 d5:2 c:4 "
PRELUDE = "c4:1 e g c5 e g4 c5 e c4 e g c5 e g4 c5 e c4 d g d5 f g4 d5 f c4 d g d5 f g4 d5 f b3 d4 g d5 f g4 d5 f b3 d4 g d5 f g4 d5 f c4 e g c5 e g4 c5 e c4 e g c5 e g4 c5 e "
ODE = "e4 e f g g f e d c c d e e:6 d:2 d:8 e:4 e f g g f e d c c d e d:6 c:2 c:8 "
NYAN = "f#5:2 g# c#:1 d#:2 b4:1 d5:1 c# b4:2 b c#5 d d:1 c# b4:1 c#5:1 d# f# g# d# f# c# d b4 c#5 b4 d#5:2 f# g#:1 d# f# c# d# b4 d5 d# d c# b4 c#5 d:2 b4:1 c#5 d# f# c# d c# b4 c#5:2 b4 c#5 b4 f#:1 g# b:2 f#:1 g# b c#5 d# b4 e5 d# e f# b4:2 b f#:1 g# b f# e5 d# c# b4 f# d# e f# b:2 f#:1 g# b:2 f#:1 g# b b c#5 d# b4 f# g# f# b:2 b:1 a# b f# g# b e5 d# e f# b4:2 c#5 "
RINGTONE = "c4:1 d e:2 g d:1 e f:2 a e:1 f g:2 b c5:4 "
FUNK = "c2:2 c d# c:1 f:2 c:1 f:2 f# g c c g c:1 f#:2 c:1 f#:2 f d# "
BLUES = "c2:2 e g a a# a g e c2:2 e g a a# a g e f a c3 d d# d c a2 c2:2 e g a a# a g e g b d3 f f2 a c3 d# c2:2 e g e g f e d "
BIRTHDAY = "c4:3 c:1 d:4 c:4 f e:8 c:3 c:1 d:4 c:4 g f:8 c:3 c:1 c5:4 a4 f e d a#:3 a#:1 a:4 f g f:8 "
WEDDING = "c4:4 f:3 f:1 f:8 c:4 g:3 e:1 f:8 c:4 f:3 a:1 c5:4 a4:3 f:1 f:4 e:3 f:1 g:8 "
FUNERAL = "c3:4 c:3 c:1 c:4 d#:3 d:1 d:3 c:1 c:3 b2:1 c3:4 "
PUNCHLINE = "c4:3 g3:1 f# g g#:3 g r b c4 "
BADDY = "c3:3 r d:2 d# r c r f#:8 "
CHASE = "a4:1 b c5 b4 a:2 r a:1 b c5 b4 a:2 r a:2 e5 d# e f e d# e b4:1 c5 d c b4:2 r b:1 c5 d c b4:2 r b:2 e5 d# e f e d# e "
BA_DING = "b5:1 e6:3 "
WAWAWAWAA = "e3:3 r:1 d#:3 r:1 d:4 r:1 c#:8 "
JUMP_UP = "c5:1 d e f g "
JUMP_DOWN = "g5:1 f e d c "
POWER_UP = "g4:1 c5 e g:2 e:1 g:3 "
POWER_DOWN = "g5:1 d# c g4:2 b:1 c5:3 "

class Buzz():
    def __init__(self):
        pinbz = Pin('BUZZ')
        self.tim = Timer(4, freq=3000)
        self.ch = self.tim.channel(3, Timer.PWM, pin=pinbz)
        self.playing = 0

    def tone(self,freq, d=1000):
        if freq == 0:
            delay(d)
            return
        self.tim.freq(freq)
        self.ch.pulse_width_percent(30)
        delay(d)
        self.ch.pulse_width_percent(0)

    def note(self, note, rest):
        d = int(rest*1000)
        freq = int(440.0*math.pow(2, (note-69)/12))
        self.tone(freq,d)

    def rest(self, rest):
        d = int(rest*1000)
        delay(d)

    def melody(self,m,bpm=120):
        m = m.lower()
        if not m.endswith(' '):
            m = m+' '
        octave = 4
        n = 0
        tnote = int(60/bpm*1000/4)
        duration=500
        self.playing = 1
        while n < len(m):
            if not self.playing:
                return
            note = ord(m[n])
            if note >= ord('a') and note <= ord('g'):
                freq = noteMap[note-ord('a')]
            elif note == ord('r'):
                freq = 0
            elif note >= ord('2') and note <= ord('6'):
                octave = note - ord('0')
            elif note == ord(':'):
                n+=1
                note = ord(m[n])
                duration = (note - ord('0'))*tnote
            elif note == ord(' '):
                freq *= pow(2, octave-4)
                self.tone(freq, duration)
            n+=1

    def stop(self):
        self.playing = 0
        self.ch.pulse_width_percent(0)

fbuf = bytearray(160*128*2)
fb = framebuf.FrameBuffer(fbuf, 160, 128, framebuf.RGB565)
tft = pyb.SCREEN()
buzzer = Buzz()

try:
    os.stat("boot.bmp")
    fb.loadbmp("boot.bmp")
    tft.show(fb)
except:
    fb.fill(0)
    fb.text("Hello world",5,10,0x80cda5)
    tft.show(fb)

from turtle import Turtle
turtle = Turtle(tft, fb)
screen = Screen(tft, fb)
sensor = Sensor()
led1 = pyb.LED(1)
led2 = pyb.LED(2)

