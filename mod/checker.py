class Checker:
    def __init__(self):
        self.modinfo = None
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

        modinfo = self.checkModinfo(modinfo_path, loader)

        if modinfo is None:
            return

    
    def checkModinfo(self, modinfo_path, loader):
        modinfo, warnings = loader.loadJson(modinfo_path)
        self.addJsonIssue(modinfo_path, warnings)

        mandatory_fields = [
            'author',
            'build',
            'category',
            'context',
            'date',
            'description',
            'display_name',
            'forum',
            'identifier',
            'signature',
            'version'
        ]

        if modinfo is None:
            self.addInfoIssue('FATAL: Could not parse modinfo.json')
            return

        new_modinfo = {}
        for key, value in modinfo.items():
            new_modinfo[key.lower()] = value
        modinfo = new_modinfo


        for field in mandatory_fields:
            field_value = modinfo.get(field, None)

            if field_value == '':
                self.addInfoIssue('ERROR: Mandatory field "'+field+'" is empty.')
            if field_value is None:
                self.addInfoIssue('ERROR: Mandatory field "'+field+'" is missing.')

            modinfo[field] = field_value


        # build - string - mandatory, build number
        category = modinfo.get('category', None)
        if category == []:
            self.addInfoIssue('WARNING: "category" field is empty. Use category keywords to make your mod easier to search for.')
        elif isinstance(category, list):
            redundant_keywords = set(['mod', 'client', 'client-mod', 'server', 'server-mod'])
            prefered_keyword_mapping = {
                'map': 'maps',
                'planet': 'maps',
                'planets': 'maps',
                'system': 'maps',
                'systems': 'maps',

                'texture':'textures',
                'unit': 'units',
                'buildings':'units',
                'particle': 'effects',
                'effect': 'effects',
                'live-game': 'gameplay',
                'in-game': 'gameplay',
                'strategic-icons': 'icons',
                'strategic icons': 'icons',
                'icon': 'icons',

                'bug-fix': 'fix',
                'bugfix': 'fix',
                'hot-fix': 'fix',
                'hotfix': 'fix'
            }
            for item in category:
                if not isinstance(item, str):
                    self.addInfoIssue('ERROR: "category" array contains a non-string element: ' + str(item))
                else:
                    if item.lower() in redundant_keywords:
                        self.addInfoIssue('WARNING: "category" array contains a redundant entry: '+ item +'. Please remove this entry.')
                    if item.lower() in prefered_keyword_mapping:
                        self.addInfoIssue('WARNING: "category" array contains a redundant entry: '+ item +'. Please use "' + prefered_keyword_mapping[item.lower()] + '" instead.')
        elif category is not None:
            self.addInfoIssue('ERROR: "category" field must be an array of strings.')

        
        # context - string - mandatory, server or client
        context = modinfo.get('context', None)
        if context not in ['client', 'server']:
            self.addInfoIssue('ERROR: "context" is must be either "client", or "server".')


        # store reference to the modinfo
        self.modinfo = modinfo



    def addInfoIssue(self, issue):
        self.modinfo_issues.append(issue)

    def addJsonIssue(self, json_file, issues):
        if json_file in self.json_issues:
            self.json_issues[json_file] |= set(issues)
        else:
            self.json_issues[json_file] = set(issues)

    def addFileIssue(self, file_name, referenced_by):
        if isinstance(referenced_by, list):
            ref_set = set(referenced_by)
        elif isinstance(referenced_by, str):
            ref_set = set([referenced_by])

        if file_name in self.file_issues:
            self.file_issues[file_name] |= set(ref_set)
        else:
            self.file_issues[file_name] = set(ref_set)

    def printReport(self):
        report = ""

        def make_heading(heading, underline_character): return heading + "\n" + underline_character * len(heading) + "\n"
        def line(string=''): return string + "\n"

        # basic details about the mod
        if self.modinfo is not None:
            report += make_heading('MOD DETAILS', '=')
            report += line("      name: " + self.modinfo['display_name'])
            report += line("        id: " + self.modinfo['identifier'])
            report += line("    author: " + self.modinfo['author'])
            report += line("     forum: " + self.modinfo['forum'])
            report += line()

        # listing issues with the modinfo files
        report += make_heading('MODINFO ISSUES ' + str(len(self.modinfo_issues)), '-')
        for modinfo_issue in self.modinfo_issues:
            report += line(modinfo_issue)
        report += line()


        return report

def _find_mod_root(mod_path):
    from os.path import join, dirname
    from glob import glob

    glob_result = glob(join(mod_path, '**','modinfo.json'), recursive=True)

    print(mod_path, glob_result)
    if len(glob_result) == 1:
        return dirname(glob_result[0])
    else:
        return None






"""
        145 in-game
        131 ui
        52 titans
        45 texture
        28 shader
        27 server-mod
        26 maps
        25 effects
        23 units
        21 client-mod
        18 strategic-icons
        18 planets
        17 lobby
        16 map
        15 systems
        15 pack
        15 planet
        15 system
        13 colours
        13 galactic-war
        12 explosion
        11 system-editor
        9 framework
        8 biome
        7 classic
        7 game-mode
        7 cheat
        7 metal
        7 balance
        7 bugfix
        7 strategic icons
        6 commander
        6 hearts
        6 modding
        5 sandbox
        5 chat
        4 main-menu
        4 reclaim
        4 ai
        4 uberbar
        3 system editor
        3 gameplay
        3 energy
        3 bug-fix
        3 appearance
        2 settings
        2 economy
        2 racing
        2 mex
        2 artillery
        2 player-guide
        2 particles
        2 buildings
        2 ai-skirmish
        2 nuke
        1 lana
        1 tweak
        1 twitch
        1 landmines
        1 pip
        1 features
        1 projectiles
        1 client
        1 game
        1 anti-nuke
        1 sound
        1 server
        1 performance
        1 energy plant
        1 icons
        1 combat
        1 violet
        1 alerts
        1 water
        1 tropical
        1 naval
        1 soundtrack
        1 mod-help
        1 the
        1 wpmarshall
        1 filter
        1 stars
        1 icon
        1 reference
        1 scale
        1 ania
        1 live-game
        1 violetania
        1 marshall
        1 selection
        1 chrono-cam
        1 replay browser
        1 system_editor
        1 construction
        1 antinuke
        1 trails
        1 anti
        1 background
        1 tournaments
        1 model
        1 hotfix
        1 series
        1 textures
        """
