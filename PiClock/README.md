The Pi Clock
---

## Inspiration

It has occurred to me that a clock in my room is a must-have. So much time can be 
wasted from checking either the nearest phone or computer screen as the 
distractions are inevitable. I know, it's a small thing, but to me it makes a 
huge difference. Also, it's nice to have a simple project like this by which I 
can hone my electronics and programming skills.

## Materials Necessary

* Raspberry Pi 2 or 3
* 4-digit 7-segment display module
* 12 jumper wires (male to female)
* 8 resistors (220 or 100 ohms)
* Breadboard
* Box of some kind to house the clock

## Wiring

> Picture of Fritzing diagram will go here

> Table of pin connections (maybe RasPi pinout table)

## Code Commentary

> Note that while the code for this project is in Python 2.7, it will still work 
> in Python 3.X.

**show__num function**

**Lines 22-40**
Here, I set some variables for use later on. Segments is a dictionary so that I
can do cool things like using the characters of each code string from the numcode
dictionary to resolved to the correct pin number which will end up sending a
signal to the correct LED segment.

```python
    segments = {'a':8, 'b':10, 'c':23, 'd':27, 'e':17, 'f':25, 'g':24, 'dp':22}

    numcode = { ' ': '',
                '0': 'abcdef',
                '1': 'bc',
                '2': 'abdeg',
                '3': 'abcdg',
                '4': 'bcfg',
                '5': 'acdfg',
                '6': 'acdefg',
                '7': 'abc',
                '8': 'abcdefg',
                '9': 'abcdfg' }

    deselect = (15, 3, 2, 14)
```
