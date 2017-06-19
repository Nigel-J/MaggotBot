#!/usr/bin/python

robot.right(172, 0.25)
#take reading
thistime = LightSensor.calculateLux()
#probability of accepting
delta = (thistime-lasttime)
print delta "Lux;" + '\n'
pa = 1/(1+math.exp(-1*(float(delta)/5)-0.85)))
# Print probablility of accepting? print pa  + '\n'
w = random.random()

if w<pa:
  #Accepted right head sweep
  robot.backward(150,0.2)
  print "Accepted;" + '\n'
  
else: 
  print "Rejected;" + '\n'
  robot.left(172, 0.25)
  lasttime = thistime
  os.system("Left_Sweep.py")
