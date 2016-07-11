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