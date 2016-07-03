import os
import os.path
import re

# get unit list (perfer local, then mod version)
# crawl unit list for all used files

"""
Finds and returns the location of PA's user data folder
"""
def find_data_dir():
    # check each possible location for PA log files.
    path = os.path.normpath(os.path.join(os.getenv('USERPROFILE'), 'AppData/local/Uber Entertainment/Planetary Annihilation'))
    if os.path.isdir(path):
        return path

    path = os.path.normpath(os.path.join(os.getenv('HOME'), ".local/Uber Entertainment/Planetary Annihilation"))
    if os.path.isdir(path):
        return path

    path = os.path.normpath(os.path.join(os.getenv('HOME'), "Library/Application Support/Uber Entertainment/Planetary Annihilation"))
    if os.path.isdir(path):
        return path

    raise FileNotFoundError('Could not find the PA user data directory.')

"""
Reads PA's logs to find the last used PA media directory.
"""
def find_media_dir():
    data_dir = find_data_dir()
    log_dir = os.path.join(data_dir, 'log')

    if not os.path.isdir(log_dir):
        raise FileNotFoundError('Could not find the log directory.')

    log_files = os.listdir(log_dir)
    log_files = map(lambda x: os.path.join(log_dir, x), log_files)
    log_files = sorted(log_files, key=os.path.getctime)

    for log_file in log_files:
        with open(log_file) as log:
            for line in log:
                m = re.search(r'INFO Coherent host dir: "([^"]*)"', line)
                if m:
                    base_path = m.group(1)

                    if not os.path.isdir(base_path): raise FileNotFoundError('Could not find PA directory.')

                    path = os.path.normpath(os.path.join(base_path, '../../media'))
                    if os.path.isdir(path): return path

                    path = os.path.normpath(os.path.join(base_path, '../../Resources/media'))
                    if os.path.isdir(path): return path

                    raise FileNotFoundError('Could not find PA media directory. You must play the game at least once for this directory to be detected.')






