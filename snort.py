import os
import sys
import glob
import platform
import PIL.Image
from datetime import datetime  

EXIF_DATETIME_TAG = 36867

try:
    path = sys.argv[1]
except IndexError:
    print("Path is taken as an argument")
    sys.exit(1)

if not os.path.exists(path):
    print("This path does not exist") 
    sys.exit(1)

types = ('**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.JPEG', '**/*.JPG')
files_found = []

for files in types:
    files_found.extend(glob.iglob(path + files, recursive = True))

def get_image_date(filepath):
    try:
        current_image = PIL.Image.open(filepath)
    except PIL.UnidentifiedImageError:
        return None

    exif_data = current_image._getexif()

    # getting the exif data from a file
    if exif_data is not None and EXIF_DATETIME_TAG in exif_data:
        file_taken = datetime.strptime(exif_data[EXIF_DATETIME_TAG], "%Y:%m:%d %H:%M:%S")
        return file_taken.strftime("%Y-%m-%d_%H-%M-%S")
    
    # if there's no exif data, get the birth or modification date of a file
    if platform.system() == 'Windows':
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d_%H-%M-%S")
    else:
        stat = os.stat(filepath)
        try:
            return datetime.fromtimestamp(stat.st_birthtime).strftime("%Y-%m-%d_%H-%M-%S")
        except AttributeError:
            return datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d_%H-%M-%S")
    
    return None

def get_duplicates(filename, file_extension, file_counter):
    if filename in file_counter:

        # adding +1 to duplicates if they have an identical date of creation
        file_counter[filename] += 1
        return f"{filename}_{file_counter[filename]}{file_extension}"
    else:
        file_counter[filename] = 0
        return f"{filename}{file_extension}"

file_counter = {}
for filepath in files_found:
    new_name = get_image_date(filepath) 
    
    if new_name is not None:
        dir_path = os.path.dirname(filepath)
        _, file_extension = os.path.splitext(filepath)

        unique_filename = get_duplicates(new_name, file_extension, file_counter)
        os.rename(filepath, os.path.join(dir_path, unique_filename))
        print(f"{filepath} -> {unique_filename}") 
    else:
        print(f"Skipping {filepath} because no date was found or it is not a valid image")
