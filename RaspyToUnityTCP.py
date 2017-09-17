# Adapted from https://stackoverflow.com/questions/38816660/sending-data-from-unity-to-raspberry

import socket

backlog = 1
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('trying to connect')
s.connect(('10.182.5.29', 50000))
try:
    print ("waiting")

    while 1:
        data = s.recv(size)
        if data:
            print (data)
            s.send(data)

finally:
    print("closing socket")
    s.close()
