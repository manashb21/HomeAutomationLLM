import json
import os

# Define input and output directories
input_dir = "../data/splitToUnslothFormat"  
output_dir = "../data/splitToUnslothTomeFormat"
os.makedirs(output_dir, exist_ok=True)

# List of dataset splits to process
splits = ["train_yaml_string.json", "val_yaml_string.json", "test_yaml_string.json"]

# Function to convert dataset format
def convert_to_finetome_format(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # Wrap all conversations inside a single "conversations" key
    converted_dataset = {"conversations": dataset}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(converted_dataset, f, indent=4, ensure_ascii=False)

    print(f"✅ Converted: {input_path} → {output_path}")

# Process all dataset splits
for split in splits:
    input_path = os.path.join(input_dir, split)
    output_path = os.path.join(output_dir, split)
    convert_to_finetome_format(input_path, output_path)

print("🎯 All datasets (train, val, test) now match FineTome-100k format!")
