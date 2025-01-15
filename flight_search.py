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
    
    def find_flights(self,origin,destination,departureDate,return_date,maxPrice):
        header = {
            "Authorization": f"Bearer {self._token}",
        }
        body = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departureDate.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "INR",
            "maxPrice": maxPrice,
            "max": 10
        }
        response = requests.get(url=FLIGHT_ENDPOINT,headers=header,params=body)
        data = response.json()["data"]
        return data