import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture('Fehlerhaft.mp4')
count = 0
while(1):
    # Take each frame
    _, frame = cap.read()
    e1 = cv.getTickCount()
    # percent of original size
    width = int(frame.shape[1] / 3)
    height = int(frame.shape[0] / 3)
    dim = (width, height)
    # resize image
    frame = cv.resize(frame, dim) 
    # Convert BGR to HSV
    frame = frame[170:550, 170:900]

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    ORANGE_MIN = np.array([7, 50, 100], np.uint8)
    ORANGE_MAX = np.array([60, 180, 255], np.uint8)
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, ORANGE_MIN, ORANGE_MAX)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)
    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    print(time)
    k = cv.waitKey(5) & 0xFF
    print(count)
    if k == 27:
        break

cv.destroyAllWindows()
