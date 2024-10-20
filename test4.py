import json
import csv

# Specify the input JSON file and output CSV file
input_json_file = 'hotel.json'  # Replace with your JSON file path
output_csv_file = 'output.csv'    # The name of the output CSV file

# Function to convert JSON to CSV
def json_to_csv(json_file, csv_file):
    # Load JSON data from the file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Open a CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        
        # Write the header (column names)
        writer.writeheader()
        
        # Write the rows from the JSON data
        for row in data:
            writer.writerow(row)

# Convert JSON to CSV
json_to_csv(input_json_file, output_csv_file)

print(f"Converted '{input_json_file}' to '{output_csv_file}' successfully.")
