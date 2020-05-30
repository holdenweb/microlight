#
# main.py: create two lamps and run them both
#
import utime

from pyb_lamp import DimmedLight, INTER_TICK_MS

c1 = DimmedLight(
    clk_pin='X1', dt_pin='X2', switch_pin='X4', pwm_pin='X3', timer=2, channel=3
)
c2 = DimmedLight(
    clk_pin='X5', dt_pin='X6', switch_pin='X8', pwm_pin='X7', timer=13, channel=1
)

while True:
    utime.sleep_ms(INTER_TICK_MS)
    for channel in (c1, c2):
        channel.tick()
