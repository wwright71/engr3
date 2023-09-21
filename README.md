# CircuitPython
This repository will actually serve as an aid to help you get started with your own template.  You should copy the raw form of this readme into your own, and use this template to write your own.  If you want to draw inspiration from other classmates, feel free to check [this directory of all students!](https://github.com/chssigma/Class_Accounts).
## Table of Contents
* [Table of Contents](#TableOfContents)
* [Hello_CircuitPython](#Hello_CircuitPython)
* [CircuitPython_Servo](#CircuitPython_Servo)
* [CircuitPython_LCD](#CircuitPython_LCD)
* [NextAssignmentGoesHere](#NextAssignment)
---

## Hello_CircuitPython

### Description & Code
Description goes here

Here's how you make code look like code:

```python
Code goes here

```


### Evidence


![spinningMetro_Optimized](https://user-images.githubusercontent.com/54641488/192549584-18285130-2e3b-4631-8005-0792c2942f73.gif)


And here is how you should give image credit to someone if you use their work:

Image credit goes to [Rick A](https://www.youtube.com/watch?v=dQw4w9WgXcQ&scrlybrkr=8931d0bc)



### Wiring
Make an account with your Google ID at [tinkercad.com](https://www.tinkercad.com/learn/circuits), and use "TinkerCad Circuits to make a wiring diagram."  It's really easy!  
Then post an image here.   [here's a quick tutorial for all markdown code, like making links](https://guides.github.com/features/mastering-markdown/)

### Reflection
What went wrong / was challenging, how'd you figure it out, and what did you learn from that experience?  Your ultimate goal for the reflection is to pass on the knowledge that will make this assignment better or easier for the next person.




## How To Fix the LCD power issue with Metro M4 boards.

### Description & Code

* **The symptoms:**  LCD acting weird OR trouble with usb connection / serial monitor / uploading / etc.
* **The problem :** The LCDs occasionally draw too much power when we turn on the boards, and that makes parts of its serial communications crash.
* **The Solution:** Add this code, and wire a switch up, like the wiring diagram below:



```python
import board
import time
import digitalio
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

# turn on lcd power switch pin
lcdPower = digitalio.DigitalInOut(board.D8)
lcdPower.direction = digitalio.Direction.INPUT
lcdPower.pull = digitalio.Pull.DOWN

# Keep the I2C protocol from running until the LCD has been turned on
# You need to flip the switch on the breadboard to do this.
while lcdPower.value is False:
    print("still sleeping")
    time.sleep(0.1)

# Time to start up the LCD!
time.sleep(1)
print(lcdPower.value)
print("running")

i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)


# Loop forever.
while True:

```
### Wiring

![WiringSolution](images/I2C_M4_Solution.png)






## Servo Button Control

### Description & Code

1. Get a 180° micro servo to slowly sweep back and forth between 0 and 180°.  

2. Spicy part: Now control the servo with 2 buttons. 

     _The servo only moves if you are pushing a button._

```python
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

  +-
```

### Evidence
![com-vido-to-gif (1)](https://github.com/wwright71/engr3/blob/main/media/ezgif.com-video-to-gif.gif?raw=true)




### Wiring
![servo wiring ](https://github.com/wwright71/engr3/blob/main/media/Servo_Button_Wiring.png?raw=true)](https://github.com/wwright71/engr3/blob/main/media/Servo_Button_Wiring.png?raw=true)




### Reflection
I had a lot of trouble making my code and wiring, Searching online really helped me when I was stuck, especially with finding code.

(https://learn.adafruit.com/multi-tasking-with-circuitpython/buttons)

^ Link to a site I found helpful for coding ^

I also used https://ezgif.com/video-to-gif/ezgif-4-736f9f4571.mp4 to create gifs for this assignment which was very helpful for making my engineering notebook.



INDENTATION IS VERY IMPORTANT!!!




## Distance Sensor

### Description & Code
```python
import time
import board
import adafruit_hcsr04  
from rainbowio import colorwheel
import neopixel 
import simpleio

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

pixel_pin = board.NEOPIXEL
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

while True:
    try:

        print((sonar.distance,))
        if (sonar.distance <= 5.0):
            blue = 0
            green = 0
            red = 255

        if (sonar.distance >= 5.0) and (sonar.distance < 20.0):
            green = 0
            blue = simpleio.map_range(sonar.distance,5.0,20.0,0.0,255.0)
            red = simpleio.map_range(sonar.distance,5.0,20.0,255.0,0.0)

        if (sonar.distance >= 20) and (sonar.distance <35):
            red = 0
            green = simpleio.map_range(sonar.distance,20.0,35.0,0.0,255.0)
            blue = simpleio.map_range(sonar.distance,20.0,35.0,255.0,0.0)
        if (sonar.distance >=35):
            red = 0
            blue = 0
            green = 255
        print("red =",red," green = ",green," blue = ",blue)    
        pixels[0] = (red,green,blue)
        pixels.show()
    
    except RuntimeError:
        print("Retrying!")

    time.sleep(0.1)


### Evidence

### Wiring
![image](https://github.com/wwright71/engr3/assets/143732572/c0f8364a-3fe6-4d4d-8f27-97105b53e2a5)

### Reflection
During this assignment I had trouble using the map() function so here is a helpful guide for using it.
https://docs.circuitpython.org/projects/simpleio/en/latest/api.html#simpleio.map_range
