import json
import os.path

class Loader:
    def __init__(self, rootPath):
        self.roots = [rootPath]

    # returns True if any of the roots has that file
    def hasFile(self, path):
        if path and len(path) > 1 and path[0] == "/":
            path = path[1:]

        for root in self.roots:
            p = os.path.join(root, path)
            if os.path.isfile(p):
                return True
        return false

    # loads Json of the given path
    def loadJson(self, path):
        if path[0] == "/":
            path = path[1:]
        for root in self.roots:
            p = os.path.join(root, path)
            if os.path.isfile(p):
                with open(p, 'r') as file:
                    return json.load(file)
        raise FileNotFoundError('Could not find the file ' + path + ' relative to any roots (' + json.dumps(roots) + ')')


