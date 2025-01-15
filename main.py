from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from datetime import datetime,timedelta
import time

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()
notification_manager = NotificationManager()

sheet_data = data_manager.get_sheet_data()

ORIGIN_CITY = "DEL"

# Getting the IATA Codes and updating in the google spreadsheet
for row in sheet_data:
    row['iataCode'] = flight_search.get_destination_code(row['city'])
    time.sleep(2)
print(f"Sheet Data:\n{sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_sheet_data()

# gettng date
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=(6*30))

# Finding flights
for destination in sheet_data:
    flights = flight_search.find_flights(
        origin=ORIGIN_CITY,
        destination=destination["iataCode"],
        departureDate=tomorrow,
        return_date=six_months_from_now,
        maxPrice=destination["lowestPrice"],
    )
    cheapest_flight = flight_data.find_cheapest_flight(flight_offers=flights)
    
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination['lowestPrice']:
        message = f"Lower price alert! Only ₹{cheapest_flight.price} to fly 
        from {cheapest_flight.origin_airport_code} to {cheapest_flight.destination_airport_code},
        on {cheapest_flight.departure_date} until {cheapest_flight.return_date}"
        
        notification_manager.send_sms(message_body=message)
        notification_manager.send_wp_message(message_body=message)