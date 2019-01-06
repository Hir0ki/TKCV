import cv2
import numpy as np

video = cv2.VideoCapture("NOFLICKER.mov")
# window = cv2.namedWindow("test")
# tracker = cv2.TrackerMedianFlow_create()


def resize_frame(frame):
    width = int(frame.shape[1] / 1)
    height = int(frame.shape[0] / 1)
    dim = (width, height)
    # resize image
    frame = cv2.resize(frame, dim)
    return frame


def wait_n_seconds(n, video):
    for num in range(n):
        _, frame = video.read()
    return video


video = wait_n_seconds(800, video)

_, frame = video.read()
frame = resize_frame(frame)

track_window = cv2.selectROI("test", frame)
cv2.destroyWindow("test")

while True:

    ret, frame = video.read()

    if ret is True:

        frame = resize_frame(frame)
    
        hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        ORANGE_MIN = np.array([10, 80, 120], np.uint8)
        ORANGE_MAX = np.array([70, 220, 240], np.uint8)
        mask = cv2.inRange(hsv_roi, ORANGE_MIN, ORANGE_MAX)

        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x, y, w, h = track_window
        img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow("test", img2)
        cv2.imshow("mask", mask)
        cv2.waitKey(1)


cv2.destroyAllWindows()

