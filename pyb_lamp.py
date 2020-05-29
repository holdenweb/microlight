# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT
#
# example for MicroPython rotary encoder
#
# Rotary Encoder Documentation:x
#   https://github.com/MikeTeachman/micropython-rotary
#
# While it would be possible to store the settings in non-volatile
# memory, at present we simply start from zero every time power is
# applied. If the press switch is closed for three ticks in a row
# the lamp is switched off, and when switched on again will fade
# up to the last-asserted setting.
#
import utime
from pyb import Pin, Timer
from rotary_irq_pyb import RotaryIRQ

TICKS_PER_CLICK = 8  # Scaling factor
INTER_TICK_MS = 10
MAX_SETTING = 30
MAX_DEMAND = MAX_SETTING * TICKS_PER_CLICK
MAX_DRIVE = MAX_DEMAND * MAX_DEMAND
INITIAL_TARGET = 5


class DimmedLight:
    def __init__(
        self,
        clk_pin='X1',
        dt_pin='X2',
        switch_pin='X4',
        pwm_pin='X3',
        timer=2,
        channel=3,
    ):
        self.switch_pin = Pin(switch_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pwm_pin = Pin(pwm_pin)  # X3 has TIM2, CH3 on PyBoard
        self.tim = Timer(2, freq=1000)
        self.pwm_ch = self.tim.channel(3, Timer.PWM, pin=self.pwm_pin)
        self.pwm_ch.pulse_width_percent(0)

        self.on_off_count = self.current = 0  # Always fade up at power on
        self.target = INITIAL_TARGET
        self.running = True
        self.incr = 1
        self.r = RotaryIRQ(
            clk_pin,
            dt_pin,
            max_val=MAX_SETTING,
            reverse=True,
            range_mode=RotaryIRQ.RANGE_BOUNDED,
        )
        self.r.set(value=self.target)

    def tick(self):
        if not self.switch_pin.value():
            self.on_off_count += 1
            if self.on_off_count == 3:
                self.running = not self.running
                if not self.running:
                    self.current, self.incr = 0, 1
                    self.pwm_ch.pulse_width_percent(0)
        else:
            self.on_off_count = 0

        if self.running:
            raw_demand = self.r.value() * TICKS_PER_CLICK
            if raw_demand != self.target:  # retargeting required
                self.target = raw_demand
                self.incr = 1 if self.target > self.current else -1
            if self.current != self.target:  # Move towards target
                self.current += self.incr
                pct = (self.current * self.current / MAX_DRIVE) * 100
                self.pwm_ch.pulse_width_percent(pct)


c1 = DimmedLight(
    clk_pin='X1', dt_pin='X2', switch_pin='X4', pwm_pin='X3', timer=2, channel=3
)

while True:
    utime.sleep_ms(INTER_TICK_MS)
    c1.tick()
