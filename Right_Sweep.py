#!/usr/bin/python

import time
import Robot
import random
import math
from Adafruit_TSL2651 import *

LEFT_TRIM=0
RIGHT_TRIM=0

robot=Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

lasttime = LightSensor.calculateLux()

print "Right Sweep"
robot.right(70, 0.7)
#take reading
thistime = LightSensor.calculateLux()
#probability of accepting
delta = (thistime-lasttime)
print "Delta is", delta, "Lux;"
pa = 1/(1+math.exp(-1*(float(delta)/5)-0.85))
print("P-%s is %s " % ("accept", pa))
w = random.random()

if w<pa:
        #Accepted right head sweep
        #Flash light
        GPIO.output(5,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(5,GPIO.LOW)
        print "Accepted"
        print "Turncount =", turncount
        print '\n'
        robot.forward(150,0.2)

else:
        robot.left(70, 0.7)
        lasttime = thistime
        if turncount >= 10:
                print "Turncount =", turncount
                print "Too many sweeps; start new run"
                GPIO.output(26,GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(26,GPIO.LOW)
                robot.forward(150,0.2)

        else:
                print "Rejected; sweep left instead" + '\n'
                turncount+=1
                execfile("Left_Sweep.py") 
                
