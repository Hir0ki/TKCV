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
    def __init__(self, thread_count, input_dir, output_dir, working_size):
        self.working_size = working_size
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
        return inactivThreads

    def free_threads(self):
        free_threads = []
        for i, thread in enumerate(self.threads):
            if thread.need_work is True:
                free_threads.append(i)
        return free_threads

    def check_is_thead_still_working(self):
        for thread in self.threads:
            if thread.isAlive() is True:
                thread.working = False 
            else:
                return True

    def stop_all_threads(self):
        for thread in self.threads:
            thread.working = False

    def add_work_to_thread(self, n, image_range):
        self.threads[n].next_range = image_range
        self.threads[n].need_work = False 

    def start_thread(self, n, image_range):
        self.threads[n].next_range = image_range
        self.threads[n].need_work = False
        self.threads[n].start()

    def get_next_frame_range(self):
        frame_range = (self.current_count, self.current_count + self.working_size)
        self.current_count = frame_range[1]
        return frame_range

    def start(self):
        self.create_threads()
        #Start all Threads 
        inactivThreads = self.check_thead_working()
        for n in inactivThreads:
            self.start_thread(n, self.get_next_frame_range())
        
        while self.current_count < self.image_count + self.working_size +1:
           for n in self.free_threads():
               self.add_work_to_thread(n, self.get_next_frame_range())
        print("All work is distiebuted")
                

        while True:
            free_threads = self.free_threads()
            if len(free_threads) == self.thread_count:
                break
        print("All Work is done")
        self.stop_all_threads()
        print("All Threads are stopt")


config = get_config()
orcast = thread_orcastrator(
    config["thread_count"], config["input_path"], config["output_path"], config["working_size"]
)

orcast.start()
print("Done")


