import json
import os
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("Hugging Face token not found in .env file")

# log in to hf
login(token=hf_token)  
# Path to the single transformed JSON file
input_file = "FormattedData_Output/sharegpt_allJsonCompiledRaw.json"  # Path to your transformed JSON file

# Read the transformed JSON data
with open(input_file, "r") as f:
    all_data = json.load(f)  # Load the data from the file

# Split the dataset into train, validation, and test sets (80%, 10%, 10%)
train_data, temp_data = train_test_split(all_data, test_size=0.2, random_state=42)
val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

# Convert the data into Hugging Face Dataset format (each conversation entry as an example)
train_dataset = Dataset.from_dict({"conversations": [entry["conversations"] for entry in train_data]})
val_dataset = Dataset.from_dict({"conversations": [entry["conversations"] for entry in val_data]})
test_dataset = Dataset.from_dict({"conversations": [entry["conversations"] for entry in test_data]})

# Create a DatasetDict
dataset = DatasetDict({
    "train": train_dataset,
    "validation": val_dataset,
    "test": test_dataset
})

# Replace with your Hugging Face dataset repo name
dataset_name = "manashb97/LightAutomationLLM"  # Change this with your dataset name

# Push the dataset to Hugging Face
dataset.push_to_hub(dataset_name)

print(f"Dataset pushed to Hugging Face: {dataset_name}")
