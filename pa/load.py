import json
from json import JSONDecodeError
from . import pajson

from os.path import join, isfile, normpath


def _strip_leading_slashes(path):
    while path and len(path) > 0 and path[0] == '/':
        path = path[1:]
    return path

def _join(path1, path2):
    if path1 is None or path2 is None:
        return None
    return join(path1, _strip_leading_slashes(path2))

class Loader:
    def __init__(self, rootPath):
        self.mounts = [('/', rootPath)]

    def mount(self, dest, path):
        self.mounts.insert(0, (dest, path))

    def unmount(self, dest):
        for mnt, path in self.mounts:
            if mnt == dest:
                self.mounts.remove((mnt, path))
                return

    def resolveGlob(self, path):
        from glob import glob

        for i in range(len(self.mounts)):
            mounts = self.mounts[-i:]

            file_path = path
            for mount_point, mount_path in mounts:
                if file_path.startswith(mount_point):
                    file_path = _join(mount_path, file_path[len(mount_point):])
                # if we are mounting the root, we should not propogate further
                if mount_point == '/':
                    break

            paths = glob(file_path, recursive=True)
            if paths:
                return map(paths,normpath)

        return None

    def resolveFile(self, path):
        for i in range(len(self.mounts)):
            mounts = self.mounts[-i:]

            file_path = path
            for mount_point, mount_path in mounts:
                if file_path.startswith(mount_point):
                    file_path = _join(mount_path, file_path[len(mount_point):])
                # if we are mounting the root, we should not propogate further
                if mount_point == '/':
                    break

            if isfile(file_path):
                return normpath(file_path)

        return None

    # returns True if any of the roots has that file
    def hasFile(self, path):
        return self.resolveFile(path) != None

    # loads Json of the given path
    def loadJson(self, file_path):
        if isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    return json.load(file), []
                except json.JSONDecodeError:
                    file.seek(0)
                    return pajson.load(file)

        raise FileNotFoundError('Could not find the file ' + file_path + ' relative to any roots.')

