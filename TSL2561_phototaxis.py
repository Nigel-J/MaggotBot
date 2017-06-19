#!/usr/bin/python

import time
import Robot
import Left_Sweep
import Right_Sweep
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
                lasttime = thistime
                
        else:
                #life is not improving, time for head sweeps
                print "Turn" + '\n'
                
                lasttime = thistime
                t = random.random()
                if t>0.5:
                        #sweep left
                        os.system("Left_Sweep.py")
                                
                else:
                        #sweep right
                        os.system("Right_Sweep.py")
                
        lasttime = thistime

