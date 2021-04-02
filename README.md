# MicroLight

This project uses MicroPython on a PyBoard to control a dimmable LED
controller for 12-24v lamps using PWM.

## Operating Principles

Dimmable DC lamps use a driver chip to achieve a constant current through the
LEDs. Dimming is achieved by driving the LEDs to full intensity with
pulse-width modulated DC current at a frequency that makes the flicker
imperceptible. Annoyingly the driver chip in some lamps has an unused enable
input that remains inaccessible inside, because it is used only for current
limiting. Consequently, similar circuitry has to be duplicated externally.

A PyBoard periodically adjusts the light levels in response to
interrupt-driven inputs from two rotary encoders with push switches.

## Conclusion

The PyBoard was not chosen for its cost, but rather because it is a
reliable, expandable easy-to-use component for hobbyists. The design should
easily adapt to other MicroPython hardware. Although at present the rotary
encoder software supports only PyBoard and the ESP8266 and ESP32
implementations, this covers quite a range of microcontrollers.

While the example PyBoard code controls two channels, the `main.py` file is
simply adjusted to create any number of channels for which you have hardware support.
Each channel's tick method is then called in a timed loop to scan for input
changes and adjust the light level if necessary. The typical single LED lamp
draws less than 1A from a 12V supply, but the channel driver circuit above is capable
(with appropriate heat sinking) of handling loads up to 60A, allowng systems of
all sizes to be configured.
