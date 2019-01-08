import cv2
import numpy as np

video = cv2.VideoCapture(
    "/home/david/Projects/OpenCV/first_Test/src/TKCV/GOPR2902_orange.MP4"
)
# window = cv2.namedWindow("test")
# tracker = cv2.TrackerMedianFlow_create()


def change_color_line(frame, x, y, radius):

    x = int(x + w /2)
    y = int(y + h /2 )
    for index,n in enumerate(range(radius)):
        frame[x , y + n] = [255, 255, 255]
        frame[x, y - n] = [255, 255, 255]
    return frame


def pixel_in_color_range(min_color, max_color, pixel_color):
    for index, n in enumerate(min_color):

        if not (n <= pixel_color[index] or max_color[index] >= pixel_color[index]):
            return False
    return True


def check_if_trackwindos_on_ball(frame, track_window):
    y, x, w, h = track_window

    mid_x = int(x + w / 1.5 )
    mid_y = int(y + h / 1.5 )

    pixel_middel = frame[mid_x, mid_y]
    pixel_left = frame[mid_x - 10, mid_y]
    pixel_right = frame[mid_x + 10, mid_y]
    pixel_bottom = frame[mid_x, mid_y - 10]
    pixel_top = frame[mid_x , mid_y + 10]   
 
    print(pixel_in_color_range(ORANGE_MIN, ORANGE_MAX, pixel_left)) 
    print(pixel_in_color_range(ORANGE_MIN, ORANGE_MAX, pixel_right)) 
    print(pixel_in_color_range(ORANGE_MIN, ORANGE_MAX, pixel_top)) 

    if ( pixel_in_color_range(ORANGE_MIN, ORANGE_MAX, pixel_middel) is True ):
       
       return True
    else:
        return False


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


ORANGE_MIN = np.array([10, 60, 150])
ORANGE_MAX = np.array([70, 220, 240])


video = wait_n_seconds(800, video)

_, frame = video.read()
frame = resize_frame(frame)

track_window = cv2.selectROI("test", frame)
cv2.destroyWindow("test")
Track_is_ok = True

while True:

    ret, frame = video.read()

    if ret is True:

        frame = resize_frame(frame)

        hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_roi, ORANGE_MIN, ORANGE_MAX)

        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        if check_if_trackwindos_on_ball(frame, track_window) is not True and Track_is_ok is False :
            track_window = cv2.selectROI("test", frame)
            Track_is_ok = False 
        elif check_if_trackwindos_on_ball(frame, track_window):
            Track_is_ok = False 
        else:
            Track_is_ok = True

        print(Track_is_ok)


        # Draw it on image
        x, y, w, h = track_window
        img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow("test", img2)
        cv2.imshow("mask", mask)
        cv2.waitKey(1)


cv2.destroyAllWindows()

