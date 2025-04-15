
import os
import configparser

class metadata:
    def __init__(self, part_id, material, author):
        self.part_id = part_id
        self.material = material
        self.author = author

class GeometryStore:
    
    def __init__(self):  
        pass

    def __init__(self, start_directory):
        self.create_dir_structure(start_directory)
        return

    def create_dir_structure(start_directory):
        try:
            config = configparser.ConfigParser()
            ini_path = os.path.join(os.getcwd(),'config.ini')
            config.read(ini_path)
            dir_count = 0

            while True:
                dir_header = 'dir'+str(dir_count)
                dir = config.get('PARENT_DIRS',dir_header)
                if dir:
                    os.makedirs( str(start_directory) + "/" + str(dir) )
                else:
                    break
                dir_count+=1

        except Exception as e:
            return "ERROR: "+str(e)
        
    def store_geometry(self, source_file_path, metadata):
        write()
        metadata.part_id
        metadata.material
        metadata.author

    def retrieve_geometry(self, file_id):

    def get_metadata(self, file_id):
