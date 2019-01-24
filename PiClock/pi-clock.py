#!/usr/bin/env python

"""
author = "Joshua Marsden"
email  = "%s%s@%s" % ("joshua", "marsden", "gmail.com")
src    = "https://raspi.tv/2015/how-to-drive-a-7-segment-display-directly-on-raspberry-pi-in-python"
"""

import RPi.GPIO as GPIO # For pin control
import time             # For display timing

GPIO.setmode(GPIO.BCM)  # Not to be confused with the WPi numbering system
GPIO.setwarnings(False) # Because it gets annoying


def show_num(digit, num, dp=False):
    """
        Given a digit place and integer to represent, send the necessary signals
        to the correct 7-segment display.
    """
    # GPIO ports mapped to 7-seg segment names
    segments = {'a':8, 'b':10, 'c':23, 'd':27, 'e':17, 'f':25, 'g':24, 'dp':22}

    # Each code corresponds to a sequence of characters referencable in the segments
    # dictionary.
    numcode = {' ': '',
               '0': 'abcdef',
               '1': 'bc',
               '2': 'abdeg',
               '3': 'abcdg',
               '4': 'bcfg',
               '5': 'acdfg',
               '6': 'acdefg',
               '7': 'abc',
               '8': 'abcdefg',
               '9': 'abcdfg'}

    # GPIO ports for digit selection
    # In order: 1, 2, 3, 4
    dselect = (15, 3, 2, 14)

    # Set GPIO pin modes to OUT
    for segment in segments:
        GPIO.setup(segments[segment], GPIO.OUT)
        GPIO.output(segments[segment], 0)
    for digit in dselect:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 1)

    for seg in segments:
        if seg in numcode[num]:
            GPIO.output(segments[seg], 1)
        else:
            GPIO.output(segments[seg], 0)
        if dp:
            GPIO.output(segments['dp'], 1)
        else:
            GPIO.output(segments['dp'], 0)
    # Remember, digit selection is anode (opposite)
    GPIO.output(dselect[digit], 0)
    # Give the 7-seg a moment to breathe
    time.sleep(0.001)
    # Deselect the digit when done
    GPIO.output(dselect[digit], 1)

    return True
# End of show_num


def display_time(hh, mm, ss, mode=12):
    """ Displays the given hour and minute to a 4-digit 7-segment display. """
    pm = hh // 12 if mode == 12 else 0

    # Only bother with 12-hour format conversion if mode is set
    if mode == 12:
        hh %= 12
        hh = ((12 - hh) // 12) * 12 + hh

    hh = "%2d" % (hh)
    mm = "%02d" % (mm)

    show_num(0, hh[0])
    show_num(1, hh[1], ss % 2)
    show_num(2, mm[0])
    show_num(3, mm[1], pm)


    #print("current time: %s:%s"% (hh, mm))

    return True
# End of display_time


if __name__ == "__main__":
    try:
        while True:
            #update_time()
            h, m, s = time.localtime()[3:6]
            display_time(h, m, s)
            time.sleep(0.01)
    finally:
        print("\ncleaning up.")
        GPIO.cleanup()
