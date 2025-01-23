## This script aims to Simplify Intents by:
# Consolidating high-level intents to single_room_control and multi_room_control.
# Moving action-specific intents like adjust_brightness or change_color into the action field.

# allJsonCompiledRaw.json file is the original dataset without changes
# the output of this script will be a dataset with the above stated changes.

import json
import os 

# directory
root_path = "../data"
filename = "allJsonCompiledRaw_FINAL.json" ## change filename here
file_path = os.path.join(root_path, filename)

# loading the json file
with open(file_path, 'r') as file:
    original_data = json.load(file)

# Function to simplify intents and restructure data
def restructure_dataset(data):
    restructured_data = []
    for entry in data:
        new_entry = {
            "command": entry["command"],
            "intent": "multi_room_control" if len(entry["rooms"]) > 1 else "single_room_control",
            "rooms": entry["rooms"],
            "actions": entry["actions"]
        }
        restructured_data.append(new_entry)
    return restructured_data

# Restructure the dataset
restructured_data = restructure_dataset(original_data)

# Save the restructured data to a new file
output_filename = "restructured_dataset_FINAL.json" ## change output filename here

output_path = os.path.join(root_path, output_filename)
with open(output_path, 'w') as output_file:
    json.dump(restructured_data, output_file, indent=4)


