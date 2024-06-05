import argparse
import json

# Initialize a set to store unique ids
unique_ids = set()

# Function to check if a string is a valid JSON
def is_json(my_json):
    try:
        json.loads(my_json)
        return True
    except ValueError:
        return False

# Function to process each line of the file
def process_line(line):
    if is_json(line):
        json_object = json.loads(line)
        if "m" in json_object:
            messages = json_object["m"]
            for message in messages:
                if "id" in message:
                    if message["id"] not in unique_ids:
                        unique_ids.add(message["id"])
                        # Save the unique messages to a list
                        unique_messages.append(message)

# Argument parser setup
parser = argparse.ArgumentParser(description="Process a JSON file and extract unique messages by id")
parser.add_argument("file", type=str, help="Input JSON text file")

# Parse command-line arguments
args = parser.parse_args()

# List to store unique messages
unique_messages = []

# Open and read the text file line by line
with open(args.file, 'r') as file:
    for line in file:
        process_line(line)

# Output the unique messages to a JSON file with the same name as the input file
output_file = args.file.replace(".txt", ".json")
with open(output_file, 'w') as outfile:
    json.dump(unique_messages, outfile, indent=4)

print(f"Unique messages saved to {output_file}")