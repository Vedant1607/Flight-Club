from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
from datetime import datetime,timedelta
import time
import sys

# Initialize the necessary classes for data management, flight search, and notifications
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY = "DEL"

# Fetch data from the Sheety spreadsheet
sheet_data = data_manager.get_sheet_data()

if not sheet_data:
    print("Error: Failed to fetch sheet data. Stopping further execution.")
    sys.exit(1)  # Exit the program with an error status

# Retrieve and update the IATA Codes for all cities in the sheet, and update the sheet data
for row in sheet_data:
    row['iataCode'] = flight_search.get_destination_code(row['city'])
    time.sleep(2) # Add a delay to avoid hitting API limits
print(f"Sheet Data:\n{sheet_data}")

# Update the destination data in the spreadsheet with the newly fetched IATA codes
data_manager.destination_data = sheet_data
data_manager.update_sheet_data()

# Retrieve customer email list from the Sheety API for notifications
customer_data = data_manager.get_customer_emails()
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]

# gettng date
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=(6*30))

# Loop through each destination in the sheet and search for both direct and indirect flights
for destination in sheet_data:
    # Search for direct flights
    print(f"Getting direct flights for {destination['city']}...")
    flights = flight_search.find_flights(
        origin=ORIGIN_CITY,
        destination=destination["iataCode"],
        departureDate=tomorrow,
        return_date=six_months_from_now,
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}:{cheapest_flight.price}")
    time.sleep(2) # Add a delay to avoid hitting API limits
    
    # Search for Indirect Flights
    if cheapest_flight.price == "N/A":
        stopover_flights = flight_search.find_flights(
            origin=ORIGIN_CITY,
            destination=destination["iataCode"],
            departureDate=tomorrow,
            return_date=six_months_from_now,
            is_direct=False
        )
    cheapest_flight = find_cheapest_flight(stopover_flights)
    print(f"Cheapest indirect flight price is:{cheapest_flight.price}")
    
    # If the cheapest flight is cheaper than the current lowest price in the sheet, send a notification
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination['lowestPrice']:
        if cheapest_flight.stops == 0: # Direct Flight
            message = f"Lower price alert! Only ₹{cheapest_flight.price} to fly "\
                    f"from {cheapest_flight.origin_airport_code} to {cheapest_flight.destination_airport_code}, "\
                    f"on {cheapest_flight.departure_date} until {cheapest_flight.return_date}"
        else: # Indirect Flight
            message = f"Lower price alert! Only ₹{cheapest_flight.price} to fly "\
                    f"from {cheapest_flight.origin_airport_code} to {cheapest_flight.destination_airport_code}, "\
                    f"with {cheapest_flight.stops} stop(s) departing on {cheapest_flight.departure_date} and returning on {cheapest_flight.return_date}"
        
        print(f"Check your email. Lower price flight found to {destination['city']}")
        
        # Send notifications via SMS, WhatsApp, and email
        notification_manager.send_sms(message_body=message)
        notification_manager.send_wp_message(message_body=message)
        notification_manager.send_email(email_list=customer_email_list,email_body=message)