import json
import os.path

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

    # returns True if any of the roots has that file
    def hasFile(self, path):
        for i in range(len(self.mounts)):
            mounts = self.mounts[-i:]

            file_path = path + ''
            for mount_point, mount_path in mounts:
                if file_path.startswith(mount_point):
                    file_path = mount_path + '/' + file_path[len(mount_point):]
                    file_path.replace("\\","/")
                    file_path.replace("//","/")

            if os.path.isfile(file_path):
                return True

        return False

    # loads Json of the given path
    def loadJson(self, path):
        attempted_paths = []
        for i in range(len(self.mounts)):
            mounts = self.mounts[-i:]

            file_path = path + ''
            for mount_point, mount_path in mounts:
                if file_path.startswith(mount_point):
                    file_path = mount_path + '/' + file_path[len(mount_point):]
                    file_path.replace("\\","/")
                    file_path.replace("//","/")

            attempted_paths.append(file_path)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    return json.load(file)

        raise FileNotFoundError('Could not find the file ' + path + ' relative to any roots. (' + json.dumps(attempted_paths) + ')')

