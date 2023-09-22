# view
import sys
from typing import Optional

from model import BikeRentalSystem, Bike, User
from datetime import datetime

option = 0
bike_rental_system = BikeRentalSystem()

class Menu:
    def __init__(self,bike_rental:BikeRentalSystem):
        self.bike_rental_system = bike_rental
    def entrada_num(self,text):
        try:
            entrada = int(input(text))
            return entrada
        except:
            print("No ingresaste un número: Tenga en cuenta los numeros dados con su respectiva funcionalidad")
            return self.entrada_num("por favor ingrese una opcion: ")
class Menu_usuarios(Menu):
    def mostrar_menu(self):
        print("1. Crear Usuario")   
    def Crear_usuario(self):
        name = input("Ingrese el nombre: ")
        email = input("Ingrese el correo electronico: ")
        phone = input("Ingrese el numero celular: ")
        usuario = User(name, email, phone)
        self.bike_rental_system.agregar_user(usuario)

    def seleccionar_usuario(self):
        if len(self.bike_rental_system.users) ==0:
            print("Por favor Registre un usuario")
            self.Crear_usuario()
            return self.bike_rental_system.users[-1]
        print("Por favor elije un usuario,(tenga en cuenta que debe elegir el primer numero de la izquierda): ")
        for index,user in enumerate(self.bike_rental_system.users):
            print(f"{index} {user}") 
        numero =self.entrada_num("por favor ingresar el numero del usuario: ")
        while numero >= len(self.bike_rental_system.users):
            print("El numero esta fuera del rango de listas disponibles")
            numero =self.entrada_num("por favor ingresar el numero del usuario: ")
        return self.bike_rental_system.users[numero]

class Menu_bicicletas(Menu):
    def rent_bike(self, usuario): 
        bike = self.bike_rental_system.bikes # seleccionar bicicleta()
        start_date = datetime.now()
        print(start_date.hour)
        # crear el objeto,
        bicicleta = self.seleccionar_bicicleta()
        id_rental = usuario.name + usuario.phone
        self.bike_rental_system.rentar_bike(bicicleta,usuario,start_date, id_rental)
        print("Su bicicleta ha sido alquilada :)")

        for q in self.bike_rental_system.bikes:
            print(q)

    def mostar_menu(self):
        print("2. Registrar bicicleta ")
        print("3. eliminar bicicleta ")
        print("4. Rentar bicicleta ")
        print("5. devolver bicicleta ")

    def seleccionar_bicicleta(self):
        if len(self.bike_rental_system.bikes) ==0:
            print("Por favor Registre una bicicleta")
            self.registrar_bicicleta()
            return self.bike_rental_system.bikes[-1]
        print("Por favor elije una bicicleta, (tenga en cuenta que debe elegir el primer numero de la izquierda): ")
        for index,bike in enumerate(self.bike_rental_system.bikes):
            if self.bike_rental_system.bikes[index].available:
                print(f"{index:} {bike}")
            bicis =self.entrada_num("por favor ingresar el numero de la bicicleta : ")
            while bicis >= len(self.bike_rental_system.bikes) or not self.bike_rental_system.bikes[bicis].available :
                print("El numero esta fuera del rango de listas disponibles")
                bicis =self.entrada_num("por favor ingresar el numero de la bicicletas: ")
            return self.bike_rental_system.bikes[bicis]
    def return_bike(self):
        if len(self.bike_rental_system.rentals)== 0:
            print("No se ha rentado ninguna bicicleta")
            return
        for e in self.bike_rental_system.rentals:
            print(e)
        print("Por favor digite solamente el ID del numero de renta: ")
        x = input("por favor ingrese el ID del numero de renta: ")
        fecha = int(input("Ingrese cuantos días has tenido la bicicleta: "))
        y= self.bike_rental_system.return_bike(x, fecha)#falta agregar el id de la renta
        print(y)
        #devolver la bicicleta
    def registrar_bicicleta(self):
        id = input("Ingrese el ID de la bicicleta: ")
        name = input("Ingrese el nombre de la bicicleta: ")
        description = input("Ingrese la descripcion de la bicicleta: ")
        price = int(input("Ingrese el precio de renta de la bicicleta por dia: "))
        model = input("Ingrese el modelo de la bicicleta: ")
        available = True
        bike = Bike(id, name, description, price, available, model) # se creo el objeto
        self.bike_rental_system.agregar_bike(bike) # se agrego a la lista de bicicletas
        print("La bicicleta ha sido creada con exito")
    def eliminar_bicicleta(self):
        if len(self.bike_rental_system.bikes) == 0:
            print("No hay bicicletas Registradas")
            return 
        self.bike_rental_system.imprimir_bicicletas()
        id = input("Ingrese el ID de la bicicleta que desee eliminar,(tenga en cuenta que el ID es el primer numero de la izquierda): ")
        bicicleta_encontrada = self.bike_rental_system.encontrar_bike(id)
        self.bike_rental_system.eliminar_bicicleta(bicicleta_encontrada)
        print("La bicicleta ha sido eliminada")

class Menu_general(Menu):
    def __init__(self,bike_rental_system ):
        super().__init__(bike_rental_system )
        exit = False
        menu_usuario = Menu_usuarios(bike_rental_system)
        menu_bici = Menu_bicicletas(bike_rental_system)
        while not exit:
            print("Bienvenido al sistema de alquiler de bicicletas !")
            menu_usuario.mostrar_menu()
            menu_bici.mostar_menu()
            print("6. Exit")
            option = self.entrada_num("Por favor ingrese una opcion: ")
            if option ==1:
                menu_usuario.Crear_usuario()
            if option == 2:
                menu_bici.registrar_bicicleta()
            if option == 3:
                menu_bici.eliminar_bicicleta()
            if option == 4:
                usuario = menu_usuario.seleccionar_usuario()
                menu_bici.rent_bike(usuario)
            if option == 5:
                menu_bici.return_bike()
            if option == 6:
                exit = True

