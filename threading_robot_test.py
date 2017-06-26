import Queue
import threading
import time
import Robot
import numpy as np

LEFT_TRIM = 0
RIGHT_TRIM = 0

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

start1 = False
start2 = False

class listenerThread(threading.Thread):
        def __init__(self, threadID, name, q):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.q = q
        def run(self):
                print("Starting " + self.name)
                get_input(self.name, self.q)
                print("Exiting " + self.name)
		
def get_input(threadName, q):
        global start1
        global start2
        while True:
                data = input("->")
                queueLock.acquire()
                q.put(data)
                queueLock.release()
                #print("%s read in %s" % (threadName, data))
                if (data == "go"):
                        start1 = True
                        start2 = False
                if (data == 'out'): 
                        start1 = False
                        start2 = True
                if (data == 'quit'):
                        start1 = False
                        start2 = False
                        break

class myThread (threading.Thread):
        def __init__(self, threadID, name, q):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.q = q
        def run(self):
                print("Starting " + self.name)
                process_data(self.name, self.q)
                print("Exiting " + self.name)
		
def process_data(threadName, q):
        going = True
        move = 1
        while going:
                while not start1 and not start2:
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
                                        break
                        else:
                                queueLock.release()
                                time.sleep(1)
                while start1:
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
                                        break
                        else:
                        	queueLock.release()
                        	print('should be moving')
                        	photo_start(move)
                        	move = move*-1
                while start2:
                        queueLock.acquire()
                        if not workQueue.empty():
                                data = q.get()
                                queueLock.release()
                                if data == 'right':
                                        robot.right(100,0.1)
                                elif data == 'left':
                                        robot.left(100, 0.1)
                                elif data == 'go':
                                        break
                                elif data == 'quit':
                                        going = False
                                        break
                        else:
                                print('should be controlled')
                                queueLock.release()
                                time.sleep(1)

def photo_start(move):
        if move > 0:
                robot.forward(100,1.0)
        else:
                robot.backward(100,1.0)

queueLock = threading.Lock()
workQueue = Queue.Queue(0)
threads = []
		
thread1 = myThread(1, "Thread-1", workQueue)
thread1.start()
threads.append(thread1)

thread2 = listenerThread(2, "Listener", workQueue)
thread2.start()
threads.append(thread2)
