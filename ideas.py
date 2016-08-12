"""
ideas.py: just kicking a few ideas around to see if I can understand what I am doing.

The Ticker is the scheduler class. On a live system its tick() method should be called periodically. The periodicity
of the ticks willd determine the speed of operation, assuming that the CPU is not so heavily loaded that interrupts
can no longer be serviced in a timely fashion.

The lighting is a prototype light channel controller, which should probably be a subset of some basic type that knows
how to interact with the Ticker (if it needs to).

"""
class Ticker:
    def __init__(self, ticker):
        print("About to start handling tick timer")
        self.irq = ticker.irq(handler=self.tick, trigger=Timer.TIMEOUT)
        self.tasks = set()
        self.time = 0
    def add(self, task):
        self.tasks.add(task)
    def remove(self, task):
        self.tasks.remove(task)
    def tick(self, peripheral): # This gets scheduled once every ten milliseconds
        """Look carefully - uses heap, should maybe find another technique"""
        self.time += 1
        done = set()
        for task in self.tasks:
            if task.tick_handler():
                done.add(task)
        for task in done:
            self.remove(task)
        self.irq.enable()
        # Do we need to re-enable this IRQ?
        # Should I therefore have a method to create the
        # IRQ and store it as an instance attribute.

print("Scheduler declared")
print("About to establish hardware control")
from machine import Timer
tim0 = Timer(0, mode=Timer.PWM)
ch = tim0.channel(Timer.A, freq=500, polarity=Timer.POSITIVE, duty_cycle=100)
mstimer = Timer(1, mode=Timer.PERIODIC, width=16)
ticker = mstimer.channel(Timer.A, freq=100)

scheduler = Ticker(ticker)
print("Scheduler created")

class Lighting:
    def __init__(self, name, scheduler=scheduler):
        self.name = name
        self.scheduler = scheduler
        self.current = self.target = self.start = self.tick_num = self.interval = 0
    def fadeto(self, value, interval=20):
        self.start = self.current
        self.target = value
        self.interval = interval
        self.tick_num = 0
        self.scheduler.add(self)
    def tick_handler(self):
        self.tick_num += 1
        self.current = self.start+((self.target-self.start)*self.tick_num)//self.interval
        ch.duty_cycle(self.current)
        return self.current == self.target

lg1 = Lighting("one")
lg1.fadeto(10000, interval=1000)
for i in range(25):
    print("About to sssssleep")
import time
time.sleep(5)
print("Woke up")