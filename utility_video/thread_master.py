from threded_image_processing import processing_thread
from os import listdir
import json


def get_config():
    file = open("config.json", "r")
    json_string = file.read(90000)
    
    return json.loads(json_string)

def get_image_count(path):
    all_images = listdir(path)
    return len(all_images)



class thread_orcastrator():

    def __init__(self, thread_count, input_dir, output_dir):
        self.thread_count = thread_count
        self.current_count = 1
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.threads = []
        self.image_count = get_image_count(input_dir)

    def create_threads(self):

        for n in range(self.thread_count):
            self.threads.append(processing_thread(n, 'image_thread', self.input_dir, self.output_dir))

    def check_thead_working(self):
        index = 0
        inactivThreads = []
        for thread in self.threads:
            if thread.isAlive() is False:
                inactivThreads.append(index)
            index = index + 1
        print(inactivThreads)    
        return inactivThreads
            
    def run_thread(self, n, image_range):
        self.threads[n].run(image_range)

    def get_next_frame_range(self):
        frame_range = (self.current_count, self.current_count + 100)
        self.current_count = self.current_count + 100
        return frame_range
         
    def start(self):
        self.create_threads()

        while True : #self.current_count < self.image_count
            
            inactivThreads = self.check_thead_working()
            
            for n in inactivThreads:

                self.run_thread(n, self.get_next_frame_range())


config = get_config()
print(config)
orcast = thread_orcastrator(config['thread_count'], config['input_path'], config['output_path'])
    
orcast.start()



