import numpy as np
import cv2

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    zeros = np.asarray([[[np.uint8(0)]]*640]*480)
    a = (frame/2)[:, :, 0].reshape(480, 640, 1)
    b = zeros
    c = (frame2/3*2)[:, :, 0].reshape(480, 640, 1)
    res = np.concatenate([a, a, c], 2)
    print type(res[0][0][0])
    # Display the resulting frame
    cv2.imshow('frame', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
