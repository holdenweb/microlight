import micropython
from machine import Timer

micropython.alloc_emergency_exception_buf(100)

index = 0


def cb(t):
    global index
    index += 1
    return


tim4 = Timer(1, mode=Timer.PERIODIC, width=16)
chan = tim4.channel(Timer.A, freq=10)
chan.irq(trigger=Timer.TIMEOUT, handler=cb)
