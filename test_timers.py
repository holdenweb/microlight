import time

from pyb import Pin
from pyb import Timer

#
# Data as list of (pin_name, timer_no, channel)
#
data = [
    ("Y1", 8, 1),
    ("Y2", 8, 2),
    ("Y3", 4, 3),
    ("Y3", 10, 1),
    ("Y4", 4, 4),
    ("Y4", 11, 1),
    ("Y7", 12, 1),
    ("Y8", 12, 2),
    ("X9", 4, 1),
    ("Y1O", 2, 4),
    ("Y9", 2, 3),
    ("X8", 14, 1),
    ("X7", 13, 1),
    ("X6", 2, 1),
    ("X4", 9, 2),
    ("X4", 5, 4),
    ("X4", 2, 4),
    ("X3", 9, 1),
    ("X3", 5, 3),
    ("X3", 2, 3),
    ("X2", 5, 2),
    ("X2", 2, 2),
    ("X1", 5, 1),
    ("X1", 2, 1),
]

# workable_configs = [
# ('Y1', 8, 1),
# ('Y2', 8, 2),
# ('Y3', 4, 3),
# ('Y3', 10, 1),
# ('Y4', 4, 4),
# ('Y4', 11, 1),
# ('Y7', 12, 1),
# ('Y8', 12, 2),
# ('X9', 4, 1),
# ('Y9', 2, 3),
# ('X8', 14, 1),
# ('X7', 13, 1),
# ('X6', 2, 1),
# ('X4', 9, 2),
# ('X4', 5, 4),
# ('X4', 2, 4),
# ('X3', 9, 1),
# ('X3', 5, 3),
# ('X3', 2, 3),
# ('X2', 5, 2),
# ('X2', 2, 2),
# ('X1', 5, 1),
# ('X1', 2, 1),
# ]


# PybLite
data_lite = [
    ("Y1", 3, 1),
    ("Y2", 3, 2),
    ("Y3", 2, 3),
    ("Y4", 4, 4),
    ("Y4", 11, 1),
    ("X9", 4, 1),
    ("X10", 4, 2),
    ("Y12", 3, 4),
    ("Y11", 3, 3),
    ("Y10", 10, 1),
    ("Y10", 4, 3),
    ("Y9", 1, 1),
    ("X8", 3, 2),
    ("X7", 3, 1),
    ("X6", 2, 1),
    ("X4", 5, 2),
    ("X4", 2, 2),
    ("X3", 5, 1),
    ("X3", 2, 1),
    ("X2", 9, 2),
    ("X2", 5, 4),
    ("X2", 2, 4),
    ("X1", 9, 1),
    ("X1", 5, 3),
    ("X1", 2, 3),
]

s_list = []
for d_t in data:
    pname, tnum, chnum = d_t
    try:
        print(pname, tnum, chnum, end=": ")
        p = Pin(pname)
        tim = Timer(tnum, freq=1000)
        ch = tim.channel(chnum, Timer.PWM, pin=p)
        ch.pulse_width_percent(50)
        s_list.append((pname, tnum, chnum))
        print("running")
    except Exception as e:
        print("Error -", e)
    time.sleep(2)
print("Workable configs:\n", s_list)
