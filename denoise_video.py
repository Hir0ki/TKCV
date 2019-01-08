import cv2
import time as testtime


def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


file = open("testfile.txt", "w")
video = cv2.VideoCapture("GOPR2902_orange.MP4")

_, frame = video.read()
out = cv2.VideoWriter(
    "GoPro_orange.avi",
    cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    10,
    (int(frame.shape[1]), int(frame.shape[0])),
)
start_time = testtime.time()
count = 0
lines = []

while True:
    ret, frame = video.read()

    count = count + 1
    # your code execution

    if ret is True:
        e1 = cv2.getTickCount()
        frame = denoise_image(frame)
        e2 = cv2.getTickCount()
        time = (e2 - e1) / cv2.getTickFrequency()

        out.write(frame)
        print("Frame: {} done;".format(count))
        file.write("Frame: {} done;".format(count))
        file.write("Time for process: {};".format(time))
        file.write("Frame: {} done;".format(count))
    else:
        break

end_time = testtime.time()

file.write("---------------")
file.write(str(start_time) + ";")
file.write(str(end_time) + ";")
file.write(str(end_time - start_time) + ";")

file.close()
