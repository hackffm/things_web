import os
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(file_dir)
sys.path.append(parent_dir)


def file_delete(file_name):
    if os.path.exists(file_name):
        print('remove ' + file_name)
        os.remove(file_name)


def path_home():
    _path = os.getenv('USERPROFILE')
    if _path == '' or _path == None:
        _path = os.getenv('HOME')
    _path = str(_path)
    _path = _path.replace('\\', '/')
    return _path
