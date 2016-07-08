from . import paths
from . import load
from . import pajson

from json import JSONDecodeError

class ModIssues:
    def __init__(self):
        self.missing = {}
        self.parseErrors = {}

    def missingFile(self, missingFile, refercingFile):
        if missingFile in self.missing:
            self.missing[missingFile].add(refercingFile)
        else:
            self.missing[missingFile] = {refercingFile}

    def invalidJson(self, jsonFile, parsingErrors):
        if jsonFile in self.parseErrors:
            self.parseErrors[jsonFile].add(parsingErrors)
        else:
            self.parseErrors[jsonFile] = set(parsingErrors)





def validate_modinfo(modinfo):
    """
    Validates the modinfo for a particular mod.
    """
    print('Validating modinfo using rules from https://wiki.palobby.com/wiki/Planetary_Annihilation_Mod_Structure')
    pass


def validate_mod_files(mod_dir):
    """ Checks for missing files. """
    loader = load.Loader(paths.PA_MEDIA_DIR)
    loader.mount('/pa', '/pa_ex1')
    loader.mount('/', mod_dir)

    return _find_missing_files(loader)


def _find_missing_files(loader):
    visited = set()
    modIssues = ModIssues()
    file_path = '/pa/units/unit_list.json'
    referenced_by = 'PA Engine'

    _walk_json(loader, visited, modIssues, file_path, referenced_by)

    return modIssues


def _walk_json(loader, visited, modIssues, file_path, referenced_by):
    visited.add(file_path)

    resolved_file = loader.resolveFile(file_path)
    if resolved_file is None:
        modIssues.missingFile(file_path, referenced_by)
        return
    if not file_path.endswith('.json') and not file_path.endswith('.pfx'):
        return

    # TODO: This is a hack
    obj, warnings = loader.loadJson(resolved_file)

    if len(warnings) > 0:
        modIssues.invalidJson(resolved_file, warnings)

    file_list = _walk_obj(obj)
    for file in file_list:
        if file not in visited:
            _walk_json(loader, visited, modIssues, file, resolved_file)


def _parse_spec(spec_path):
    ret = set()
    specs = spec_path.split(' ')
    for spec in specs:
        if '/' in spec and '.' in spec:
            ret.add(spec)

    return ret


def _walk_obj(obj):
    if isinstance(obj, str):
        return _parse_spec(obj)

    specs = set()
    if isinstance(obj, dict):
        obj = list(obj.values())

    if isinstance(obj, list):
        specs = set()
        for value in obj:
            specs |= _walk_obj(value)

    return specs


if __name__ == '__main__':
    validate_mod_files('../../com.pa.domdom.laser_unit_effects')

"""
    if len(sys.argv) != 2:
        print(sys.argv[0] + ' takes one argument, the path to the folder containing modinfo.')
    elif not os.path.isdir(sys.argv[1]):
        print(sys.argv[1] + ' is not a directory.')
    elif not os.path.isfile(os.path.join(sys.argv[1], 'modinfo.json')):
        print(sys.argv[1] + ' does not contain a modinfo.json file.')
    else:
        run(sys.argv[1])
        """