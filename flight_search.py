import requests
from dotenv import load_dotenv
import os

AMADEUS_AUTH = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
CITY_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

class FlightSearch:
    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv('AMADEUS_API_KEY')
        self._api_secret = os.getenv('AMADEUS_API_SECRET')
        self._token = self._get_new_token()
    
    # Function to request a new OAuth token from Amadeus API
    def _get_new_token(self):
        header = {
            "content-type":"application/x-www-form-urlencoded"
        }
        body = {
            "grant_type":"client_credentials",
            "client_id": self._api_key,
            "client_secret":self._api_secret
        }
        response = requests.post(url=AMADEUS_AUTH,headers=header,data=body)
        token = response.json()['access_token']
        return token
    
    # Function to get the IATA code for a city based on its name
    def get_destination_code(self,city_name):
        header = {
            "Authorization": f"Bearer {self._token}",
        }
        parameters = {
            "keyword":city_name,
            "max":1,
            "include":"AIRPORTS"
        }
        response = requests.get(
            url=CITY_ENDPOINT,
            headers=header,
            params=parameters
        )
        try:
            iata_code = response.json()['data'][0]['iataCode']
        except IndexError:
            print(f"No Airport found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"No Airport found for {city_name}")
            return "Not Found"
        return iata_code
    
     # Function to find available flights between origin and destination
    def find_flights(self,origin,destination,departureDate,return_date,is_direct=True):
        header = {
            "Authorization": f"Bearer {self._token}",
        }
        body = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departureDate.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "INR",
            "max": 10
        }
        response = requests.get(url=FLIGHT_ENDPOINT,headers=header,params=body)
        response.raise_for_status()
        data = response.json()["data"]
        return data