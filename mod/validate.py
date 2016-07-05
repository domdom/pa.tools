import os
import os.path
import sys

import json

import paths

import load



"""
Validates the modinfo for a particular mod.
"""
def validate_modinfo(modinfo):
    print ('Validating modinfo using rules from https://wiki.palobby.com/wiki/Planetary_Annihilation_Mod_Structure')
    pass


"""
Checks for missing files.
"""
def validate_mod_files(mod_dir):
    loader = load.Loader(paths.find_media_dir())
    loader.mount('/pa', '/pa_ex1')
    loader.mount('/', mod_dir)

    file_map = _walk_json(loader, '/pa/units/unit_list.json')
    for file, refs in file_map.items():
        if not loader.hasFile(file):
            print (file, " not found, referenced by: ", list(refs))


    # file_map = _walk_json(loader, '/pa/units/unit_list.json')
    # for file, refs in file_map.items():
    #     if not loader.hasFile(file):
    #         print (file, " not found, referenced by: ", list(refs))

def _parse_spec(spec_path):
    ret = set()
    specs = spec_path.split(' ')
    for spec in specs:
        if '/' in spec and '.' in spec:
            ret.add(spec)

    return ret

def _walk_obj(source, obj):
    items = []
    if isinstance(obj, dict):   items = obj.values()
    elif isinstance(obj, list): items = obj

    ret = {}
    for v in items:
        if isinstance(v, str):
            child_ret = _parse_spec(v)
            for v in child_ret:
                ret[v] = ret.get(v, set()) | set([source])

        elif isinstance(v, (list, dict)):
            child_ret = _walk_obj(source, v) 
            for k, v in child_ret.items():
                ret[k] = ret.get(k, set()) | v

    return ret

def _walk_json(loader, unit_path, visited=None):
    if visited is None: visited = set()

    ret = {}
    if unit_path in visited: return ret

    visited.add(unit_path)
    unit_path = loader.resolveFile(unit_path)

    if unit_path == None: return ret

    unit = loader.loadJson(unit_path)

    unit_specs = _walk_obj(unit_path, unit)
    for spec in unit_specs:
        ret[spec] = ret.get(spec, set()) | set([unit_path])

        if spec.endswith('.json') or spec.endswith('.pfx'):
            child_ret = _walk_json(loader, spec, visited)
            for k, v in child_ret.items():
                ret[k] = ret.get(k, set()) | v

    return ret









validate_mod_files('../../com.pa.domdom.laser_unit_effects')









"""
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0] + ' takes one argument, the path to the folder containing modinfo.')
    elif not os.path.isdir(sys.argv[1]):
        print(sys.argv[1] + ' is not a directory.')
    elif not os.path.isfile(os.path.join(sys.argv[1], 'modinfo.json')):
        print(sys.argv[1] + ' does not contain a modinfo.json file.')
    else:
        run(sys.argv[1])
        """