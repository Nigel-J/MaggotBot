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

while True:
        
        #begin with short run
        robot.backward(150,0.2)
        
        #judge if life is improving
        thistime = LightSensor.calculateLux()
        delta=(thistime-lasttime)
        pt=1/(1+math.exp(-1*(-1*(float(delta)/5)-0.5)))
        print "P-turn is" pt
        r = random.random()   
        
        if r>pt:
                #life is good, keep going
                print "Continue run" + '\n'
                robot.backward(150,0.2)
                
        else:
                #life is not improving, time for head sweeps
                print "Turn" + '\n'
                
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
                
        lasttime = thistime;

