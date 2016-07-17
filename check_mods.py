import os
import os.path

from mod.validate import validate_mod_files

from urllib.request import urlopen
import json

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

        print(i, '/', len(api_mods), '-', mod_id)

        mod_path = os.path.join(temp_mod_dir, mod_id)

        #############
        try:
            if not os.path.exists(mod_path):
                print('Downloading', mod_id, ':', mod_url)
                with urlopen(mod_url) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall(mod_path)
            else:
                print('Skipping download of', mod_id, ':', mod_url)
        except:
            print('Failed to download', mod_id)
            continue

# _download_mods(api_mods)
# _validate_mods(api_mods)

# api_mods = [{'identifier':'com.pa.domdom.laser_unit_effects'}]
api_mods = json.loads(urlopen(url).read().decode('UTF-8'))

if not os.path.exists(temp_issue_dir): os.makedirs(temp_issue_dir)
for i, mod in enumerate(api_mods):
    mod_id = mod['identifier']

    mod_path = os.path.join(temp_mod_dir, mod_id)
    mod_issue_path = os.path.join(temp_issue_dir, mod_id + '.txt')

    from mod.checker import check_mod

    mod_report = check_mod(mod_path)

    print(i, '/', len(api_mods), '-', mod_id, ' - [' + str(mod_report.getIssueCount()) + ']')

    with open(mod_issue_path, 'w') as mod_issue_file:
        if mod_report.getIssueCount() > 0:
            print(mod_report.printReport(), file=mod_issue_file)






