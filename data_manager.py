import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

SHEETY_ENDPOINT = "https://api.sheety.co/33f06c66389284b581728496bf47ad0a/flightDeals/prices"

class DataManager:
    def __init__(self):
        load_dotenv
        self._user = os.getenv('SHEETY_USERNAME')
        self._password = os.getenv('SHEET_PASSWORD')
        self._authorization = HTTPBasicAuth(self._user,self._password)
        self.destination_data = {}
    
    def get_sheet_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        self.destination_data = response.json()['prices']
        return self.destination_data
    
    def update_sheet_data(self):
        for city in self.destination_data:
            new_data = {
                "price":{
                    "iataCode":city['iataCode']
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )
            response.raise_for_status()
            print(response.text)