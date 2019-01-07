from threded_image_processing import processing_thread
from os import listdir
import json
import time


def get_config():
    file = open("config.json", "r")
    json_string = file.read(90000)
    return json.loads(json_string)


def get_image_count(path):
    all_images = listdir(path)
    return len(all_images)


class thread_orcastrator:
    def __init__(self, thread_count, input_dir, output_dir):
        self.thread_count = thread_count
        self.current_count = 1
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.threads = []
        self.image_count = get_image_count(input_dir)

    def create_threads(self):

        for n in range(self.thread_count):
            self.threads.append(
                processing_thread(n, "image_thread", self.input_dir, self.output_dir)
            )

    def check_thead_working(self):
        index = 0
        inactivThreads = []
        for thread in self.threads:
            if thread.isAlive() is False:
                inactivThreads.append(index)
            index = index + 1
        print(inactivThreads)
        return inactivThreads

    def check_is_thead_still_working(self):
        for thread in self.threads:
            if thread.isAlive() is True:
                return True
            else:
                return False

    def run_thread(self, n, image_range):
        print(n)
        self.current_count = image_range[1]
        print(image_range[1])
        self.threads[n].next_range = image_range
        self.threads[n].start()

    def get_next_frame_range(self):
        frame_range = (self.current_count, self.current_count + 100)
        
        return frame_range

    def start(self):
        self.create_threads()

        while self.current_count < self.image_count:
            inactivThreads = self.check_thead_working()

            for n in inactivThreads:

                self.run_thread(n, self.get_next_frame_range())

        while True:
            if self.check_is_thead_still_working() is False:
                break
            else:
                time.sleep(1)


config = get_config()
orcast = thread_orcastrator(
    config["thread_count"], config["input_path"], config["output_path"]
)

orcast.start()

