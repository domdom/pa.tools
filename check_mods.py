import os
import os.path

from mod.validate import validate_mod_files

from urllib.request import urlopen
import json

temp_mod_dir = './tmp/mods'
temp_issue_dir = './tmp/issues'
url = "https://pamm-mereth.rhcloud.com/api/mod"
api_mods = json.loads(urlopen(url).read().decode('UTF-8'))

from collections import defaultdict
import operator

counter = defaultdict(int)
for mod in api_mods:
    for tag in mod.get('category', []):
        counter[tag.lower()] += 1

sorted_x = reversed(sorted(counter.items(), key=operator.itemgetter(1)))
for k, v in sorted_x:
    print(v, k)

exit()
# download all the mods (maybe compare to the cache?)
# validate each mod
# print results

def _download_mods(api_mods):
    from io import BytesIO
    from urllib.request import urlopen
    from zipfile import ZipFile

    if not os.path.exists(temp_mod_dir): os.makedirs(temp_mod_dir)


    for i, mod in enumerate(api_mods):
        mod_id = mod['identifier']
        mod_url = mod['url']

        print (i, '/', len(api_mods), '-', mod_id)

        mod_path = os.path.join(temp_mod_dir, mod_id)

        #############
        try:
            if not os.path.exists(mod_path):
                print ('Downloading', mod_id, ':', mod_url)
                with urlopen(mod_url) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall(mod_path)
            else:
                print ('Skipping download of', mod_id, ':', mod_url)
        except:
            print('Failed to download', mod_id)
            continue

def _validate_mods(api_mods):
    if not os.path.exists(temp_issue_dir): os.makedirs(temp_issue_dir)

    print('================== VALIDATING MODS')
    for i, mod in enumerate(api_mods):
        mod_id = mod['identifier']

        print(i, '/', len(api_mods), '-', mod_id, end='')

        mod_path = os.path.join(temp_mod_dir, mod_id)

        import glob
        glob_result = glob.glob(os.path.join(mod_path, '**','modinfo.json'), recursive=True)

        if len(glob_result) == 0:
            print(' - FAIL: Could not find modinfo for')
            continue

        modinfo_path = glob_result[0]
        mod_path = os.path.dirname(modinfo_path)

        modIssues = validate_mod_files(mod_path)

        print (' - [', len(modIssues.missing) + len(modIssues.parseErrors), ']')

        file_map = modIssues.missing
        json_map = modIssues.parseErrors

        # skip if there are no issues
        if len(file_map) == 0 and len(json_map) == 0:
            continue

        mod_issue_path = os.path.join(temp_issue_dir, mod_id + '.txt')

        with open(mod_issue_path, 'w') as mod_issue_file:
            print(mod['display_name'], file=mod_issue_file)
            print('=' * len(mod['display_name']), file=mod_issue_file)
            print('missing files:', modIssues.getMissingFileCount(), file=mod_issue_file)
            print('  json errors:', modIssues.getJsonErrorCount(), file=mod_issue_file)

            print('',file=mod_issue_file)

            print('MISSING FILES ' + str(modIssues.getMissingFileCount()) + ' ', file=mod_issue_file)
            print('=' * len('MISSING FILES ' + str(modIssues.getMissingFileCount()) + ' '), file=mod_issue_file)

            if len(file_map) > 0:
                for file, refs in file_map.items():
                    print (file, '   not found, referenced by:', file=mod_issue_file)
                    for ref in refs:
                        print('      - ', ref, file=mod_issue_file)

            print('',file=mod_issue_file)
            
            print('JSON ERRORS ' + str(modIssues.getJsonErrorCount()) + ' ', file=mod_issue_file)
            print('=' * len('JSON ERRORS ' + str(modIssues.getJsonErrorCount()) + ' '), file=mod_issue_file)
            if len(json_map) > 0:
                for file, errors in json_map.items():
                    for error in errors:
                        print(error, file=mod_issue_file)

    print('------------------ DONE')


# _download_mods(api_mods)
# _validate_mods(api_mods)

api_mods = [{'identifier':'com.pa.domdom.laser_unit_effects'}]

for i, mod in enumerate(api_mods):
    mod_id = mod['identifier']
    if 'com.pa.domdom.laser' not in mod_id: continue

    mod_path = os.path.join(temp_mod_dir, mod_id)

    from mod.checker import Checker

    checker = Checker()
    checker.check(mod_path)
    checker.printReport()






