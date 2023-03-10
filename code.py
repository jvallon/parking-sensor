# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Simple demo of the VL53L1X distance sensor.
# Will print the sensed range/distance every second.

import time
import board
import digitalio
import adafruit_vl53l1x
import neopixel
import adafruit_dotstar
import microcontroller

RED = (255, 0, 0)
YELLOW = (233, 100, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

i2c = board.I2C()

# setup onboard neopixel
if hasattr(board, "NEOPIXEL"):
    NEOPIXEL = board.NEOPIXEL
else:
    NEOPIXEL = microcontroller.pin.GPIO16

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1, auto_write=False)

# setup onboard LED
if hasattr(board, "LED"):
    led = digitalio.DigitalInOut(board.LED)
else:
    led = digitalio.DigitalInOut(board.A0)

led.direction = digitalio.Direction.OUTPUT

# setup IO
btn = digitalio.DigitalInOut(board.A0)
btn.switch_to_input(pull=digitalio.Pull.UP)

# setup led strip
ledstrip = adafruit_dotstar.DotStar(
    clock=board.SCK, data=board.MOSI, n=10, brightness=0.1
)

# setup range finder
vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# OPTIONAL: can set non-default values
vl53.distance_mode = 2
vl53.timing_budget = 200

# return color for a predefined
def color_by_range(number: range):
    if range > 100:
        pixels[0] = GREEN
    elif range > 50:
        pixels[0] = YELLOW
    else:
        pixels[0] = RED
    pixels.show()


print("VL53L1X Simple Test.")
print("--------------------")
model_id, module_type, mask_rev = vl53.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Mask Revision: 0x{:0X}".format(mask_rev))
print("Distance Mode: ", end="")
if vl53.distance_mode == 1:
    print("SHORT")
elif vl53.distance_mode == 2:
    print("LONG")
else:
    print("UNKNOWN")
print("Timing Budget: {}".format(vl53.timing_budget))
print("--------------------")

vl53.start_ranging()

while True:

    if vl53.data_ready:
        range = vl53.distance
        print("Distance: {} cm".format(range))
        vl53.clear_interrupt()
        if range is not None:
            color_by_range(vl53.distance)
        if not btn.value:
            led.value = True
            print("Btn true")
        else:
            led.value = False

        time.sleep(0.1)

# define range min/max/ideal
# define colors by range: 100-50% green, 50-ideal yellow, ideal%-0 red.
# while in range
#  if > ideal + X
#
#
