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
        try:
            response = requests.get(url=self.sheety_prices_endpoint)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            data = response.json()
            
            # Attempt to access the key
            self.destination_data = data['prices']
            return self.destination_data
        except requests.exceptions.RequestException as e:
            print(f"HTTP error occurred: {e}")
        except KeyError as e:
            print(f"KeyError occurred: {e}. The key 'prices' is missing in the response JSON.")
        except ValueError as e:
            print(f"ValueError: Failed to parse JSON. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
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
        try:
            response = requests.get(url=self.sheety_users_endpoint)
            response.raise_for_status()
            self.customer_data = response.json()['users']
            return self.customer_data
        except requests.exceptions.RequestException as e:
                print(f"HTTP error occurred: {e}")
        except KeyError as e:
            print(f"KeyError occurred: {e}. The key 'users' is missing in the response JSON.")
        except ValueError as e:
            print(f"ValueError: Failed to parse JSON. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")