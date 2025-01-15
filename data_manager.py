import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

class DataManager:
    def __init__(self):
        load_dotenv()
        self._user = os.getenv('SHEETY_USERNAME')
        self._password = os.getenv('SHEET_PASSWORD')
        self._authorization = HTTPBasicAuth(self._user,self._password)
        self.sheety_prices_endpoint = os.getenv('SHEETY_PRICES_ENDPOINT')
        self.sheety_users_endpoint = os.getenv('SHEETY_USERS_ENDPOINT')
        self.destination_data = {}
        self.customer_data = {}
    
    # Function to retrieve sheet data (price information)
    def get_sheet_data(self):
        response = requests.get(url=self.sheety_prices_endpoint)
        self.destination_data = response.json()['prices']
        return self.destination_data
    
    # Function to update sheet data (adding IATA code to the price sheet)
    def update_sheet_data(self):
        for city in self.destination_data:
            new_data = {
                "price":{
                    "iataCode":city['iataCode']
                }
            }
            response = requests.put(
                url=f"{self.sheety_prices_endpoint}/{city['id']}",
                json=new_data
            )
            response.raise_for_status()
            print(response.text)
    
    # Function to get customer email list from Sheety
    def get_customer_emails(self):
        response = requests.get(url=self.sheety_users_endpoint)
        self.customer_data = response.json()['users']
        return self.customer_data