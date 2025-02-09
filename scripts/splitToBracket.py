import json
import os 

def convert_to_bracket_format(entry):
    """
    Convert JSON-style output to bracket-based format (SRC(room:action)).
    """
    action_strs = []
    for action in entry["actions"]:
        room = action["room"]
        action_type = action["action"].replace("_", "")  # Remove underscores for compactness
        
        # Handle brightness adjustment separately
        if action_type == "adjustbrightness":
            formatted_action = f"{room}:brightness={action.get('brightness', 1.0)}"
        else:
            formatted_action = f"{room}:{action_type}"
        
        action_strs.append(formatted_action)

    return f"SRC({', '.join(action_strs)})"

root_dir_input = "../data/splittedData"
root_dir_output = "../data/splittedData_BracketFormat"
# Convert datasets
for split in ["train", "val", "test"]:
    # Load JSON file
    ip_filename = split + ".json" 
    ip_full_filename = os.path.join(root_dir_input, ip_filename)
    with open(ip_full_filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Convert format
    for entry in data:
        entry["bracket_output"] = convert_to_bracket_format(entry)
    
    # Save modified dataset
    op_filename = split + "_bracket.json"
    op_full_filename = os.path.join(root_dir_output, op_filename)
    with open(op_full_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Datasets converted and saved successfully with bracketed format!")
