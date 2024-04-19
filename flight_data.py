class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, from_city, from_city_code, to_city, to_city_code, from_date, to_date) -> None:
        self.price = price
        self.from_city = from_city
        self.from_city_code = from_city_code
        self.to_city = to_city
        self.to_city_code = to_city_code
        self.from_date = from_date
        self.to_date = to_date
    pass