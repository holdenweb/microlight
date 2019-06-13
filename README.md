This project records the MicroPython software development for a dimmable
LED controller for 12-24v lamps.

Dimmable DC lamps use a driver chip to achieve a constant current through
the LEDs. Dimming is achieved by driving the LEDs with pulse-width
modulated DC current at a frequency that makes the flicker imperceptible.
Annoyingly the internal chip has an unused enable input that remains
inaccessible, so similar circuitry has to be duplicated externally.



