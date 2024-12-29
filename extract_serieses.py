import requests
import csv

# API URL and initial setup
API_URL = "https://api4.thetvdb.com/v4/series"
OUTPUT_CSV = "data/series_data_v2.csv"
TOKEN = 'TOKEN'
HEADERS = {"Authorization": TOKEN}  
KEYS = ['name',	'slug',	'image', 'firstAired', 'lastAired', 'lastUpdated', 'overview',	'year']

def extract_string_fields(item):
    """Extract string fields and status name from the API response."""
    extracted = {}
    for key, value in item.items():
        if key in KEYS:
            extracted[key] = value
    return extracted

def fetch_and_save_data():
    """Fetch data from the API, extract relevant fields, and save to a CSV file."""
    current_page = 1
    data_list = []

    while True:
        print('current_page: ', current_page)
        response = requests.get(API_URL, headers=HEADERS, params={"page": current_page})
        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}: {response.status_code}")
            break

        response_json = response.json()
        data = response_json.get("data", [])
        for item in data:
            extracted = extract_string_fields(item)
            data_list.append(extracted)

        # Check for next page
        links = response_json.get("links", {})
        if not links.get("next"):
            break

        current_page += 1

    # Save to CSV
    if data_list:
        with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
            writer.writeheader()
            writer.writerows(data_list)
        print(f"Data successfully saved to {OUTPUT_CSV}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    fetch_and_save_data()
