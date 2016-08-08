lasttime=0
thistime=0

while True:
        thistime=LightSensor.calculateLux()
        print thistime - lasttime, "Lux"

        robot.backward(150,0.2)

        delta=(thistime-lasttime)
        pt=1/(1+math.exp(-1*(-1*(float(delta)/5)-0.5)))
        print pt
        r = random.random()
        if r<pt:
                robot.left(172, random.random())
                print "Turn;"+'\n'
        else:
                robot.backward(150, 0.3)
                print "Run;"+'\n'

        lasttime = thistime;
