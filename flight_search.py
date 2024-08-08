import requests
import datetime as dt
import json

FROM_CITY = 'LON'

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self, api_key, api_secret) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.token = self._get_new_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    
    def _get_new_token(self):
        # Header with content type as per Amadeus documentation
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)

        # New bearer token. Typically expires in 1799 seconds (30min)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']


    def get_iata_code(self, city) -> str:
        params = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS"
        }

        response = requests.get(url=IATA_ENDPOINT, params=params, headers=self.headers)
        response.raise_for_status()

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return code


    def get_flights_next_6_mo(self, city):
        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
            "originLocationCode": FROM_CITY,
            "destinationLocationCode": city,
            "departureDate": dt.datetime.today().strftime('%Y-%m-%d'),
            'returnDate': (dt.datetime.today() + dt.timedelta(days=6*30)).strftime('%Y-%m-%d'),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10"
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )
        response.raise_for_status()
        data = response.json()
        
        return data

