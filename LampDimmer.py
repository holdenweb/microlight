import micropython
from pyb import ADC
from pyb import Pin
from pyb import Timer

# micropython.alloc_emergency_exception_buf(250)
#
# PyBoard implementation
#

#
# Set various fundamental parameters
#
# Hardware
#
# PWM specific#tions
PWM_PIN = Pin("X1")
PWM_TIMER_NO = 2
PWM_TIMER_CHANNEL = 3
#
# Tick Timer
#
TICK_TIMER = Timer(4, freq=2)
#
# Lowest and highest possible ADC values, these values to be
# determined by observation. The input is clamped within this
#
ADC_PIN_NAME = "X11"
CTRL_ADC = ADC(ADC_PIN_NAME)
ADC_LEVELS = 4096
ADC_MIN = 50
ADC_MAX = ADC_LEVELS - 50
ADC_RANGE = ADC_MAX - ADC_MIN
#
# Size of increments towards target per tick
#
INCREMENT = 0.025
#
# `Amount demand must change before being actioned
#
D_DELTA = 1 / 64


class DimmerLamp:
    def __init__(
        self, adc=CTRL_ADC, p_pin=PWM_PIN, t_num=PWM_TIMER_NO, chnum=PWM_TIMER_CHANNEL
    ):
        self.adc = adc
        dim_tim = Timer(t_num, freq=1000)
        self.ch = dim_tim.channel(chnum, Timer.PWM, pin=p_pin)
        self.current = self.increment = self.target = self.ticks_left = 0
        self.tr = self.tick_response

    def tick(self, arg):
        "Read the ADC and schedule the tick response."
        # struct.pack_into(B_FMT, self.adc_val, 0, self.adc.read())
        micropython.schedule(self.tr, None)

    def tick_response(self, _):
        """
        Sample ADC input to set new target if necessary,
        then increment current value towards target.
        Scales current value and sets PWM percentage.
        """
        adc_val = self.adc.read()
        if adc_val < ADC_MIN:
            adc_val = ADC_MIN
        if adc_val > ADC_MAX:
            adc_val = ADC_MAX
        demand = (adc_val - ADC_MIN) / ADC_RANGE
        print(self.target - demand)
        if abs(self.target - demand) > D_DELTA:
            print(self.target, demand, self.current)
            self.target = demand
            gap = demand - self.current
            self.increment = INCREMENT if gap > 0 else -INCREMENT
            self.ticks_left = int(gap / self.increment)
        if self.ticks_left:
            self.ticks_left -= 1
            self.current += INCREMENT
            print(self.ticks_left)
            self.ch.pulse_width_percent(100 * self.current * self.current)


d = DimmerLamp()

TICK_TIMER.callback(d.tick)
