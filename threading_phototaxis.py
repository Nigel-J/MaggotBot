import Queue
import threading
import time
import Robot
import numpy as np
from Adafruit_TSL2651 import *
import RPi.GPIO as io

io.setmode(io.BCM)
io.setwarnings(False)
io.setup(5,io.OUT) #red right
io.setup(20, io.OUT) #yellow new run
io.setup(25, io.OUT) #green going
io.setup(27, io.OUT) #blue left

LEFT_TRIM = 0
RIGHT_TRIM = 10

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

phototaxis = False
directing = False

class listenerThread(threading.Thread):
        def __init__(self, threadID, name, q):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.q = q
        def run(self):
			try:
	    	    print("Starting " + self.name)
	    	    get_input(self.name, self.q)
	    	    print("Exiting " + self.name)
			except Exception as e:
				print("Listener Broke")
				print(e)
				io.output(5, io.LOW)
				io.output(20, io.LOW)
				io.output(25, io.LOW)
				io.output(27, io.LOW)
				robot.stop()
		
def get_input(threadName, q):
        global phototaxis
        global directing
        while True:
                data = input("->")
                queueLock.acquire()
                q.put(data)
                queueLock.release()
                #print("%s read in %s" % (threadName, data))
                if (data == "go"):
                        phototaxis = True
                        directing = False
                if (data == 'out'): 
                        phototaxis = False
                        directing = True
                if (data == 'quit'):
                        phototaxis = False
                        directing = False
                        break

class motionThread(threading.Thread):
        def __init__(self, threadID, name, q):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.q = q
        def run(self):
			try:
	            print("Starting " + self.name)
	            process_input(self.name, self.q)
	            print("Exiting " + self.name)
			except Exception as e:
				print("Motion broke")
                print(e)
				io.output(5, io.LOW)
                io.output(20, io.LOW)
                io.output(25, io.LOW)
                io.output(27, io.LOW)
                robot.stop()

def process_input(threadName, q):
        going = True
        move = 1
	while going:
		io.output(25, io.HIGH)
        # not doing anything, waiting for initial instruction
        while not phototaxis and not directing:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
                if data == 'go':
                    break
                elif data == 'out':
                    photo = False
                    break
                elif data == 'quit':
                    going = False
                    photo = False
					io.output(25, io.LOW)
                    break
            else:
                queueLock.release()
                time.sleep(1)
        # phototaxis loop
    	#thislux = LightSensor.calculateLux()
        #print(thislux)
        while phototaxis:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
                if data == 'out':
                    photo = False
                    break
                elif data == 'quit':
                    going = False
                    photo = False
                    io.output(25, io.LOW)
					break
            else:
                queueLock.release()
                #print("new run" + str(thislux))
                thislux = LightSensor.calculateLux()
                newrun(np.array([0.2,0.5]),thislux)
                #print(thislux)
        # directing loop
        while directing:
        	queueLock.acquire()
            if not workQueue.empty():
                dir = q.get()
                queueLock.release()
                if dir == 'right':
                    robot.right(100,0.5)
                elif dir == 'left':
                    robot.left(100, 0.5)
                elif dir == 'go':
                    break
                elif dir == 'quit':
                    going = False
                    io.output(25, io.LOW)
					break
            else:
                #print('should be controlled')
                queueLock.release()
            	robot.forward(100, 0.5)

def calcprob_run(lastlux):
	a = 0.02
	b = -0.8
	dt = 0.2
	thislux = LightSensor.calculateLux()
	delta = (thislux-lastlux)
	lmbda = np.exp(-1*a*delta + b)
	p = lmbda*dt*np.exp(-lmbda*dt)
	return thislux, p

def calcprob_sweep(lastlux, a, b):
	thislux = LightSensor.calculateLux()
	#print(lastlux)
	delta=(thislux-lastlux)
	p=1/(1+np.exp(a*(-1*(float(delta)/5)-b)))
	return thislux, p

def newrun(rang, lastlux):
	#begin with short run
	dt = 0.2
	robot.forward(150, 0.2)
	#judge how life is going improving
	thislux, pt = calcprob_run(lastlux)
	#print(thislux)
	#print("P-turn is")
	r = np.random.rand() 
	if r>pt:
		#life is good
        newlux = thislux
	else:
		#life is bad, do sweeps
		t = np.random.rand()
		if t>0.5:
    		#sweep left
    		headsweep(robot.left, (0.4,0.6), thislux, 0)
    	else:
    		#sweep right
			headsweep(robot.right, (0.4,0.6), thislux, 0)
	#return newlux

def headsweep(dir, rang, lastlux, count):
    #print("head sweep")
	#initial sweep
	dir(100, np.random.uniform(rang[0],rang[1]))
	#take reading
	thislux, pa = calcprob_sweep(lastlux, 1, 0.85)
	#print(thislux)
	w = np.random.rand()
	
	if w>pa:
		# doubles range after first reject
		# to sweep back through center
        if count == 0:
            rang = rang*2
		#print(count)
		count += 1
		# initiate new run after four rejects
		if count > 3:
			dir = "go on"
			flashturn(dir)
		#print("Rejected;")
		elif dir == robot.left:
			headsweep(robot.right, rang, lastlux, count)
		else:
			headsweep(robot.left, rang, lastlux, count)
	else:
        flashturn(dir)
		#print("gonna start new run " + str(thislux))
        #return thislux

def flashturn(dir):
	if dir == robot.left:
		io.output(27, io.HIGH)
		time.sleep(0.2)
		io.output(27, io.LOW)
	elif dir == robot.right:
		io.output(5, io.HIGH)
		time.sleep(0.2)
		io.output(5, io.LOW)
	else:
		io.output(20, io.HIGH)
		time.sleep(0.2)
		io.output(20, io.LOW)

queueLock = threading.Lock()
workQueue = Queue.Queue(0)	
threads = []
			
thread1 = motionThread(1, "Motion", workQueue)
thread1.start()
threads.append(thread1)

thread2 = listenerThread(2, "Listener", workQueue)
thread2.start()
threads.append(thread2)
