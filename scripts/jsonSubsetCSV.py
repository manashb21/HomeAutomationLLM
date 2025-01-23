
## this script produces a subset of the restructure final data into a csv. The csv is to be use for Krippendorff's alpha score calculation.
import json
import pandas as pd

# Load JSON file
with open('../data/restructured_dataset_FINAL.json', 'r') as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.json_normalize(data)

# Split dataset by intent
single_room = df[df['intent'] == 'single_room_control']
multi_room = df[df['intent'] == 'multi_room_control']

# Randomly select 100 rows for each intent
single_room_sample = single_room.sample(n=100, random_state=42)
multi_room_sample = multi_room.sample(n=100, random_state=42)

# Combine the samples
alpha_subset = pd.concat([single_room_sample, multi_room_sample])

# Save to CSV for annotators
alpha_subset.to_csv('../csv/krippendorff_alpha_200.csv', index=False)
