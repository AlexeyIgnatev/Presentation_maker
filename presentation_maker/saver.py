import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def check_path(path):
    path = os.path.join(ROOT_DIR, path)
    if not os.path.exists(path):
        os.mkdir(path)


def path_to_file(file):
    return os.path.join(ROOT_DIR, file)
