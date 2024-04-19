from dotenv import load_dotenv
import os
import requests
from data_manager import DataManager
from flight_search import FlightSearch


load_dotenv()

SHEETY_STEM = 'https://api.sheety.co/d9f02081f9a01191e5a5c45c80a67854/flightDeals (pythonProject)/prices'
SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')
data_manager = DataManager(SHEETY_STEM, SHEETY_TOKEN)

FLIGHT_SEARCH_STEM = 'https://api.tequila.kiwi.com/locations'
FLIGHT_SEARCH_TOKEN = os.environ.get('FLIGHT_SEARCH_API_KEY')
flight_search = FlightSearch(FLIGHT_SEARCH_STEM, FLIGHT_SEARCH_TOKEN)

### POPULATE IATA CODES
# Pull all data from Google Sheet
sheet_data = data_manager.get_data()

if sheet_data['prices'][0]['iataCode'] == '':
    # Iterate through cities and record country codes in Google Sheet
    for row in sheet_data['prices']:
        # Get IATA code for this city
        flight_search.get_iata_code(row['city'])

        # Update row in Google Sheet with IATA code
        json = {
            'price': {
                'city': row['city'],
                'iataCode': city_code,
                'lowestPrice': row['lowestPrice']
            }
        }

        data_manager.update_row(json, row['id'])







url = 'https://api.tequila.kiwi.com/locations/query'
# response = requests.get(url=url, params=params, headers=headers)
# response.raise_for_status()
# print(response.text)