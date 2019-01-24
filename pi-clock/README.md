The Pi Clock
---

![Pi Clock Front Picture](https://github.com/JoshMarsden/python-projects/blob/master/pi-clock/photos/pi-clock-front.jpg)

## Contents

* [Materials Necessary](#materials-necessary)
* [Wiring](#wiring)
    - [Pin Connection Table](#pin-connection-table)
    - [7-segment display pinout](#7-segment-display-pinout)
    - [Pro tip - gpio readall](#pro-tip---gpio-readall)
* [Running Headless](#running-headless)
* [Code Commentary](#code-commentary)

## Inspiration

It has occurred to me that a clock in my room is a must-have. So much time can be 
wasted from checking either the nearest phone or computer screen as the 
distractions are inevitable. I know, it's a small thing, but to me it makes a 
huge difference. Also, it's nice to have a simple project like this by which I 
can hone my electronics and programming skills.

[^ back to top]

## Materials Necessary

* Raspberry Pi 2 or 3 _($35 new)_
* 16GB SD card _(~$25 for pack of 5)_
* 4-digit 7-segment anode module SH5461AS _(~$2)_
* 12 jumper wires (male to female) _(common in kits)_
* 8 resistors (220 or 100 ohms) _(common in kits)_
* Breadboard _($1-3)_
* Box of some kind to house the clock

## Wiring

![Fritzing wiring diagram screenshot](https://github.com/JoshMarsden/python-projects/blob/master/pi-clock/photos/fritzing-screenshot.png)

### Pin Connection Table

Segment/Digit | 7-seg pin | resistor? | GPIO# (BCM)
------------- | --------- | --------- | -----------
bot left (e) | 1 | Yes | 17
bottom (d) | 2 | Yes | 27
dot (dp) | 3 | Yes | 22
bot right (c) | 4 | Yes | 23
middle (g) | 5 | Yes | 24
DIGIT 4 | 6 | No | 14
top right (b) | 7 | Yes | 10
DIGIT 3 | 8 | No | 2
DIGIT 2 | 9 | No | 3
top left (f) | 10 | Yes | 25
top (a) | 11 | Yes | 8
DIGIT 1 | 12 | No | 15

### 7-segment display pinout

![7-segment display pinout drawing](https://github.com/JoshMarsden/python-projects/blob/master/pi-clock/photos/7-segment-pinout-drawing.jpg)

### Pro tip - gpio readall

The best thing about the Raspberry Pi is the direct control you have over its
GPIO system. Ever wonder what pins are labeled what? I picked up this trick from
a blog somewhere online. Type `$ gpio readall` from the command line. This will 
you a very straightforward, clear table of the pin layout your Raspbery Pi is 
using. Here's an example from the Pi 2b that I am using for this project:

![Pi 2b GPIO command line pinout](https://github.com/JoshMarsden/python-projects/blob/master/pi-clock/photos/gpio-readall-screenshot.png)

You'll notice that I have requested the pinout from the Pi as my program is 
running. This is a great way to debug your hardward projects on the fly. Not only
can you list this, but `gpio -h` and `gpio <command> -h` can give you more tools
to work with to affect the GPIO pins and observe the results. Science!


## Running Headless

Having the Pi Clock is great, but how does one keep it running and then leave the
terminal? The simplest version is to run the python process in the background, 
then detach the process from your current SSH session.

Run the program with python:

```bash
$ python pi-clock.py
```

Pause the current process (the running python program) with ctrl-z (^z) and 
background it with the `bg` command:

```bash
^Z
[1]+	Stopped			python pi-clock.py
$ bg
[1]+ python pi-clock.py &
$
```

This gives you the command prompt back, but if you log off from the SSH session, 
the program will stop running. To fix that, you need to `disown` the python 
process from the SSH session.

```bash
$ disown
```

You should be good to go now. You can log off and let the Pi run in peace.


## Code Commentary

> **Note:** While the code for this project is in Python 2.7, it will still work 
> in Python 3.X.

**show_num function**  
This function takes an integer argument `digit` for selecting one of the four 7-
segment displays to control. Following is a string argument `num` for selecting
a code string from a dictionary called `numcode`. The third argument `dp` is used
to turn the dot point LED on (True) or off (False).

```python
def show_num(digit, num, dp=False):
```

**Lines 39-49**
Here, I set some variables for use later on. Segments is a dictionary so that I
can do cool things like using the characters of each code string from the numcode
dictionary to resolved to the correct pin number which will end up sending a
signal to the correct LED segment.

```python
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
```

**Lines 51-64**
This is where the chosen numcode string comes into play. The if-else block turns 
a segment on only if it is in the code string. The next line is what controls 
whether the dot point LED is turned on or not.

The last three lines turn the selected digit on (0 because of the anode thing), 
wait a millisecond, and quickly deselect the digit.

```python
    for seg in segments:

        if seg in numcode[num]:
            GPIO.output(segments[seg], 1)
        else:
            GPIO.output(segments[seg], 0)

        GPIO.output(segments['dp'], dp)

    GPIO.output(dselect[digit], 0)
    time.sleep(0.001)
    GPIO.output(dselect[digit], 1)
```


**display_time function**  
This function _"prints"_ the hour and minute values on the 7-segment display 
module. The hour is expected to be in 24-hour time format, but does not break the 
logic if it is not. The second is simply used to _"animate"_ the dot point between
the hour and minute digits to give some motion to the clock. The mode is there if 
one wishes to put a button in the assembly later to control output format.

```python
def display_time(hh, mm, ss, mode=12):
```

**Line 72**
This is a one-liner to set the very last dot point to mark PM for evening times. A
ternary expression is used here to turn the PM marker off if in the 24-hour 
format. I prefer to use mathematical expressions of what is desired instead of 
relying on if-else logic to control my code. I feel that it leads to very simple
solutions.

```python
    pm = hh // 12 if mode == 12 else 0
```

**Lines 75-77**
Starting with a conditional mode option, this block is another simple mathematical
solution to a complex problem. I wanted a quick way to convert a 0-23 hour scale
to a 1-12 scale. This can either be accomplished via various if-else blocks in 
succession or using some clever tricks like integer division (//) and modulus (%).
Broken down, hh MOD 12 converts 24-hour numbers to a 12-hour scale. Subtracting 12
from the newly-scaled hour value and performing integer division by 12 ensures 
that 12 will only be added if the hour value is exactly equal to 0.

```python
    if mode == 12:
        hh %= 12
        hh = ((12 - hh) // 12) * 12 + hh
```

**Lines 79-85**
After all the 12-hour conversion stuff was finished, it was time to pad any single
digit values with zeroes (in the case of the hour value, with spaces). I decided
to leave the final values as strings because I could easily iterate through each
digit without too much fuss. It was also easy to just use a dictionary for storing
the numcode strings.

The final step was to call the `show_num` function four times, one for each digit
on the clock display. The seconds value MOD 2 is used to flash on and off every 
other second (another fun math trick). Now you see why I put that dp argument in.

```python
    hh = "%2d" % (hh)
    mm = "%02d" % (mm)

    show_num(0, hh[0])
    show_num(1, hh[1], ss % 2)
    show_num(2, mm[0])
    show_num(3, mm[1], pm)
```


**The \_\_main\_\_ show**  
After abstracting the heavy work out to the above two functions, all that was left
was to ask nicely for the current time (which is accurate as can be), extract the
hours, minutes, and seconds values from the time tuple, and call the 
`display_time` function. I put the `time.sleep(0.01)` just to test how slow the 
LEDs could flash on and off without the eye detecting them. I have found from 
other animation programming projects that .01 seconds is the perfect amount.

At the very end, I use the `finally` block to reset the GPIO pin modes and hand
control of the pins cleanly over the OS after the program terminates.

> **Note:** A better version can be created that does not keep polling the OS for 
> the current time 100 times a second.

```python
if __name__ == "__main__":
    try:
        while True:
            h, m, s = time.localtime()[3:6]
            display_time(h, m, s)
            time.sleep(0.01)
    finally:
        print("\ncleaning up.")
        GPIO.cleanup()
```
