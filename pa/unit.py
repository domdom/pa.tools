"""
unit.py - 28 Aug 2016

This class represents some unit spec in PA. This includes ammo and weapon specs as well.
"""

from .load import Loader

from glob import glob

def match(pattern, loader):
    """ Matches the unit spec pattern and yields the resulting units """
    paths = loader.resolveGlob(pattern)
    for path in paths:
    	yield Unit(path, loader)


class Unit:
    def __init__(self, spec_path, loader):
    	# path relative to root of this unit's spec
        self.spec_path = spec_path
        # loader object, which we can use to get a json
        self.loader = loader
        pass

    # loads the unit from it's path
    def load():
    	pass

    # merges the data json into the current unit
    def merge(data):
    	pass

    def store():
    	pass



