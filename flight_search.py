import requests


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self, url_stem, token) -> None:
        self.url_stem = url_stem
        self.token = token


    def get_iata_code(self, city) -> str:
        headers = {
            'accept': 'application/json',
            'apikey': self.token
        }
        params = {
            'term': city,
            'location_types': 'city'
        }

        response = requests.get(url=f'{flight_search_stem}query', params=params, headers=headers)
        response.raise_for_status()
        city_code = response.json()['locations'][0]['code']

        return(city_code)


    def get_flights():
        pass