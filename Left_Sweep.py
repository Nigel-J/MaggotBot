#!/usr/bin/python

robot.left(172, 0.25
#take reading
thistime = LightSensor.calculateLux()
#probability of accepting
delta = (thistime-lasttime)
print delta "Lux;" + '\n'
pa = 1/(1+math.exp(-1*(float(delta)/5)-0.85)))
print "P-accept is" + pa  + '\n'
w = random.random()

if w<pa:
  #Accepted left head sweep
  robot.backward(150,0.2)
  print "Accepted;" + '\n'

else: 
  print "Rejected;" + '\n'
  robot.right(172, 0.25)
  lasttime = thistime
  os.system("Right_Sweep")
  
