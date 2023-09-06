import time
import board
from digitalio import DigitalInOut, Direction, Pull
import pwmio
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm)

btn1 = DigitalInOut(board.D2)
btn1.direction = Direction.INPUT
btn1.pull = Pull.DOWN

btn2 = DigitalInOut(board.D3)
btn2.direction = Direction.INPUT
btn2.pull = Pull.DOWN

while True:
    if  btn1.value:
        print("BTN1 is down")
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time
            my_servo.angle = angle

    if  btn2.value:
        print("BTN2 is down")
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time
            my_servo.angle = angle
    
    time.sleep(0.1) # sleep for debounce
