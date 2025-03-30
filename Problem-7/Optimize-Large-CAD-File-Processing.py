import multiprocessing
from pyautocad import Autocad, APoint
import os

# Multiprocessing
class Process(multiprocessing.Process):
    def __init__(self, autocad_directory, file_list, start_ind, end_ind, entity_count):
        super(Process, self).__init__()
        self.autocad_directory = autocad_directory
        self.file_list = file_list
        self.start_ind = start_ind
        self.end_ind = end_ind
        self.entity_count = entity_count

    def run(self):
        self.read_autocad_files(self.autocad_directory, self.file_list, self.start_ind, self.end_ind, self.entity_count)

    def read_chunk(self, fileObj, chunk_size=1024*32):
        while True:
            chunk = fileObj.read(chunk_size)
            if not chunk:
                return None
            else:
                yield chunk

    def read_autocad_files(self, autocad_directory, file_list, start_ind, end_ind, entity_count):   
        for index in range(start_ind, end_ind+1):
            counter=0
            file_path = os.path.join(autocad_directory, file_list[index])
            with open(file_path, 'r') as filePtr:
                for chunk in self.read_chunk(filePtr):
                    obj = Autocad.Open(chunk) # Syntax needs to be changed
                    
                    # Process and count entities

                    entity_count = obj.EntityCount() # Syntax needs to be changed
                    counter+=entity_count
            entity_count[index] = counter

if __name__ == '__main__':
    MAX_ALLOCATED_FILES = 1000
    autocad_directory = "C:/Users/vinodrao/autocad/"
    list_of_files = [filename for filename in os.listdir(autocad_directory) if filename.endswith(".step") or filename.endswith(".stl")]
    total_files = len(list_of_files)
    entity_count = [0] * total_files
    
    for index in (0, total_files, MAX_ALLOCATED_FILES):
        start = index
        end = min(index+MAX_ALLOCATED_FILES-1 , total_files-1)
        p = Process(autocad_directory, list_of_files, start, end, entity_count)
        P.start()
        P.join()