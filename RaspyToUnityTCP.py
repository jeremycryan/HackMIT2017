# Adapted from https://stackoverflow.com/questions/38816660/sending-data-from-unity-to-raspberry

import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

lF = 3
lR = 5
rF = 7
rR = 11

GPIO.setup(lF, GPIO.OUT)
GPIO.setup(lR,GPIO.OUT)
GPIO.setup(rF,GPIO.OUT)
GPIO.setup(rR,GPIO.OUT)

backlog = 1
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('trying to connect')
s.connect(('169.254.130.102', 50000))
try:
    print ("waiting")

    while 1:
        data = s.recv(size)
        if data:
	    powerValues = []
	    curr = ""
	    for i in data:
		print(i)
		if (str(i) == " "):
			powerValues.append(curr)
			curr = ""
		else:
			curr += str(i)
            powerValues.append(curr)
            powerValues[0] = int(powerValues[0])
            powerValues[1] = int(powerValues[1])	
            print (powerValues)
	    if(powerValues[0]>100):
                GPIO.output(lF,1)
		GPIO.output(lR, 0)
            elif(powerValues[0]<-100):
                GPIO.output(lF,0)
                GPIO.output(lR,1)
            else:
                GPIO.output(lF,0)
                GPIO.output(lR,0)
            if(powerValues[1]>100):
                GPIO.output(rF,1)
                GPIO.output(rR,0)
            elif(powerValues[1]<-100):
                GPIO.output(rF,0)
                GPIO.output(rR,1)
            else:
                GPIO.output(rF,0)
                GPIO.output(rR,0)
            s.send(data)

finally:
    print("closing socket")
    s.close()
