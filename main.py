from dotenv import load_dotenv
import os
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


load_dotenv()

SHEETY_STEM = 'https://api.sheety.co/d9f02081f9a01191e5a5c45c80a67854/flightDeals (pythonProject)/prices'
SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')
data_manager = DataManager(SHEETY_STEM, SHEETY_TOKEN)

AMADEUS_API_KEY = os.environ.get('AMADEUS_API_KEY')
AMADEUS_API_SECRET = os.environ.get('AMADEUS_API_SECRET')
flight_search = FlightSearch(AMADEUS_API_KEY, AMADEUS_API_SECRET)

EMAIL = os.environ.get('EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
notification_manager = NotificationManager(EMAIL, EMAIL_PASSWORD)

### POPULATE IATA CODES
# Pull all data from Google Sheet
sheet_data = data_manager.get_data()

if sheet_data['prices'][0]['iataCode'] == '':
    # Iterate through cities and record country codes in Google Sheet
    for row in sheet_data['prices']:
        # Get IATA code for this city
        city_code = flight_search.get_iata_code(row['city'])

        # Update row in Google Sheet with IATA code
        json = {
            'price': {
                'city': row['city'],
                'iataCode': city_code,
                'lowestPrice': row['lowestPrice']
            }
        }

        data_manager.update_row(json, row['id'])

sheet_data = data_manager.get_data()
for i in range(len(sheet_data['prices'])):
    code = sheet_data['prices'][i]['iataCode']
    price = sheet_data['prices'][i]['lowestPrice']
    data = flight_search.get_flights_next_6_mo(code)
    cheapest_flight = find_cheapest_flight(data)

    print(cheapest_flight.price, price)
    if cheapest_flight.price != 'N/A' and cheapest_flight.price <= price:
        print('hello')
        notification_manager.send_email(cheapest_flight)