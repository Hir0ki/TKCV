import cv2
import threading
from os import listdir


def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


def make_file_name(number):
    image_number = '0000000'
    number = str(number)
    number_length = len(number)
    image_number = image_number+number
    image_number = image_number[number_length:]
    file_name = "img-" + image_number + ".bmg"
    return file_name


def get_image(dir, number):
    file_name = make_file_name(number)
    path = dir + file_name
    print(path)
    cv2.imread(path)


def write_image(dir, image, number):
    file_name = file_name = make_file_name(number)
    path = dir + file_name
    cv2.imwrite(path)


class processing_thread(threading.Thread):
    def __init__(self, threadID, name, input_dir, output_dir):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self, image_range):

        for n in range(image_range[1] - image_range[0]):
            
            frame = get_image(self.input_dir, n)

            frame = denoise_image(frame)
            print("Frame: n done!")
            write_image(self.output_dir, frame, n)

