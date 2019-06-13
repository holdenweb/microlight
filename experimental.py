from machine import Pin, PWM
def cycle(wait=0.025):
    from time import sleep
    p = Pin(5, Pin.OUT, Pin.OPEN_DRAIN)
    pwm = PWM(p)
    pwm.freq(50)
    for i in range(64):
        pwm.duty(i*16)
        sleep(wait)
p.on()
sleep(2)
p.off()


from machine import Pin, PWM, ADC, Timer
from time import sleep
adc = ADC(0)
p = Pin(5, Pin.OUT, Pin.OPEN_DRAIN)
pwm = PWM(p)
pwm.freq(50)

def track(wait=0.025):
    while True:
        duty = 1024 - (1024 * (adc.read()-204)/747)
        pwm.duty(int(duty))
        sleep(wait)

#
# When I have to do this I pine for the PyBoard
#
with open('main.py', 'w') as f:
    f.write("""\
# https://docs.micropython.org/en/latest/esp8266/quickref.html#timers
from machine import Pin, PWM, ADC, Timer
from time import sleep
adc = ADC(0)

class Lamp:
    def __init__(self, pin_no):
        self.pin = Pin(pin_no, Pin.OUT, Pin.OPEN_DRAIN)
        self.pwm = PWM(self.pin)
        self.pwm.freq(100)
        self.pwm.duty(1024)
        self.tim = Timer(-1)
        self.tim.init(period=200, mode=Timer.PERIODIC, callback=self.follow)
        self.reading = 0
    def follow(self, se):
        reading = (adc.read()-204)  # Manifest constant?
        if abs(reading-self.reading) > 3:  # Mainfest constant?
            self.reading = reading
            duty = 1024 - (1024 * reading/747)
            self.pwm.duty(int(duty))
    def br(self, n):
        self.pwm.duty(n)

lamp = Lamp(5)
""")

from machine import Pin, PWM, ADC, Timer
from time import sleep
p = Pin(5, Pin.OUT, Pin.OPEN_DRAIN)
pwm = PWM(p)
pwm.freq(50)
for i in range(1024):
    pwm.duty(1023-i)
    sleep(0.05)
