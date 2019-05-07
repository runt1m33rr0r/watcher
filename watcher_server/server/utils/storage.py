import os


PERSONS_FOLDER_NAME = 'persons'
DETECTIONS_FOLDER_NAME = 'detections'
save_location = ''


def decide_save_location(instance, filename):
    return f'{save_location}/{filename}'


def set_save_location(location):
    global save_location
    save_location = location


def delete_file(file_path):
    if not os.path.isfile(file_path):
        return

    dir_path = os.path.dirname(file_path)

    os.remove(file_path)

    if not os.listdir(dir_path):
        os.rmdir(dir_path)
