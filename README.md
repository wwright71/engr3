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

1. Use the HC-SR04 to measure the distance to an object and print that out to your serial monitor or LCD in cm.
   
2. Next, you will get the neopixel to turn red when your object is less than 5cm, and green when its 35cm.  Ignore the blue and 20cm for now, let's just keep it simple.

3. For your final version of this code, you'll smoothly shift the color of the onboard neopixel, corresponding to the distance, according to the graphic below.

     1. (Neopixel should stay red when below 5cm and green when above 35cm)


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
```

### Evidence
![ezgif com-video-to-gif (2)](https://github.com/wwright71/engr3/blob/main/ezgif.com-video-to-gif%20(1).gif?raw=true)
### Wiring
![image](https://github.com/wwright71/engr3/assets/143732572/c0f8364a-3fe6-4d4d-8f27-97105b53e2a5)

### Reflection
During this assignment I had trouble using the map() function so here is a helpful guide for using it.
https://docs.circuitpython.org/projects/simpleio/en/latest/api.html#simpleio.map_range
Another issue I ran into was indentation. This code uses a lot of "if" commands and loops, so it is very important that you indent everything correctly otherwise the code will not work. I had 4 separate times where I had the wrong line either indented too much or not indented enough and it drove me insane, SO PLEASE MAKE SURE YOU INDENT!!!!!!






## Motor Control

### Description & Code

1. Wire up a 6v battery pack to this circuit with a motor.

2. Write Python code to make the motor speed up and slow down, based on input from a potentiometer.
 

```python
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
    time.sleep(0.25)                   # Wait a bit before checking all again
    motor.duty_cycle = potentiometer.value

```

### Evidence
![ezgif com-video-to-gif (2)](https://github.com/wwright71/engr3/assets/143732572/cf7467b3-c4ce-4a99-bf5c-53ded6fd28f8)

### Wiring
![image](https://github.com/wwright71/engr3/assets/143732572/9b7db0c1-933b-46a8-980f-6a787dee25f7)

### Reflection

Make sure to check your wiring with one of the teachers when wiring with a 6v battery pack because if you wire it incorrectly it will short circuit and blow it out. My favorite part of this assignment was when I first set up the motor without being able to control the speed it started going really fast and it scared half the class. My least favorite part of this assignment was getting the potentiometer to link up with the speed of the motor and being able to adjust it to change the speed/direction.

## Onshape_Assignment_The_Hanger

### Assignment Description

Using the images provided create the part in Onshape, then set the correct measurements and material 

### Evidence

![image](https://github.com/wwright71/engr3/assets/143732572/eea89c57-03fc-4c96-bff1-afa0eb567833)
![image](https://github.com/wwright71/engr3/assets/143732572/9edb5fa3-f1d8-4431-8ba5-efcf42dc123e)
![image](https://github.com/wwright71/engr3/assets/143732572/81221293-ce5c-4d69-9f92-20a14c93c8b3)

### Part Link 

https://cvilleschools.onshape.com/documents/547e5da0936915c8f3a4169a/w/a8f0df700954ea780c5fcdcc/e/66277b2755306290ad869600

### Reflection
Overall, this assignment was very simple, it only had one image and it was completely symmetrical. This allowed me to make one-half of the assignment and then mirror all of it over, actively cutting my work time in half. My favorite past of this assignment was mirroring over everything at the end and my least favorite was creating the curved line in the stretch since it took multiple different steps to do.
&nbsp;


## Onshape_Assignment_Swing_Arm

### Assignment Description

1. Make a copy of the assignment and rename it with your name

2. The first 2 slides are instructions and the last 2 are for you to work on

3. Create a new part and rename it to "swing arm

4. Design the part using the drawings and define variables that they can change depending on the assignment

5. Update model based off of the question asked and submit the mass

### Evidence

![image](https://github.com/wwright71/engr3/assets/143732572/5fc89ba5-5c37-4532-af4a-33b297ff9165)
![image](https://github.com/wwright71/engr3/assets/143732572/61d93ad7-c0d7-45a6-953d-2100b1cf6372)
![image](https://github.com/wwright71/engr3/assets/143732572/43861d25-1d11-490e-9fce-89114fe68477)
![image](https://github.com/wwright71/engr3/assets/143732572/9431501c-67e1-4158-83d6-0356b8a10624)

### Part Link 

https://cvilleschools.onshape.com/documents/ac4b93d873400ee95a17c509/w/fe7c10129bcfea8a546af52d/e/7f25961cc17f1d8061031a8f

### Reflection
Overall, before I started this assignment I was very scared because it looked quite complex, but once I got started and set up my variables the assignment wasn't very difficult. Things I do want to look back on were to make sure and check each picture and all the measurements twice because I did mix up a measurement where I was supposed to put a variable. Another thing that you need to do is make sure your material is set to the correct thing and it correlates to the assignment.
&nbsp;

## Onshape_Multipart_Design

### Assignment Description

1. Make a copy of this document.
   
2. Rename and replace the copy with your name.
   
3. Create all of the parts needed for the assembly.  The cylinder is given as a starting point.
 
4. Answer the 4 questions below.  There is a question about the initial assembly and then one for each of the three revisions to the product.

You should be able to complete this assignment in 1 hour.

### Evidence

![image](https://github.com/hotting45/engr3/assets/143732418/3bd0524f-8284-4b27-b977-37d00626baf0)
![image](https://github.com/hotting45/engr3/assets/143732418/cb09068e-812b-4fdc-8a71-39f1a88ee934)
Credit to Henry Ottinger because my pictures wouldn't work

### Part Link 

(https://cvilleschools.onshape.com/documents/4e36acb62dc45aa02786041a/w/e64ad7152e355b89b94c1132/e/fa7f75331ca38b3800fb7080)

### Reflection

I learned how to use multiple images to create one complex piece using multiple different parts. Some things that others should know while making this assignment are to create variables, make sure to set extrudes to "add" or "new" depending on if you need to make a new part or add on to an old one, and make sure to select the part you're adding on to if you are adding on to a new part. Lastly, make sure constriants are set to where they're supposed to be and not equal to a specific number.
&nbsp;

