import cv2


def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


def resize_frame(frame):
    width = int(frame.shape[1] / 1)
    height = int(frame.shape[0] / 1)
    dim = (width, height)
    # resize image
    frame = cv2.resize(frame, dim)
    return frame


video = cv2.VideoCapture("GOPR2902_orange.MP4")

_, frame = video.read()
out = cv2.VideoWriter(
    "GoPro_orange.avi",
    cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    10,
    (int(frame.shape[1]), int(frame.shape[0])),
)

count = 0
while True:
    count = count + 1
    ret, frame = video.read()

    if ret is True:
        frame = denoise_image(frame)
        out.write(frame)
        print("Frame: {} done".format(count))
    else:
        break

