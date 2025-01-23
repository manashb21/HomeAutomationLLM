import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict
import random

load_dotenv()
# Configure OpenAI API key
openai = OpenAI()
api_key = os.getenv("OPENAI_API_KEY")
           
system = '''You are an expert assistant in creating diverse home automation commands for controlling lights. Generate realistic, natural, and code-mixed (Nepali-English or English) 
            text commands for a home automation system. The commands should vary in tone, intent, and style, with a mix of formal and informal expressions. 
            Include controls for turning lights on/off, adjusting brightness, multi-room operations, and ambiguous or vague instructions. 
            Ensure the dataset contains polite requests, conversational tones, and scenarios involving multiple intents.'''

user = '''Generate 5 examples of home automation commands for controlling lights in a house. Each command should be written in code-mixed Nepali-English or English and follow the structure below. 
        Ensure diversity in intent, tone, and room settings.
        Example Format:
        {
            "id": 1,
            "command": "Bedroom lights off garera kitchen lights dim garnu.",
            "intent": "multi_room_control",
            "rooms": ["bedroom", "kitchen"],
            "actions": [
              {"room": "bedroom", "action": "turn_off"},
              {"room": "kitchen", "action": "adjust_brightness", "brightness": "low"}
            ]
        }
         
        Generate Commands for These Scenarios:
            1. Turn lights on/off in specific rooms.
            2. Adjust brightness in percentage or qualitative terms (e.g., dim, brighten).
            3. Control lights in multiple rooms at once.
            4. Combine multiple intents, such as turning off lights in one room and dimming lights in another.
        
        Example Commands:
        1. 'Bedroom lights off garera kitchen lights dim garna sakinchha?'
        2. 'Living room lights thap bright banaunus.'
        3. 'Can you turn the study room light to warm white?'
        4. 'Sabai room ka lights dim garidinus.'
        5. 'Turn off living room lights and change bedroom lights to red.'
        
        Write the output as JSON objects following the example format above.
'''


def builder(system, user):
    return [{"role":"system", "content":system},
            {"role":"user", "content":user}
           ]       

# combining all the steps
def generate_dataset(system, user):
    try:
        response = openai.chat.completions.create(model = "gpt-4o-mini",
                                                  messages = builder(system, user),
                                                  # temperature = 0.8, 
                                                  # max_tokens = 2000
                                                  )
        # dataset = json.loads(response.choices[0].message.content)
        dataset = (response.choices[0].message.content)
        print(dataset)
        return dataset
    except Exception as e:
        print(f"Error generating dataset: {str(e)}")
        return []

# function to save the dataset as json      
def save_dataset(dataset: List[Dict], filename: str):
    """Save the generated dataset to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    dataset = generate_dataset(system, user)
    
    if dataset:
        # Save the dataset
        save_dataset(dataset, "light_automation_dataset.json")
        print(f"Successfully generated and saved {len(dataset)} samples to light_automation_dataset.json")
    else:
        print("Failed to generate dataset")

