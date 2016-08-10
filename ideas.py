"""
ideas.py: just kicking a few ideas around to see if I can understand what I am doing.

The Ticker is the scheduler class. On a live system its tick() method should be called periodically. The periodicity
of the ticks willd determine the speed of operation, assuming that the CPU is not so heavily loaded that interrupts
can no longer be serviced in a timely fashion.

The lighting is a prototype light channel controller, which should probably be a subset of some basic type that knows
how to interact with the Ticker (if it needs to).

"""
class Ticker:
    def __init__(self):
        self.tasks = set()
        self.time = 0
    def add(self, task):
        self.tasks.add(task)
    def remove(self, task):
        self.tasks.remove(task)
    def tick(self): # This gets scheduled once a millisecond (or thereabouts)
        self.time += 1
        print("====", self.time, "====")
        done = set()
        for task in self.tasks:
            if task.tick_handler():
                done.add(task)
        for task in done:
            self.remove(task)

scheduler = Ticker()

class Lighting:
    def __init__(self, name, scheduler=scheduler):
        self.name = name
        self.scheduler = scheduler
        self.current = self.target = self.start = self.ticknum = self.interval = 0
    def fadeto(self, value, interval=20):
        self.start = self.current
        self.target = value
        self.interval = interval
        self.tick_num = 0
        self.scheduler.add(self)
    def tick_handler(self):
        for i in range(self.interval):
            self.tick_num += 1
            self.current = self.start+((self.target-self.start)*self.tick_num)//self.interval
            print("[][][]", self.name, "==>", self.current)
            return self.current == self.target

lg1 = Lighting("one")
lg2 = Lighting("two")
lg3 = Lighting("three")
lg1.fadeto(500, interval=30)
lg2.fadeto(5000)
lg3.fadeto(1000, interval=10)

while scheduler.tasks:
    scheduler.tick()