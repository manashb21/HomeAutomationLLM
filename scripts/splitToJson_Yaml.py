import json
import yaml
import os

def convert_to_yaml_like_string(entry):
    """
    Convert structured JSON output to a YAML-like string inside JSON.
    """
    output = " ".join(
        f"{action['room']}: brightness={action.get('brightness', 1.0)}" if action["action"] == "adjust_brightness"
        else f"{action['room']}: {action['action']}"
        for action in entry["actions"]
    )

    return {"command": entry["command"], "output": output}

root_dir_input = "../data/splittedData"
root_dir_output = "../data/splittedData_JSON_YAML"

# Convert datasets
for split in ["train", "val", "test"]:
    # Load JSON file
    ip_filename = split + ".json" 
    ip_full_filename = os.path.join(root_dir_input, ip_filename)
    with open(ip_full_filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
     # Convert format
    structured_data = [convert_to_yaml_like_string(entry) for entry in data]
    
    # Save as YAML file
    op_filename = split + "_yaml_string.json"
    op_full_filename = os.path.join(root_dir_output, op_filename)
    with open(op_full_filename, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4, ensure_ascii=False)


print("✅ Datasets converted successfully to YAML format!")
