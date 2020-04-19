# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
#
# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

import time
from pyb import Pin, Timer
from rotary_irq_pyb import RotaryIRQ

ticks_per_click = 8  # Scaling factor
inter_tick_delay_ms = 10
max_setting = 30
max_demand = max_setting*ticks_per_click
max_drive = max_demand*max_demand

current = 0  # Always fade up at power on

r = RotaryIRQ(pin_num_clk='X1',
              pin_num_dt='X2',
              min_val=0,
              max_val=max_setting,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

p = Pin('X3') # X3 has TIM2, CH1
tim = Timer(2, freq=1000)
pwm_ch = tim.channel(1, Timer.PWM, pin=p)
pwm_ch.pulse_width_percent(0)

val_old = r.value()

#
# While it would be possible to store the settings in non-volatile
# memory, at present we simply start from zero every time.
#
val_old = current = target = pct = 0

while True:
    raw_demand = r.value()*ticks_per_click
    if raw_demand != target:  # retargeting required
        target = raw_demand
        incr = 1 if target > current else -1
#        print("Now", current, "incrementing by", incr, "to", target)
    if current != target:  # Move towards target
        current += incr
        pct = (current*current/max_drive)*100
        pwm_ch.pulse_width_percent(pct)
#    print(target, current, pct)
    time.sleep_ms(inter_tick_delay_ms)
