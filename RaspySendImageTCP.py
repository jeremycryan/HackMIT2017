# Adapted from http://picamera.readthedocs.io/en/release-1.9/recipes1.html#capturing-to-a-network-stream

import io
import socket
import struct
import time
import cv2
import array

def byte_string(frame):
    data = []
    for x in frame:
        for y in x:
            for z in y:
                data.append(chr(z))
    length = frame.shape[0] * frame.shape[1] * frame.shape[2]
    byte_length = struct.pack('bbbb', *[(length%(256**4))/(256**3), (length%(256**3))/(256**2), (length%(256**2))/256, length%256])
    length_array =  bytearray(byte_length)
    data_array = bytearray(data)
    print len(data_array + length_array)
    return length_array + data_array

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('169.254.130.102', 50001))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    capture = cv2.VideoCapture(-1)
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


        connection.write(byte_string(frame))
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
    time.sleep(1000)
finally:
    connection.close()
    client_socket.close()
