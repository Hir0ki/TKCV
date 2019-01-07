import cv2
import numpy as np


def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


def resize_frame(frame):
    width = int(frame.shape[1] / 1)
    height = int(frame.shape[0] / 1)
    dim = (width, height)
    # resize image
    frame = cv2.resize(frame, dim)
    return frame


def pixel_in_color_range(min_color: np.array, max_color: np.array, pixel_color: np.array):
    for index, n in enumerate(min_color):
        if not (n <= pixel_color[index] and max_color[index] >= pixel_color[index]):
            return False
    return True


