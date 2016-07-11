class Checker:
    def __init__(self):
        self.modinfo_issues = []
        self.file_issues = {}
        self.json_issues = {}

    def check(self, mod_path):
        from .load import Loader
        from os.path import join

        mod_root = _find_mod_root(mod_path)

        loader = Loader(mod_root)
        modinfo_path = loader.resolveFile('/modinfo.json')

        if modinfo_path is None:
            self.addInfoIssue('FATAL: Could not find modinfo.json')
            return

        modinfo = checkModinfo(modinfo_path, loader)

        if modinfo is None:
            return



    def checkModinfo(modinfo_path, loader):
        modinfo, warnings = loader.loadJson(modinfo_path)
        self.addJsonIssue(modinfo_path, warnings)

        if modinfo is None:
            self.addInfoIssue('FATAL: Could not parse modinfo.json')
            return

        new_modinfo = {}
        for key, value in modinfo:
            new_modinfo[key.lower()] = value
        modinfo = new_modinfo
        # author field - string - manditory, not empty
        if modinfo.get('author', '') == '':
            self.addInfoIssue('ERROR: Mandatory field "author" is missing or empty.')

        # build field - string - manditory, build number
        if modinfo.get('build', '') == '':
            self.addInfoIssue('ERROR: Mandatory field "build" is missing or empty.')

        # build field - string - manditory, build number
        category = modinfo.get('category', None)
        if category is None:
            self.addInfoIssue('ERROR: Mandatory field "category" is missing.')
        elif category == []:
            self.addInfoIssue('WARNING: "category" field is empty. Use category keywords to make your mod easier to search for.')
        elif isinstance(category, list):
            redundant_keywords = set(['mod', 'client', 'client-mod', 'server', 'server-mod'])
            prefered_keyword_mapping = {
                # maps
                'map': 'maps',
                'planet': 'maps',
                'planets': 'maps',
                'system': 'maps',
                'systems': 'maps',

                'effect': 'effectss',
                'live-game': 'gameplay',
            }
            for item in category:
                if not isinstance(item, str):
                    self.addInfoIssue('ERROR: "category" array contains a non-string element: ' + str(item))
                else:
                    if item in redundant_keywords:
                        self.addInfoIssue('WARNING: "category" array contains a redundant entry: '+ item +'. Please remove this entry.')
                    if item in prefered_keyword_mapping:
                        self.addInfoIssue('WARNING: "category" array contains a redundant entry: '+ item +'. Please use "' + prefered_keyword_mapping[item] + '" instead.')


            if len(redundant_keywords & set(category)) > 0:

        else:
            self.addInfoIssue('ERROR: "category" field must be an array of strings.')


        # build field - string - manditory, build number
        if modinfo.get('build', '') == '':
            self.addInfoIssue('Mandatory field "build" is missing or empty.')


       
"""
143 in-game
129 ui
52 titans
45 Texture
28 shader
27 server-mod
26 maps
24 effects
21 units
21 client-mod
17 lobby
16 map
16 planets
15 planet
15 system
15 pack
15 systems
13 Strategic-icons
13 colours
12 explosion
12 galactic-war
11 system-editor
8 biome
7 classic
7 cheat
7 framework
7 game-mode
6 bugfix
6 metal
6 modding
6 hearts
5 Strategic Icons
5 strategic-icons
5 sandbox
5 chat
4 commander
4 balance
4 ai
4 reclaim
4 uberbar
3 gameplay
3 appearance
3 Balance
3 energy
3 main-menu
2 Framework
2 artillery
2 UI
2 bug-fix
2 economy
2 ai-skirmish
2 racing
2 strategic icons
2 nuke
2 system editor
2 Units
2 buildings
2 particles
2 settings
2 Commander
2 mex
2 In-game
2 player-guide
2 Planets
1 lana
1 Tropical
1 server
1 Model
1 ania
1 anti
1 the
1 stars
1 Metal
1 bug-Fix
1 replay browser
1 Icon
1 series
1 game
1 mod-help
1 Projectiles
1 Main-Menu
1 naval
1 Effects
1 alerts
1 Galactic-War
1 scale
1 construction
1 sound
1 filter
1 antinuke
1 client
1 tweak
1 Hotfix
1 twitch
1 tournaments
1 landmines
1 marshall
1 chrono-cam
1 Icons
1 Water
1 features
1 violet
1 anti-nuke
1 combat
1 system_editor
1 reference
1 selection
1 Energy Plant
1 performance
1 violetania
1 System Editor
1 live-game
1 Bugfix
1 textures
1 soundtrack
1 trails
1 Background
1 wpmarshall
1 pip
"""


    def addInfoIssue(self, issue):
        self.modinfo_issues.append(issue)

    def addJsonIssue(self, json_file, issues):
        if json_file in self.json_issues:
            self.json_issues[json_file] |= set(issues)
        else:
            self.json_issues[json_file] = set(issues)

    def addFileIssue(self, json_file, referenced_by):
        if isinstance(referenced_by, list):
            ref_set = set(referenced_by)
        elif isinstance(referenced_by, str):
            ref_set = set([referenced_by])

        if json_file in self.json_issues:
            self.json_issues[json_file] |= set(ref_set)
        else:
            self.json_issues[json_file] = set(ref_set)

    def printReport(self):
        print (self)


def _find_mod_root(mod_path):
    from os.path import join, dirname
    from glob import glob

    glob_result = glob(join(mod_path, '**','modinfo.json'), recursive=True)

    print(mod_path, glob_result)
    if len(glob_result) == 1:
        return dirname(glob_result[0])
    else:
        return None


def _check_category(category_array):
    pass