import os


save_location = ''


def decide_save_location(instance, filename):
    return f'{save_location}/{filename}'


def set_save_location(location):
    global save_location
    save_location = location


def delete_file(file_path):
    dir_path = os.path.dirname(file_path)

    os.remove(file_path)

    if not os.listdir(dir_path):
        os.rmdir(dir_path)
