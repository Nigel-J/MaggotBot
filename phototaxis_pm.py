#!/usr/bin/python

import time
import Robot
import numpy as np
import initTSL2561

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
	robot.backward(100, numpy.random.uniform(rang[0],rang[1])
	#judge if life is improving
	thislux, pt = calcprob(lastlux, 0.5)
	print "P-turn is" pt
	r = np.random.rand() 
	if r>pt:
		#life is good, try small turns
		print "Small turns" + '\n'
		t = np.random.rand()
		if t>0.5:
    		#sweep left
    		headsweep(robot.left, (0.1,0.25), thislux)
    	else:
    		#sweep right
			headsweep(robot.left, (0.1,0.25), thislux)
	else:
		#life is bad, do big sweeps
		print "Big turns" + '\n'
		t = np.random.rand()
		if t>0.5:
    		#sweep left
    		headsweep(robot.left, (0.25,0.4), thislux)
    	else:
    		#sweep right
			headsweep(robot.left, (0.25,0.4), thislux)

def headsweep(dir, rang, lastlux):
	#initial sweep
	dir(150, np.random.uniform(rang[0],rang[1]))
	#take reading
    thislux, pa = calcprob(lastlux, 0.85)
	w = np.random.rand()
	if w<pa:
		#Accepted head sweep
		print "Accepted;" + '\n'
		newrun(rang, thislux)
	else: 
		print "Rejected;" + '\n'
		if dir == robot.left:
			headsweep(robot.right, rang, lastlux)
		else:
			headsweep(robot.left, rang, lastlux)
			
try:
	while True:
		newrun([0,1.0], LightSensor.calculateLux())
except KeyboardInterrupt:
	print('seeya')