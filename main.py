#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from dotenv import load_dotenv
import os
import requests

load_dotenv()

FLIGHT_SEARCH_API_KEY = os.environ.get('FLIGHT_SEARCH_API_KEY')
SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')

sheety_stem = 'https://api.sheety.co/d9f02081f9a01191e5a5c45c80a67854/flightDeals (pythonProject)/prices'
flight_search_stem = 'https://api.tequila.kiwi.com/locations/'

### POPULATE IATA CODES
# Pull all data from Google Sheet
response = requests.get(url=sheety_stem)
response.raise_for_status()
cities_data = response.json()

# Iterate through cities and record country codes in Google Sheet
for row in cities_data['prices']:
    # Get IATA code for this city
    headers = {
        'accept': 'application/json',
        'apikey': FLIGHT_SEARCH_API_KEY
    }
    params = {
        'term': row['city'],
        'location_types': 'city'
    }

    response = requests.get(url=f'{flight_search_stem}query', params=params, headers=headers)
    response.raise_for_status()
    city_code = response.json()['locations'][0]['code']

    # Update row in Google Sheet with IATA code
    headers = {
        'Authorization': SHEETY_TOKEN,
        'Content-Type': 'application/json'
    }
    body = {
        'price': {
            'city': row['city'],
            'iataCode': city_code,
            'lowestPrice': row['lowestPrice']
        }
    }

    response = requests.put(url=f'{sheety_stem}/{row['id']}', json=body, headers=headers)
    response.raise_for_status()





# params = {
#     'fly_from':'',
#     'fly_to': 'San Diego',
#     'date_from': '07/06/2024',
#     'date_to': '10/06/2024',
#     'adults': '2'
# }
params = {
    'term': 'San Diego',
    'location_types': 'city'
}

url = 'https://api.tequila.kiwi.com/locations/query'
# response = requests.get(url=url, params=params, headers=headers)
# response.raise_for_status()
# print(response.text)