import json
import csv
import os

def update_csv_from_json(input_json_file, output_csv_file):
    """
    Reads a JSON file and appends its content to a CSV file.
    Writes the header only if the CSV file does not already exist or is empty.

    Args:
        input_json_file (str): Path to the JSON input file.
        output_csv_file (str): Path to the CSV output file.
    """
    # Load JSON data
    with open(input_json_file, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Check if the CSV file exists and has data
    file_exists = os.path.isfile(output_csv_file) and os.path.getsize(output_csv_file) > 0

    # Prepare CSV file for appending or writing
    with open(output_csv_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write header only if the file doesn't already exist
        if not file_exists:
            writer.writerow([
                "Command",            # command
                "Intent",             # Intent from JSON
                "Rooms",              # Comma-separated list of rooms
                "Actions",            # Actions with brightness and color
                "Annotator Feedback"  # Placeholder for annotations for Krippendorff's alpha score calculation
            ])

        nrow = 0
        # Write rows
        for item in json_data:
            command = item["command"]
            intent = item["intent"]
            rooms = ", ".join(item["rooms"])
            actions = "; ".join([
                f"{action['action']} (Brightness: {action.get('brightness', '-')}, Color: {action.get('color', '-')})"
                for action in item["actions"]
            ])
            nrow+=1
            # Write row to CSV
            writer.writerow([command, intent, rooms, actions, ""])

    print(f"CSV file '{output_csv_file}' updated successfully! {nrow} rows added.")


# update_csv_from_json("light_automation_dataset.json", 'annotator_data.csv')