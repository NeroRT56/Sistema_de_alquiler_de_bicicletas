#model
#sistema de alquiler de bicicletas 
from datetime import date
import math
from datetime import datetime
from datetime import timedelta
import csv
class Bike:
    def __init__(self, id : str ,name: str, description: str, price: int, available: bool, model: str):
        self.id: str = id
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
    def __init__(self, bike: Bike, user: str, start_date, end_date, id_rental: str):
        self.bike = bike
        self.user = user
        self.start_date = start_date # igual a datetime.now()
        self.end_date = 0 
        self.id_rental = id_rental
    # funcionalidad de calcular el precio
    # me toco colocar end_date porque me lo pedia 

    def calculate_price(self):
        tomorrow = self.start_date +timedelta(days=self.end_date)
        hours = (tomorrow.day - self.start_date.day)
        return self.bike.price * math.ceil(hours)
    def __str__(self):
        return f"id de la renta : {self.id_rental} fecha inicial:  {self.start_date} usuario : {self.user}"

class BikeRentalSystem:
    def __init__(self):
        self.bikes: dict[str: Bike] = []
        self.users = []
        self.rentals = []
        self.invoices = []
        self.__cargar_catalogoBicicletas()
        self.__cargar_catalogosUsuarios()
        self.__cargar_catalogoRentas()
        

    def __cargar_catalogoBicicletas(self):
        with open("data/catalogo-Bicicletas.csv") as file:
            
            csv_data = list(csv.reader(file, delimiter =(";")))
            print(csv_data)
            bicis = list(map(lambda data: Bike(data[0], data[1], data[2], float(data[3]), data[4], data[5]), list(csv_data)))
            #lo hago con para el metodo de bicicletas-revisar
            self.bikes = bicis
            print(self.bikes)
            # debo modificar dicho archivo 

    def __cargar_catalogosUsuarios(self):
        with open("data/catalogo-Usuarioss.csv") as file:
            
            csv_data = list(csv.reader(file, delimiter =(";")))
            print(csv_data)
            users = list(map(lambda data: User(data[0], data[1], data[2]), list(csv_data)))
           # lo hago con para el metodo de usuarios-revisar
            self.users= users 
            print(self.users)
            # debo modificar dicho archivo s 

    def __cargar_catalogoRentas(self):
        with open ("data/catalogo-Rentas.csv") as file:
            csv_data = list(csv.reader(file, delimiter =(";")))
            print(csv_data)
            rentas = list(map(lambda data: Rental(data[0], data[1], data[2], data[3], data[4]), list(csv_data)))
            self.rentals = rentas
            print(self.rentals)


    def __agregaralCatalogoUsuarios(self,user : User):
        #Aquí se modifica el archivo
        listuser = [user.name,user.email,user.phone]
        with open("data/catalogo-Usuarioss.csv", "a", newline="") as f_object:
            writer_object = csv.writer(f_object, delimiter =(";"))
            writer_object.writerow(listuser)
            f_object.close()
            
    def __agregaralcatalogoBicicletas(self, bicis : Bike):
        ##Aquí se modifica el archivo
        listbicis = [bicis.id, bicis.name, bicis.description, bicis.price, bicis.available, bicis.model]
        with open("data/catalogo-Bicicletas.csv", "a", newline="") as f_object:
            writer_object = csv.writer(f_object, delimiter =(";"))
            writer_object.writerow(listbicis)
            f_object.close()
    def __agregaralcatalogoRentas(self, rentas : Rental):
        listrentas= [rentas.bike, rentas.user , rentas.start_date, rentas.end_date, rentas.id_rental]
        with open("data/catalogo-Rentas.csv", "a", newline="") as f_object:
            writer_object = csv.writer(f_object, delimiter =(";"))
            writer_object.writerow(listrentas)
            f_object.close()


    def agregar_bike(self, bike):
        self.bikes.append(bike)
        #se utiliza el metedo para guardar en la interfaz por medio de agregar_bike
        self.__agregaralcatalogoBicicletas(bike)
         
    # agregar usuarios
    def agregar_user(self, user):
        self.users.append(user)
        self.__agregaralCatalogoUsuarios(user)
        #aqui me tocaria agregar los usuarios pero en la interfax 
    # rentar bicicletas
    def rentar_bike(self, bike, user, start_date,end_date, id_rental):
        rental = Rental(bike, user, start_date, end_date,  id_rental) # Aqui tambien me generaba error con el end date
        self.rentals.append(rental)
        bike.available = False
        print(rental)
        print(len(self.rentals))
        self.__agregaralcatalogoRentas(rental)

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
    def eliminar_bicicleta(self, bike: Bike ):
        self.bikes.remove(bike)
    def eliminar_usuario(self, user : User):
        self.users.remove(user)
class Invoice:
    def __init__(self, rental, price: str):
        self.rental = rental
        self.price = price
    def __str__(self):
         return f"Renta: {self.rental} con un precio pagado de: {self.price}"
        

        