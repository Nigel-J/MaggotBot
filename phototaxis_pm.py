#!/usr/bin/python

import time
import Robot
import numpy as np
from Adafruit_TSL2651 import *

LEFT_TRIM=0
RIGHT_TRIM=0

robot=Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

def calcprob(lastlux, offset):
	thislux = LightSensor.calculateLux()
	delta=(thislux-lastlux)
	p=1/(1+np.exp(-1*(-1*(float(delta)/5)-offset)))
	return thislux, p

def newrun(rang, lastlux):
	#begin with short run
	robot.forward(100, np.random.uniform(rang[0],rang[1]))
	#judge if life is improving
	thislux, pt = calcprob(lastlux, 0.5)
	print("P-turn is")
	r = np.random.rand() 
	if r>pt:
		#life is good, try small turns
		print("Small turns")
		t = np.random.rand()
		if t>0.5:
    			#sweep left
    			headsweep(robot.left, (0.2,0.3), thislux)
    		else:
    			#sweep right
			headsweep(robot.left, (0.2,0.3), thislux)
	else:
		#life is bad, do big sweeps
		print("Big turns")
		t = np.random.rand()
		if t>0.5:
    			#sweep left
    			headsweep(robot.left, (0.3,0.5), thislux)
    		else:
    			#sweep right
			headsweep(robot.left, (0.3,0.5), thislux)

def headsweep(dir, rang, lastlux):
	#initial sweep
	dir(150, np.random.uniform(rang[0],rang[1]))
	#take reading
	thislux, pa = calcprob(lastlux, 0.85)
	w = np.random.rand()
	if w<pa:
		#Accepted head sweep
		print("Accepted;")
		newrun([0.5,1.0], thislux)
	else: 
		print("Rejected;")
		if dir == robot.left:
			headsweep(robot.right, rang, lastlux)
		else:
			headsweep(robot.left, rang, lastlux)
			
try:
	while True:
		newrun([0.5,1.0], LightSensor.calculateLux())
except KeyboardInterrupt:
	print('seeya')
