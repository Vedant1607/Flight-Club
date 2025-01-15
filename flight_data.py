class FlightData:
    def __init__(self,price,origin_airport_code,destination_airport_code,departure_date,return_date,stops):
        self.price = price
        self.origin_airport_code = origin_airport_code
        self.destination_airport_code = destination_airport_code
        self.departure_date = departure_date
        self.return_date = return_date
        self.stops = stops

# Function to find the cheapest flight from a list of flight offers 
def find_cheapest_flight(data):
    if not data:
        print("No flight data")
        return FlightData("N/A","N/A","N/A","N/A","N/A","N/A")
    
    # Initializing first flight for comparison
    first_flight = data[0]
    lowest_price = float(first_flight['price']['grandTotal'])
    nr_stops = len(first_flight["itineraries"][0]["segments"])-1
    departure_airport = first_flight['itineraries'][0]['segments'][0]['departure']['iataCode']
    arrival_airport = first_flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
    departure_date = first_flight['itineraries'][0]['segments'][0]['departure']['at'].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            
    for flight in data:
        price = float(flight['price']['grandTotal'])
        if price < lowest_price:
            lowest_price = float(flight['price']['grandTotal'])
            departure_airport = flight['itineraries'][0]['segments'][0]['departure']['iataCode']
            arrival_airport = flight['itineraries'][0]['segments'][nr_stops]['arrival']['iataCode']
            departure_date = flight['itineraries'][0]['segments'][0]['departure']['at'].split("T")[0]
            return_date = flight['itineraries'][1]['segments'][0]['arrival']['at'].split("T")[0]
            # Return the cheapest flight as a FlightData object
            cheapest_flight = FlightData(price=lowest_price,origin_airport_code=departure_airport,destination_airport_code=arrival_airport,departure_date=departure_date,return_date=return_date,stops=nr_stops)

    return cheapest_flight   