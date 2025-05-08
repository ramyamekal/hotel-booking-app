import pandas
from abc import ABC,abstractmethod

df = pandas.read_csv("hotels.csv",dtype={"id":str})
df_cards = pandas.read_csv("cards.csv",dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv",dtype=str)

class Hotel:
    def __init__(self,hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id,"name"].squeeze()

    def book(self):
        """ Book a hotel by changing its availablity to no"""
        df.loc[df["id"] == self.hotel_id,"available"] = "no"
        df.to_csv("hotels.csv",index=False)

    def available(self):
        """ checks if hotel is available """
        availablliy = df.loc[df["id"] == self.hotel_id,"available"].squeeze()
        print(availablliy)
        if availablliy == "yes":
            return True
        else:
            return False

class Ticket(ABC):
    @abstractmethod
    def generate(self):
        pass

class DigitalTicket(Ticket):
    def generate(self):
        return "Hello, this is your digital ticket"
    def download(self):
        pass

class ReservationTicket:
    def __init__(self,customer_name,hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f""" Thank you for your Reservation! Here are your Booking Data: 
        Name : {self.the_customer_name}
        Hotel Name:{self.hotel.name}"""
        return content

    # Properties
    @property
    def the_customer_name(self):
        name = self.customer_name.strip()
        name = name.title()
        return name

    # Static Methods
    @staticmethod
    def convert(amount):
        return amount * 1.2

    # Magic Methods
    def __eq__(self,other):
        if self.hotel_id == other.hotel_id:
            return True
        else:
            return False
    #Magic Methods example 2
    def __add__(self,other):
        total = self.price + other.price
        return total

class Creditcard:
    def __init__(self,number):
        self.number = number

    def validate(self,expiration,holder,cvc):
        card_data = {"number":self.number,"expiration":expiration,
                     "holder":holder,"cvc":cvc}
        if card_data in df_cards:
            return True
        else:
            return False

class SecureCreditCard(Creditcard):
    def authenticate(self,given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number,"password"].squeeze()
        if password == given_password:
            return True
        else:
            return False

class Spa(ReservationTicket):
    def bookspa(self,spastatus):
        if spastatus == "yes":
            status = (f""" Thank you for your SPA Reservation! Here are your Booking Data: 
            Name : {self.customer_name}
            Hotel Name:{self.hotel.name}""")
            return status


print(df)
hotel_ID = input("Enter hotel id:")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26",holder="JOHN SMITH",cvc="123"):
        if credit_card.authenticate(given_password ="mypass"):
            hotel.book()
            name = input("Enter your name:")
            reservation_ticket = ReservationTicket(customer_name = name,hotel_object=hotel)
            print(reservation_ticket.the_customer_name)
            print(reservation_ticket.convert(10))
            print(reservation_ticket.generate())
            spa = input("Do you want to book a spa package? (yes/no): ")
            spa_reservation = Spa(customer_name=name, hotel_object=hotel)
            if spa.lower() == "yes":
                print(spa_reservation.bookspa(spastatus=spa))
        else:
            print("Credit card authentication failed")
    else:
        print("There is a problem with your payment")
else:
    print("Hotel is not free")