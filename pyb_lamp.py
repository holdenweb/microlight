# The MIT License (MIT)
# Copyright (c) 2020 Steve Holden
# https://opensource.org/licenses/MIT
#
# Control PWM lamps in MicroPython with a rotary encoder.
#
# Thanks to Mike Teachman for an exemplary rotary encoder driver.
#   https://github.com/MikeTeachman/micropython-rotary
#
# While it would be possible to store settings in non-volatile memory, at
# present we simply start from a fixed value every time power is applied. If
# the press switch is closed for three ticks in a row the lamp is switched
# off, and when switched on again will fade up to the last-asserted setting.
#
from pyb import Pin
from pyb import Timer
from rotary_irq_pyb import RotaryIRQ

TICKS_PER_CLICK = 8  # Scaling factor
INTER_TICK_MS = 10
MAX_SETTING = 30
MAX_DEMAND = MAX_SETTING * TICKS_PER_CLICK
MAX_DRIVE = MAX_DEMAND * MAX_DEMAND
INITIAL_TARGET = 5
DEBOUNCE_TICKS = 3


class DimmedLight:
    """
    Controls a PWM output using three input pins connected to a rotary
    encoder.

    The clk_pin and dt_pin inputs are used to create the RotaryIRQ object
    that provides an integer value for the intensity setting. The switch_pin
    input provides on/off control for the channel. These control the PWM
    output at the pwm_pin driven by a timer channel created for the purpose.
    """

    def __init__(
        self,
        clk_pin="X1",
        dt_pin="X2",
        switch_pin="X4",
        pwm_pin="X3",
        timer=2,
        channel=3,
    ):
        """
        Establish pin functions, create rotary control and initialise tick
        response.
        """
        self.switch_pin = Pin(switch_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pwm_pin = Pin(pwm_pin)  # X3 has TIM2, CH3 on PyBoard
        self.tim = Timer(timer, freq=1000)
        self.pwm_ch = self.tim.channel(channel, Timer.PWM, pin=self.pwm_pin)
        self.pwm_ch.pulse_width_percent(0)
        self.r = RotaryIRQ(
            clk_pin,
            dt_pin,
            max_val=MAX_SETTING,
            reverse=True,
            range_mode=RotaryIRQ.RANGE_BOUNDED,
        )
        self.on_off_count = self.current = 0  # Always fade up at power on
        self.target = INITIAL_TARGET
        self.running = True
        self.incr = 1
        self.r.set(value=self.target)

    def tick(self):
        """
        Debounce switch pin, actioning when the switch is pressed (zero)
        three ticks in a row.

        This routine should be called periodically for each lamp in the bank.
        The calls should be relatively frequent and regular, as each tick triggers an
        increment in the lamp brightness while proceeding towards a new target.
        """
        if not self.switch_pin.value():
            self.on_off_count += 1
            # After DEBOUNCE_TICKS cycles, action a press on the switch.
            # Otherwise just count uselessly until the switch is re-opened.
            if self.on_off_count == DEBOUNCE_TICKS:
                self.running = not self.running
                if not self.running:
                    print("Suspending", self.pwm_pin)
                    self.current, self.incr = 0, 1
                    self.pwm_ch.pulse_width_percent(0)
        else:
            self.on_off_count = 0

        if self.running:
            demand = self.r.value() * TICKS_PER_CLICK
            # retargeting required ?
            if demand != self.target:
                print("New target:", demand)
                self.target = demand
                self.incr = 1 if self.target > self.current else -1
            # Move towards target unless already there
            if self.current != self.target:
                self.current += self.incr
                pct = (self.current * self.current / MAX_DRIVE) * 100
                self.pwm_ch.pulse_width_percent(pct)
