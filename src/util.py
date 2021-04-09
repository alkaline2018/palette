import os
import datetime

def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def get_dir_path_for_now(_parent_path, _strftime):
    now_date = datetime.datetime.now()
    now_dir_structure = now_date.strftime(_strftime)
    new_dir_path = _parent_path + now_dir_structure
    return new_dir_path