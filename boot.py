# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import machine
import pyb, time

pyb.country("US")  # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU
pyb.main("main.py")  # main script to run after this one
