import time
import board
from digitalio import DigitalInOut, Direction, Pull

btn1 = DigitalInOut(board.D2)
btn1.direction = Direction.INPUT
btn1.pull = Pull.DOWN

while True:
    if  btn1.value:
        print("BTN1 is down")
    else:
        print("BTN1 is up")
        pass

    time.sleep(0.1) # sleep for debounce