from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os
import os.path 

from mod.validate import validate_mod_files

from urllib import request
import json

temp_dir = './tmp-mods'
url = "https://pamm-mereth.rhcloud.com/api/mod"

if not os.path.exists(temp_dir): os.makedirs(temp_dir)

api_mods = json.loads(urlopen(url).read().decode('UTF-8'))

# for i, mod in enumerate(api_mods):
#     print (i, '/', len(api_mods))

#     mod_id = mod['identifier']
#     mod_url = mod['url']

#     mod_path = os.path.join(temp_dir, mod_id)

#     #############
#     try:
#         if not os.path.exists(mod_path):
#             print ('Downloading', mod_id, ':', mod_url)
#             with urlopen(mod_url) as zipresp:
#                 with ZipFile(BytesIO(zipresp.read())) as zfile:
#                     zfile.extractall(mod_path)
#         else:
#             print ('Skipping download of', mod_id, ':', mod_url)
#     except:
#         print('Failed to download', mod_id)
#         continue

import glob
issues = {}

print('================== VALIDATING MODS')
for i, mod in enumerate(api_mods):
    mod_id = mod['identifier']
    mod_url = mod['url']

    print (i, '/', len(api_mods), '-', mod_id)

    mod_path = os.path.join(temp_dir, mod_id)
    glob_result = glob.glob(os.path.join(mod_path, '**','modinfo.json'), recursive=True)

    if len(glob_result) == 0:
        print('+++ Could not find modinfo for', mod_id)
        continue

    modinfo_path = glob_result[0]
    mod_path = os.path.dirname(modinfo_path)

    issues[mod_id] = validate_mod_files(mod_path)
print('------------------ DONE')


print('================== ISSUE SUMMARY')
for mod_id, file_map in issues.items():
    if len(file_map) > 0:
        
        print('=====', mod_id , '=====[', len(file_map), ']')
        
        for file, refs in file_map.items():
            print (file, 'not found, referenced by:')
            for ref in refs:
                print('    ', ref)

            