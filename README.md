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

1. Make a copy of the document

2. Rename it with your name

3. Create all parts needed and assemble

4. You should be able to do this in 1 hour

### Evidence

![image](https://github.com/hotting45/engr3/assets/143732418/3bd0524f-8284-4b27-b977-37d00626baf0)
![image](https://github.com/hotting45/engr3/assets/143732418/cb09068e-812b-4fdc-8a71-39f1a88ee934)
Credit to Henry Ottinger because my pictures wouldn't work

### Part Link 

(https://cvilleschools.onshape.com/documents/4e36acb62dc45aa02786041a/w/e64ad7152e355b89b94c1132/e/fa7f75331ca38b3800fb7080)

### Reflection

I learned how to use multiple images to create one complex piece using multiple different parts. Some things that others should know while making this assignment are to create variables, make sure to set extrudes to "add" or "new" depending on if you need to make a new part or add on to an old one, and make sure to select the part you're adding on to if you are adding on to a new part. Lastly, make sure constraints are set to where they're supposed to be and not equal to a specific number.
&nbsp;

## Onshape_Assignment_Single_Part

### Assignment Description

1. Open the Document and make a copy

2. Follow instructions for each question and adjust each measurement

3. Record measurements and mass while answering questions

4. Enter mass in questions and SUBMIT!
   
### Evidence

![image](https://github.com/wwright71/engr3/assets/143732572/f4cef4c9-f652-4adb-987d-b30cf53b57b8)
![image](https://github.com/wwright71/engr3/assets/143732572/e5c1b08d-e732-4530-964f-28978595d08f)
![image](https://github.com/wwright71/engr3/assets/143732572/73a19c6c-a265-4515-ab82-617e1d074d7c)

### Part Link 

(https://cvilleschools.onshape.com/documents/7d26552196fee86ea06089da/w/c958bbc6fe884ff7775a4628/e/7e7e4d82e081317643a46f52)

### Reflection
I completed this assignment pretty quickly and I would say I didn't specifically learn anything but it was a good test to see how fast I could complete an assignment which was quite useful for me. Something that could help other students is when you have a shape that is symmetrical you can make one half of the shape and then mirror it over later for an easier time. Something I learned how to do during this assignment was to increase my skill in creating a piece from a blueprint in a limited time quickly.

&nbsp;


## Onshape_Assignment_Alignment_Plate

### Assignment Description

1. Copy the template from onshape
   
2. Subscribe to the template
   
3. Open a new doc and the template in that doc
   
4. Start working on the assignment 
   
### Evidence

![image](https://github.com/wwright71/engr3/assets/143732572/579e1726-369b-4cd4-b779-faf4e185ff51)
![image](https://github.com/wwright71/engr3/assets/143732572/9c6ccd17-6287-42d4-9a57-9dd4b9825e75)

### Part Link 

(https://cvilleschools.onshape.com/documents/10b9a3a559efe6ee7fe9565c/w/8ea7c6795f75a829aa8b4936/e/718fa5047b23684c752667af)

### Reflection
This assignment was overall very easy and was completed very fast. I had no issues with this part since it was very small and not complex. I recommend that others remember to set the material and make sure to check your chamfers. 

&nbsp;

## Onshape_Assignment_Multipart

### Assignment Description

1. Open and copy the document

2. Follow instructions for each question asked

3. After finishing the part, submit the mass to canvas

4. Submit the quiz
   
### Evidence

![image](https://github.com/wwright71/engr3/assets/143732572/5209b029-48f7-4da9-b245-7cf33236b19f)
![image](https://github.com/wwright71/engr3/assets/143732572/a3394e53-ed1f-4924-9b6c-a0961c08b57f)
![image](https://github.com/wwright71/engr3/assets/143732572/0d7c6106-de85-433f-b39d-6f17604eb0d9)
![image](https://github.com/wwright71/engr3/assets/143732572/ccb09917-8bd7-46e2-9d41-dcc204184d4b)

### Part Link 

(https://cvilleschools.onshape.com/documents/085529258c83be1f3c0ec0ff/w/6298bff7abde40b9328b0d3a/e/734f698ec62c0bf367cb75b3)

### Reflection
During this assignment, I learned that the bolt at the top was not defined by anything except for the fillet and that I need to pay more attention to what or what not is defined. Other students would find the fillet tool very helpful especially for making those curved edges on this assignment. Overall, this assignment was pretty simple to construct and I was able to complete it with minimal difficulty. 
&nbsp;

## Rotary Encoder

### Description & Code

1. Get materials from the labs in the back

2. Create the wiring and test it with the serial monitor

3. Set up LCD screen and check if its working

4. Translate all code over to print on the LCD

5. Set up led on board to match the menu on the LCD screen

```python
import rotaryio
import board
import neopixel
import digitalio
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

enc = rotaryio.IncrementalEncoder(board.D4, board.D3, divisor = 2)

lcd = LCD(I2CPCF8574Interface(board.I2C(), 0x27), num_rows = 2, num_cols = 16)

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
led[0] = (255, 0, 0)

button = digitalio.DigitalInOut(board.D2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
button_state = None  

menu_index = 0

 
while True:
    menu_index = enc.position
    menu = ["stop", "caution", "go"]
    last_index = None
    menu[0] = "stop"
    menu[1] = "caution"
    menu[2] = "go"  
    menu_index_lcd = menu_index % 3
    lcd.set_cursor_pos(0,0)
    lcd.print("Push for: ")
    lcd.set_cursor_pos(1,0)
    lcd.print ("           ")
    lcd.set_cursor_pos(1,0)
    lcd.print(menu[menu_index_lcd])
    print(menu_index_lcd)
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button is pressed")
        button_state = None
    if menu_index_lcd == 0:
        led[0] = (255, 0, 0)
    if menu_index_lcd == 2:
        led[0] = (0, 255, 0)
    if menu_index_lcd == 1:
        led[0] = (255, 255, 0)
```

### Evidence
https://im5.ezgif.com/tmp/ezgif-5-f016b3766d.gif


### Wiring
![image](https://github.com/wwright71/engr3/assets/143732572/5004adef-d614-4104-99fa-f9543e0774cc)



### Reflection
Creating a menu was a little difficult because it had been a while since I had made one, but using my vast knowledge combined with the power of Google, I would win. I recommend when doing something you haven't done in a while, use the beautiful creation of Google just as I did, it is a lot more useful than you think. Also it is Mr. Miller approved.
## IR Sensor

### Description & Code

1. Download neopixel libraries if not already downloaded

2. Wire up the IR sensor to metro m4 using the neopixel, ground, any D pin, and 5v

3. Code in the IR sensor to print into the monitor, then check if it runs

4. Set up the IR sensor so it changes the color of the LED when active vs not active

```
import board
import neopixel
import digitalio

ir_sensor = digitalio.DigitalInOut(board.D2)
ir_sensor.direction = digitalio.Direction.INPUT
ir_sensor.pull = digitalio.Pull.UP

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
led[0] = (255,0,0)

while True:
    if ir_sensor.value == 1:
        print("Sensor is LOW")
        led[0] = (255, 0, 0)

    if ir_sensor.value == 0:
        print("Sensor is HIGH")
        led[0] = (0, 255, 0)
```

### Evidence
![WIN_20240212_11_30_24_Pro-ezgif com-optimize (1)](https://github.com/wwright71/engr3/assets/143732572/df415300-c7f2-46d8-b575-d9bcb2089db0)



### Wiring
![image](https://github.com/wwright71/engr3/assets/143732572/a6b43bf9-d0d7-45d8-8053-8649ce656381)

&nbsp;

### Reflection
MAKE SURE TO CHECK YOUR WIRING BECAUSE I DIDN'T KNOW THE PINS STARTED AT 0 AND NOT 1 SO I WAS VERY LOST AS TO WHY IT WAS NOT WORKING UNTIL I REALIZED IT WAS OFF BY ONE PIN BECAUSE I THOUGHT IT WAS PLUGGED INTO 1 AND NOT 2.

## Onshape_Assignment_Robot_Claw

### Assignment Description

1. Create a design for a robot claw on Onshape using the following requirements:
           Must close using one actuator
           Must be able to fully close
           Must be able to be printed and laser cut
           Must be fully fastened through Onshape
   
### Evidence

![image](https://github.com/wwright71/engr3/assets/143732572/6483b163-b668-4d97-aa72-b92f1712e45b)
![image](https://github.com/wwright71/engr3/assets/143732572/b2cb6966-b1da-44f1-b2b7-b420c55dedb8)
![image](https://github.com/wwright71/engr3/assets/143732572/986cb5b6-5b56-4677-b2c1-0b91528a3420)

### Part Link 

https://cvilleschools.onshape.com/documents/a407a953e0de07ab89e63153/w/99b41ad0450fa2a2bc45e323/e/1d4bab6124a929e8dda980fa

### Reflection
Make sure to check all of your parts are aligned correctly with each other, I, unfortunately, did not do this and was stuck trying to fix all of my Revolute mates that were breaking whenever I tried to connect multiple parts. In conclusion, check all of the lengths and widths of your parts to make sure they match before trying to Revolute mate them together. 

&nbsp;
