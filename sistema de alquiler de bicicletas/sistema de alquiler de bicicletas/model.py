#model
#sistema de alquiler de bicicletas 
from datetime import date
import math
from datetime import datetime
from datetime import timedelta
class Bike:
    def __init__(self, id : str ,name: str, description: str, price: int, available: bool, model: str):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.available = available
        self.model = model
    def __str__(self):
        return f"{self.id} {self.name} {self.available} {self.price} {self.model}"
class User:
    def __init__(self, name:str, email:str, phone:int):
        self.name = name
        self.email = email
        self.phone = phone
    def __str__(self):
        return f"{self.name} {self.phone}"

class Rental:
    def __init__(self, bike: Bike, user: str, start_date, id_rental: str):
        self.bike = bike
        self.user = user
        self.start_date = start_date # igual a datetime.now()
        self.end_date = 0 
        self.id_rental = id_rental
    # funcionalidad de calcular el precio
    def calculate_price(self):
        tomorrow = self.start_date +timedelta(days=self.end_date)
        hours = (tomorrow.day - self.start_date.day)
        return self.bike.price * math.ceil(hours)
    def __str__(self):
        return f"id de la renta : {self.id_rental} fecha inicial:  {self.start_date} usuario : {self.user}"

class BikeRentalSystem:
    def __init__(self):
        self.bikes = []
        self.users = []
        self.rentals = []
        self.invoices = []
    # agregar bicicletas
    def agregar_bike(self, bike):
        self.bikes.append(bike)
    # agregar usuarios
    def agregar_user(self, user):
        self.users.append(user)
    # rentar bicicletas
    def rentar_bike(self, bike, user, start_date, id_rental):
        rental = Rental(bike, user, start_date, id_rental)
        self.rentals.append(rental)
        bike.available = False
        
    def return_bike(self, rental_id, end_date):
        rental:Rental = self.encontrar_rental(rental_id)
        rental.end_date = end_date
        rental.bike.available = True
        price = rental.calculate_price()
        invoice = Invoice(rental, price)
        self.invoices.append(invoice)
        #sacar rental de la lista
        return invoice
    # buscar bicicletas
    def encontrar_bike(self, bike_id):
        for bike in self.bikes:
            if bike.id == bike_id:
                return bike
        return None
    # funcionalidad de buscar usuarios
    def encontrar_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    # buscar las bicicletas rentadas 
    def encontrar_rental(self, rental_id):
        for rental in self.rentals:
            if rental.id_rental == rental_id:
                return rental
        return None
    def imprimir_bicicletas(self):
        for bike in self.bikes:
            print(bike)
    def eliminar_bicicleta(self, bike ):
        self.bikes.remove(bike)
class Invoice:
    def __init__(self, rental, price: str):
        self.rental = rental
        self.price = price
    def __str__(self):
         return f"Renta: {self.rental} con un precio pagado de: {self.price}"
        

        