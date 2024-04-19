import requests


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, url_stem, token) -> None:
        self.url_stem = url_stem
        self.token = token


    def get_data(self) -> dict:
        response = requests.get(url=self.url_stem)
        response.raise_for_status()
        return(response.json())


    def update_row(self, json, id) -> None:
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.put(url=f'{self.url_stem}/{id}', json=json, headers=headers)
        response.raise_for_status()
