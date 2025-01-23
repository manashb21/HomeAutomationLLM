## script for compiling all the separate chunks of json into one single json file.

import os
import json

root = '../data/temp' # IMP: change the root according to which folder has the json chunks 
all_files = os.listdir(root)

# to combine all the json arrays to one file for further formatting according to chat template
def extender():
    combined_file = []
    for file in all_files:
        full_path = root+"/"+file
        with open(full_path, 'r') as f:
            combined_file.extend(json.load(f))
    print(f"Total json data in file: {len(combined_file)}")
    return combined_file

output = extender()

filename = "allJsonCompiledRaw_FINAL.json" #IMP: change output filename here!
save_path = root + "/" + filename

with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)