import os
import json

# Define input and output folders
input_folder = "../data/splittedData"
output_folder = "../data/splittedData_Correct_UnslothTomeFormat"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to process and convert data
def convert_data_format(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    conversations = []
    for entry in data:
        if "command" not in entry or "actions" not in entry:
            print(f"Skipping malformed entry: {entry}")
            continue

        human_message = {"from": "human", "value": entry["command"]}

        # Construct GPT response
        gpt_response_values = []
        for action in entry["actions"]:
            room = action.get("room", "unknown_room")
            action_type = action.get("action", "unknown_action")

            if action_type == "change_color" and "color" in action:
                gpt_response_values.append(f"{room}: {action_type} ({action['color']})")
            elif action_type == "adjust_brightness" and "brightness" in action:
                gpt_response_values.append(f"{room}: {action_type} ({action['brightness']})")  # No %
            else:
                gpt_response_values.append(f"{room}: {action_type}")

        gpt_message = {"from": "gpt", "value": ", ".join(gpt_response_values)}

        # Append as a conversation pair
        conversations.append([human_message, gpt_message])

    return {"conversations": conversations}

# Process each JSON file in the input folder
for filename in ["train.json", "test.json", "val.json"]:
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    if os.path.exists(input_path):
        converted_data = convert_data_format(input_path)
        if converted_data:
            with open(output_path, "w", encoding="utf-8") as output_file:
                json.dump(converted_data, output_file, indent=2, ensure_ascii=False)
            print(f"Converted and saved: {output_path}")
    else:
        print(f"Skipping {filename} (file not found).")
