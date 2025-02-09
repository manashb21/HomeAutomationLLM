import os
import json

# Define input and output directories
input_dir = "../data/splittedData_JSON_YAML"
output_dir = "../data/splitToUnslothFormat"
os.makedirs(output_dir, exist_ok=True)

# List of files to process
file_names = ["train_yaml_string.json", "val_yaml_string.json", "test_yaml_string.json"]

# Function to transform dataset
def transform_to_unsloth_format(data):
    return [
        [
            {"from": "human", "value": entry["command"]},
            {"from": "gpt", "value": entry["output"]}
        ]
        for entry in data
    ]

# Process each file
for file_name in file_names:
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(output_dir, file_name)
    
    # Read the input JSON file
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Transform the dataset
    transformed_data = transform_to_unsloth_format(data)
    
    # Save the transformed dataset
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transformed_data, f, indent=4, ensure_ascii=False)
    
    print(f"Processed and saved: {output_path}")

print("All files have been successfully converted and saved in the Unsloth format.")
