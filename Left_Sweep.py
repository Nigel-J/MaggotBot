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
robot.left(70,0.7)
#take reading
thistime = LightSensor.calculateLux()
#probability of accepting
delta = (thistime-lasttime)
print "Delta is", delta, "Lux"
pa = 1/(1+math.exp(-1*(float(delta)/5)-0.85))
print("P-%s is %s " % ("accept", pa))
w = random.random()

if w<pa:
        #Accepted left head sweep
        robot.forward(150,0.2)
        print "Accepted;" + '\n'

else:
        print "Rejected; sweep right instead" + '\n'
        robot.right(70, 0.7)
        lasttime = thistime
        execfile("Right_Sweep.py")

  
