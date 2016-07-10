class Checker:
    def __init__(self):
        self.modinfo_issues = []
        self.file_issues = {}
        self.json_issues = {}

    def check(self, mod_path):
        mod_root = _find_mod_root(mod_path)
        pass


def _find_mod_root(mod_path):
    from os.path import join
    from glob import glob

    glob_result = glob(join(mod_path, '**','modinfo.json'), recursive=True)

    if len(glob_result) == 1:
        return glob_result[0]
    else:
        return None
