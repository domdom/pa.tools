import os
import os.path

from urllib.request import urlopen
import json
from pa import pajson

temp_mod_dir = './tmp/mods'
temp_issue_dir = './tmp/issues'
url = "https://pamm-mereth.rhcloud.com/api/mod"
# api_mods = json.loads(urlopen(url).read().decode('UTF-8'))

# from collections import defaultdict
# import operator

# counter = defaultdict(int)
# for mod in api_mods:
#     for tag in mod.get('category', []):
#         counter[tag.lower()] += 1

# sorted_x = reversed(sorted(counter.items(), key=operator.itemgetter(1)))
# for k, v in sorted_x:
#     print(v, k)

# exit()
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
        mod_version = mod['version']

        print(i, '/', len(api_mods), '-', mod_id)

        mod_path = os.path.join(temp_mod_dir, mod_id)

        #############
        try:
            should_download_mod = False
            if os.path.exists(mod_path):
                from os.path import join, dirname
                from glob import glob

                glob_result = glob(join(mod_path, '**','modinfo.json'), recursive=True)

                if len(glob_result) == 1:
                    modinfo_path = glob_result[0]
                    with open(modinfo_path, 'r', encoding='utf-8') as modinfo_file:
                        modinfo, warnings = pajson.load(modinfo_file)
                        if modinfo['version'] != mod_version:
                            print (modinfo['version'], mod_version)
                            should_download_mod = True
            else:
                should_download_mod = True

            if should_download_mod:
                import shutil
                shutil.rmtree(mod_path, ignore_errors=True)
                print('Downloading', mod_id, ':', mod_url)
                with urlopen(mod_url) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall(mod_path)
            else:
                print('Skipping download of', mod_id, ':', mod_url)
        except:
            print('Failed to download', mod_id)
            continue

api_mods = json.loads(urlopen(url).read().decode('UTF-8'))
_download_mods(api_mods)
# _validate_mods(api_mods)

# api_mods = [{'identifier':'com.pa.domdom.laser_unit_effects'}]

if not os.path.exists(temp_issue_dir): os.makedirs(temp_issue_dir)
for i, mod in enumerate(api_mods):
    mod_id = mod['identifier']

    mod_path = os.path.join(temp_mod_dir, mod_id)
    mod_issue_path = os.path.join(temp_issue_dir, mod_id + '.txt')

    from mod.checker import check_mod

    mod_report = check_mod(mod_path)

    print(i, '/', len(api_mods), '-', mod_id, ' - [' + str(mod_report.getIssueCount()) + ']')

    if mod_report.getIssueCount() > 0:
        with open(mod_issue_path, 'w') as mod_issue_file:
            print(mod_report.printReport(), file=mod_issue_file)
    else:
        if os.path.exists(mod_issue_path):
            os.remove(mod_issue_path)






