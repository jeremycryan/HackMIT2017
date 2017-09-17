# Adapted from https://stackoverflow.com/questions/38816660/sending-data-from-unity-to-raspberry

import socket

backlog = 1
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 50000))
try:
    print ("is waiting")

    while 1:
        data = s.recv(size)
        if data:
            print (data)
            s.send(data)

finally:
    print("closing socket")
    s.close()
