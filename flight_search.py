import requests
import datetime as dt


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self, url_stem, token) -> None:
        self.url_stem = url_stem
        self.token = token
        self.headers = {
            'accept': 'application/json',
            'apikey': self.token
        }


    def get_iata_code(self, city) -> str:
        endpoint = '/query'
        params = {
            'term': city,
            'location_types': 'city'
        }

        response = requests.get(url=f'{self.url_stem}{endpoint}', params=params, headers=self.headers)
        response.raise_for_status()
        city_code = response.json()['locations'][0]['code']

        return(city_code)


    def get_flights_next_6_mo(self, city):
        endpoint = '/search'
        params = {
            'fly_from': 'WAS',
            'fly_to': city,
            'date_from': dt.datetime.today().strftime('%m/%d/%Y'),
            'date_to': dt.datetime.today().strftime('%m/%d/%Y') + dt.timedelta(days=6*30),
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'adults': '2',
            'curr': 'USD'
        }

        response = requests.get(url=f'{self.url_stem}{endpoint}', headers=self.headers, params=params)
        response.raise_for_status()
