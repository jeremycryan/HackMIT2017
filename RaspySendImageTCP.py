# Adapted from http://picamera.readthedocs.io/en/release-1.9/recipes1.html#capturing-to-a-network-stream

import io
import socket
import struct
import time
import cv2

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 50001))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    capture = cv2.VideoCapture(1)
    # Start a preview and let the camera warm up for 2 seconds


    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()
    if capture.isOpened(): # try to get the first frame
        frame_captured, frame = capture.read()
    else:
        frame_captured = False
    while frame_captured:


        connection.write(struct.pack('>L', byte_string(frame)))
        connection.flush()

        stream.seek(0)
        connection.write(stream.read())

        stream.seek(0)
        stream.truncate()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # for foo in camera.capture_continuous(stream, 'jpeg'):
        #     # Write the length of the capture to the stream and flush to
        #     # ensure it actually gets sent
        #     connection.write(struct.pack('<L', stream.tell()))
        #     connection.flush()
        #     # Rewind the stream and send the image data over the wire
        #     stream.seek(0)
        #     connection.write(stream.read())
        #     # If we've been capturing for more than 30 seconds, quit
        #     if time.time() - start > 30:
        #         break
        #     # Reset the stream for the next capture
        #     stream.seek(0)
        #     stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()

def byte_string(frame):
    byte_list = []
    for x in frame:
        for y in x:
            for z in y:
                byte_list.append(str(z))
    byte_list = " ".join(byte_list)
