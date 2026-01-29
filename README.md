# MicroPython-display_7_segmentos

A simple MicroPython library for 7-segments Display.

## Features
- Easy to use.
- Compatible with ESP32 and Raspberry.

## Example of usage
```python
from display import Display
from time import sleep
my_display = Display(a=1, b=2, c=3, d=4, e=5, f=6, g=7, common_cathode=true)
for n in range(10):
  my_display.print_int(n)#displays the numbers from 0 to 9
  sleep(1)
my_display.print_str(string="Eduardo", seconds=1)#displays all characters in the string with one second between them
