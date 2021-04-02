import gc
from time import sleep

import micropython
from pyb import ExtInt
from pyb import Pin

enc_tbl = 0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0

# extint = pyb.ExtInt(pin, mode, pull, callback)
count = state = 0

micropython.alloc_emergency_exception_buf(250)


def int_cb(_):
    micropython.schedule(cb, None)


def cb(_):
    global count, state
    new_state = ((state << 2) + (CLK.value() << 1) + DAT.value()) & 0xF
    val = enc_tbl[new_state]
    if val:
        count += val
        state = new_state


CLK = Pin("X1", Pin.IN, Pin.PULL_UP)
DAT = Pin("X2", Pin.IN, Pin.PULL_UP)

ExtInt(CLK, ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, int_cb)
ExtInt(DAT, ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, int_cb)

print("Ready")
while True:
    sleep(2.0)
    print(count)
    gc.collect()
