import time

import Robot

LEFT_TRIM   = 0
RIGHT_TRIM  = 0

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

import random

import RPi.GPIO as GPIO, time, os

DEBUG = 1

GPIO.setmode(GPIO.BCM)
# everything initialized

def RCtime (RCpin): # take a reading of the light
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading

lasttime=0
#while True:                                     
#        #  print RCtime(18)    
#       thistime=RCtime(18)
#       print thistime-lasttime
#       lasttime=thistime

while True:
        timeToLight = RCtime(18)
        robot.backward(150, 0.5)
        if timeToLight-lasttime > 0: #if light intensity is now greater, move forward
                robot.backward(150, 0.5)
                lasttime = timeToLight # reassign lasttime to be timeToLight
        else:   robot.left(150,random.random()) # if light intensity is not greater, turn in random direction and restart

