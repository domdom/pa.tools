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
    base_list = _build_classic_list()

    loader = load.Loader(paths.find_media_dir())

    for file in base_list:
        if not loader.hasFile(file):
            print ("LKJFSDLKFJSDKLFJSDKLFJSDLFKJSD")



    pass

def _parse_spec(spec_path):
    ret = set()
    specs = spec_path.split(' ')
    for spec in specs:
        if '/' in spec and '.' in spec:
            ret.add(spec)

    return ret

def _walk_obj(obj):
    ret = set()
    items = []
    if isinstance(obj, dict):
        items = obj.values()
    elif isinstance(obj, list):
        items = obj

    for v in items:
        if isinstance(v, str):
            ret |= _parse_spec(v)

        elif isinstance(v, (list, dict)):
            ret |= _walk_obj(v) 

    return ret

def _walk_json(loader, unit_path, visited=None):
    if visited is None: visited = set()

    ret = set()
    if unit_path in visited: return ret

    visited.add(unit_path)
    unit = loader.loadJson(unit_path)

    unit_specs = _walk_obj(unit)

    for spec in unit_specs:
        if spec.endswith('.json'):
            ret |= _walk_json(loader, spec, visited)



    return ret | unit_specs





def _build_classic_list():
    specs = set()

    media_dir = paths.find_media_dir()
    loader = load.Loader(media_dir)

    visited = set()
    units = loader.loadJson('pa/units/unit_list.json')['units']

    for unit_path in units:
        specs.add(unit_path)
        specs |= _walk_json(loader, unit_path, visited)

    return units

def _build_titans_list():
    specs = set()

    media_dir = paths.find_media_dir()
    loader = load.Loader(media_dir)

    visited = set()
    units = loader.loadJson('pa_ex1/units/unit_list.json')['units']

    for unit_path in units:
        specs.add(unit_path)
        specs |= _walk_json(loader, unit_path, visited)

    return units









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