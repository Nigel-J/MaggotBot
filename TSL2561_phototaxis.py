#!/usr/bin/python

import time
import Robot
import random
import math
from Adafruit_TSL2651 import *

LEFT_TRIM=0
RIGHT_TRIM=0

robot=Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

thistime = 0
lasttime = 0

while True:

        #begin with short run
        lasttime = LightSensor.calculateLux()
        robot.forward(150,0.2)
        
        #judge if life is improving
        thistime = LightSensor.calculateLux()
        delta=(thistime-lasttime)
        print "Delta is", delta, "Lux;"
        pt=1/(1+math.exp(-1*(-1*(float(delta)/5)-0.5)))
        print "P-turn is", pt
        r = random.random()

        if r>pt:
                #life is good, keep going
                print "Continue run" + '\n'
                robot.forward(150,0.2)

        else:
                #life is not improving, time for head sweeps
                print "Turn; Begin head sweeps" + '\n'

                lasttime = thistime
                t = random.random()
                if t>0.5:
                        #sweep left
                        print "Sweep left"
                        execfile("Left_Sweep.py")

                else:
                        #sweep right
                        print "Sweep right"
                        execfile("Right_Sweep.py")
                        
        lasttime = thistime
