import json
import os

# System prompt for the assistant
system_prompt = "You are an assistant that controls smart lights by responding with precise JSON actions."

def transform_to_sharegpt(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    sharegpt_data = []
    for entry in data:
        # Extract fields
        command = entry.pop("command")  # Remove the 'command' field
        gpt_response = json.dumps(entry)  # Convert the rest to JSON string

        # Create ShareGPT format
        sharegpt_data.append({
            "conversations": [
                {"from": "system", "value": system_prompt},
                {"from": "human", "value": command},
                {"from": "gpt", "value": gpt_response}
            ]
        })

    return sharegpt_data

file_name = "allJsonCompiledRaw.json"
input_path = file_name
output_dir = "FormattedData_Output"
output_path = os.path.join(output_dir, f"sharegpt_{file_name}")

transformed_data = transform_to_sharegpt(input_path)

# Save transformed data
with open(output_path, "w") as f:
    json.dump(transformed_data, f, indent=4)

print(f"Transformed file saved: {output_path}")
