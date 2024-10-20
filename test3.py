import json
import csv

# File paths for offering.txt and review.txt (update paths as needed)
offering_file = 'offering.json'
review_file = 'review.json'
output_csv = 'hotel1.csv'

# Function to load JSON data from a file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]

# Load offering and review data
offerings = load_json_data(offering_file)
reviews = load_json_data(review_file)

# Create a mapping of hotel id to city (locality) from the offering file
hotel_city_map = {offer['id']: offer['address']['locality'] for offer in offerings}

# Create and write data to CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['city', 'location_rating']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Iterate through the reviews and write to CSV
    for review in reviews:
        hotel_id = review['offering_id']
        city = hotel_city_map.get(hotel_id, 'Unknown')
        location_rating = review['ratings'].get('location', 'N/A')
        
        writer.writerow({
            'city': city,
            'location_rating': location_rating
        })

print(f"CSV file '{output_csv}' created successfully.")
