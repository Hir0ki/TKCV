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
