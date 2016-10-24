#!/usr/bin/python

import time
import Robot
import random
import math
import initTSL2561

LEFT_TRIM=0
RIGHT_TRIM=5

robot=Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

thistime = 0
lasttime = 0

while True:
        thistime=LightSensor.calculateLux()
        print thistime - lasttime, "Lux"

        robot.backward(150,0.2)

        delta=(thistime-lasttime)
        pt=1/(1+math.exp(-1*(-1*(float(delta)/5)-0.5)))
        print pt
        r = random.random()
# cap        if pt>0.9:
#                pt=0.9
# cap        if pt<0.1:
#                pt=0.1        
        if r<pt:
                robot.left(172, random.random())
                print "Turn;"+'\n'
        else:
                robot.backward(150, 0.3)
                print "Run;"+'\n'

        lasttime = thistime;

