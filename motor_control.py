# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from analogio import AnalogIn
import pwmio 
from digitalio import DigitalInOut

potentiometer = AnalogIn(board.A1)  # potentiometer connected to A1, power & ground
motor = pwmio.PWMOut(board.D3)

while True:

    print(potentiometer.value)      # Display value
    time.sleep(0.25)                   # Wait a bit before checking all againng all again
    motor.duty_cycle = potentiometer.value
