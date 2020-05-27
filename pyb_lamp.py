# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
#
# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

import utime
from pyb import Pin, Timer
from rotary_irq_pyb import RotaryIRQ

ticks_per_click = 8  # Scaling factor
inter_tick_delay_ms = 10
max_setting = 30
max_demand = max_setting*ticks_per_click
max_drive = max_demand*max_demand

r = RotaryIRQ(pin_num_clk='X1',
              pin_num_dt='X2',
              min_val=0,
              max_val=max_setting,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

switch_pin = Pin('X4', mode=Pin.IN, pull=Pin.PULL_UP)
pwm_pin = Pin('X3') # X3 has TIM2, CH3 on PyBoard
tim = Timer(2, freq=1000)
pwm_ch = tim.channel(3, Timer.PWM, pin=pwm_pin)
pwm_ch.pulse_width_percent(0)

val_old = r.value()

#
# While it would be possible to store the settings in non-volatile
# memory, at present we simply start from zero every time power is
# applied. If the press switch is closed for three ticks in a row
# the lamp is switched off, and when switched on again will fade
# up to the last-asserted setting.
#
val_old = current = pct = 0   # Always fade up at power on
target = 5
r.set(value=target)
running = True
on_off_count = 0

while True:
    utime.sleep_ms(inter_tick_delay_ms)
    if not switch_pin.value():
        on_off_count += 1
        if on_off_count == 3:
            running = not running
            if not running:
                current, incr = 0, 1
                pwm_ch.pulse_width_percent(0)
    else:
        on_off_count = 0

    if running:
        raw_demand = r.value()*ticks_per_click
        if raw_demand != target:  # retargeting required
            target = raw_demand
            incr = 1 if target > current else -1
        if current != target:  # Move towards target
            current += incr
            pct = (current*current/max_drive)*100
            pwm_ch.pulse_width_percent(pct)
