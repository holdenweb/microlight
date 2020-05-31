This project records the MicroPython software development for a dimmable
LED controller for 12-24v lamps.

Dimmable DC lamps use a driver chip to achieve a constant current through
the LEDs. Dimming is achieved by driving the LEDs with pulse-width
modulated DC current at a frequency that makes the flicker imperceptible.
Annoyingly the internal driver chip has an unused enable input that remains
inaccessible inside the lamp, since it is used only for current limiting,
so similar circuitry has to be duplicated externally.

I chose the PyBoard primarily because of the resolution of the DAC
outputs. This may have been an irrational decision.
It certinly wasn't a cost-based one!
