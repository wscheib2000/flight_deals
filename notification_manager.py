import smtplib
from flight_data import FlightData


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, email, password):
        self.email = email
        self.password = password

    
    def send_email(self, cheapest_flight: FlightData):
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls() # Makes connection secure

            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=self.email,
                msg=f'Subject:Cheap Flights!\n\n\nLow price alert! Only {cheapest_flight.price} to fly from {cheapest_flight.from_city} to {cheapest_flight.to_city} on {cheapest_flight.from_date} and stay until {cheapest_flight.to_date}.'
            )