#!/usr/bin/python

import time
import Robot
import random
import math
import initTSL2561

LEFT_TRIM=0
RIGHT_TRIM=0

robot=Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

thistime = 0
lasttime = 0

#begin with short run

while True:
        robot.backward(150,0.2)
        
        #headsweep(s)
        t = random.random()
        if t>0.5:
                #sweep left
                robot.left(172, 0.25)
                #take reading
                thistime = LightSensor.calculateLux()
                #probability of accepting
                delta = (thistime-lasttime)
                print delta "Lux;" + '\n'
                pa = 1/(1+math.exp(-1*(-1*(float(delta)/5)-0.85)))
                # Print probablility of accepting? print pa  + '\n'
                w = random.random()
                if w<pa:
                        #Accepted left head sweep
                        robot.backward(150,0.2)
                        print "Accepted;" + '\n'
                        
                else: 
                        print "Rejected;" + '\n'
                        robot.right(172, 0.25)
                         
        else:
                #sweep right
                robot.right(172, 0.25)
                #take reading
                thistime = LightSensor.calculateLux()
                #probability of accepting
                delta = (thistime-lasttime)
                print delta "Lux;" + '\n'
                pa = 1/(1+math.exp(-1*(-1*(float(delta)/5)-0.85)))
                # Print probablility of accepting? print pa  + '\n'
                w = random.random()
                if w<pa:
                        #Accepted right head sweep
                        robot.backward(150,0.2)
                        print "Accepted;" + '\n'
                else: 
                        print "Rejected;" + '\n'
                        robot.left(172, 0.25)
                
        ###
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

