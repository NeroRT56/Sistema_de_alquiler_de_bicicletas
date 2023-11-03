import sys
import typing
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QMessageBox, QListView
from PyQt5 import QtCore, uic
from model import Bike, BikeRentalSystem, User
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QDoubleValidator
from datetime import datetime
class MainWindowSistemaBicicleta(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/InterfaxGrafica-Sistema_de_alquiler_bicicletas.ui", self)
        self.setFixedSize(self.size())
        self.dialogo_agregar_usuario = DialogoUsuariosAdd()
        self.dialogo_agregar_bicicletas = DialogoBicicletasAdd()
        self.runin =BikeRentalSystem()
        self.__configurar()
        self.__cargar_datos_usuario()
        self.__cargar_datos_bicicletas()
        self.__cargar_datos_rentas()
        self.usuario_seleccionado = None
        self.bicicleta_seleccionada = None
        self.rentas_seleccionada =None
        
    def __configurar(self):
        # configuramos el tableView
        self.listViewUsuariosDisponibles.setModel(QStandardItemModel())
        self.listViewBicicletasDisponibles.setModel(QStandardItemModel())
        self.listViewrentas.setModel(QStandardItemModel())
        # Este metodo se va a ejecutar cada que el usuario seleccione un item de la lista.
        self.listViewUsuariosDisponibles.selectionModel().selectionChanged.connect(self.obternerItemSeleccionadoUsuario)
        #este metodo se va a ejecutar cada que el usuario seleccione un item de las bicicletas
        self.listViewBicicletasDisponibles.selectionModel().selectionChanged.connect(self.obternerItemSeleccionadoBicicletas)
        #enlazar los eventos de los botones /pushButtonAgrega_Nuevo_usuario /pushButtonAgregar_Nueva_Bicicleta / 
        self.pushButtonAgrega_Nuevo_usuario.clicked.connect(self.abrir_dialogo_Agregar_usuario)
        self.pushButtonAgregar_Nueva_Bicicleta.clicked.connect(self.abrir_dialogo_Agregar_bicicletas)
        # Desde aca se utiliza para eliminar un item
        self.pushButtonEliminar_Usuario.clicked.connect(self.eliminarItemSeleccionadoUsuario)
        self.pushButtonEliminar_Bicicleta.clicked.connect(self.eliminarItemSeleccionadoBicicleta)
        # enlazar con la funcion de rentar bicicleta 
        self.pushButtonAlquilar_Bicicleta.clicked.connect(self.obtenerRentaBicicletas)
        #devolver la renta de la factura 
        self.pushButtonDevolver_Bicicleta.clicked.connect(self.devolverRentaBicicletas)

    #este metodo se va a ejecutar cada que el usuario le de click a un item de la lista 
    def obternerItemSeleccionadoUsuario(self):
        #metodo retorna el indice de la lista del elemento que se selecciono
        indice_seleccionado = self.listViewUsuariosDisponibles.currentIndex()
        if indice_seleccionado.isValid():  # Aca se verifica que el indice sea valido, (que no sea negativo y demas validaciones)
            self.usuario_seleccionado = self.listViewUsuariosDisponibles.model(
            ).itemFromIndex(indice_seleccionado)  # Obtengo el item QStandardItem que se ha seleccionado a partir del indice obtenido en la linea 45
            # imprimo el objeto user del item seleccionado. Este objeto user se asigna en la linea 56 de este archivo
            print(f"Elemento seleccionado: {self.usuario_seleccionado.user}")
    def obternerItemSeleccionadoBicicletas(self):
        indice_seleccionado = self.listViewBicicletasDisponibles.currentIndex()
        if indice_seleccionado.isValid():  # Aca se verifica que el indice sea valido, (que no sea negativo y demas validaciones)
            self.bicicleta_seleccionada = self.listViewBicicletasDisponibles.model(
            ).itemFromIndex(indice_seleccionado)  # Obtengo el item QStandardItem que se ha seleccionado a partir del indice obtenido en la linea 45
            # imprimo el objeto user del item seleccionado. Este objeto user se asigna en la linea 56 de este archivo
            print(f"Elemento seleccionado: {self.bicicleta_seleccionada.bicis}")
    def eliminarItemSeleccionadoUsuario(self):
        # falta solucionar el error 
        usuario = self.usuario_seleccionado.user
        if usuario is None:
            return
        question =  question =QMessageBox.question(self,"Eliminar","¿Deseas eliminar el usuario{}".format(usuario.name),QMessageBox.Yes | QMessageBox.No)       
        if question == QMessageBox.Yes:


            del usuario
        #aqui se utiliza el metodo para eliminar un item del usuario 
    def eliminarItemSeleccionadoBicicleta(self):
        bicicleta = self.bicicleta_seleccionada.bicis
        if bicicleta is None:
            
            return
        question = question = QMessageBox.question(self,"Eliminar","¿Deseas eliminar la bicicleta {}?".format(bicicleta.name) , QMessageBox.Yes | QMessageBox.No)
        if question == QMessageBox.Yes:
            del bicicleta

    def obtenerRentaBicicletas(self):
        #aquí esta la funcion de rentar bicicleta 
        usuario_selec = self.usuario_seleccionado.user
        bicicleta_selec = self.bicicleta_seleccionada.bicis
        #se coloca porque me genera un error 
        end_date = 0
        if usuario_selec and bicicleta_selec:
     # seleccionar bicicleta()
            start_date = datetime.now()
            print(start_date.hour)
            # crear el objeto,
            id_rental = usuario_selec.name + usuario_selec.phone
            self.runin.rentar_bike(bicicleta_selec,usuario_selec,start_date, end_date, id_rental)
        else:
            msg_box = QMessageBox(None)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe Seleccionar el usuario y la bicicleta para poder rentarla")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            #no funciona el condicional 
    def obtenerItemSeleccionadoRenta(self):
        indice_seleccionado = self.listViewrentas.currentIndex()
        if indice_seleccionado.isValid():
            self.rentas_seleccionada = self.listViewrentas.model(
            ).itemFromIndex(indice_seleccionado) 
            print(f"Elemento seleccionado: {self.rentas_seleccionada.rentas}")
            #solucionar el error no imprime
    def devolverRentaBicicletas(self):
        #Aqui irá el metodo para devolver la bicicleta y pagar 
        pass

    def __cargar_datos_usuario(self):
        # se quiere cargar los datos del catalogo de usuarios
        usuarios = self.runin.users
        for user in usuarios:
            item =QStandardItem(str(user))
            item.user = user
            item.setEditable(False)
            self.listViewUsuariosDisponibles.model().appendRow(item)
    def __cargar_datos_rentas(self):
        #continuar con el proceso
        rentas = self.runin.rentals
        for rent in rentas:
            item = QStandardItem(str(rent))
            item.rent = rent
            item.setEditable(False)
            self.listViewrentas.model().appendRow(item)

    def __cargar_datos_bicicletas(self):
        bicicletas = self.runin.bikes
        for bicis in bicicletas:
            item = QStandardItem(str(bicis))
            item.bicis = bicis
            item.setEditable(False)
            self.listViewBicicletasDisponibles.model().appendRow(item)

    def abrir_dialogo_Agregar_usuario(self):
        resp = self.dialogo_agregar_usuario.exec()
        if resp == QDialog.Accepted:
            #se agregan las campos de texto con sus respectivos nombres 
            name = self.dialogo_agregar_usuario.lineEditNombre.text()
            email = self.dialogo_agregar_usuario.lineEditCorreo.text()
            phone = self.dialogo_agregar_usuario.lineEditCelular.text()
            newUser = User(name, email, phone)
            self.runin.agregar_user(newUser)
            item =QStandardItem(str(newUser))
            item.user = newUser
            item.setEditable(False)
            self.listViewUsuariosDisponibles.model().appendRow(item) # corregir 
        self.dialogo_agregar_usuario.limpiar()

    def abrir_dialogo_Agregar_bicicletas(self):
        resp =self.dialogo_agregar_bicicletas.exec()
        if resp == QDialog.Accepted:
            id = self.dialogo_agregar_bicicletas.lineEditID.text()
            name = self.dialogo_agregar_bicicletas.lineEditName.text()
            description = self.dialogo_agregar_bicicletas.lineEditDescription.text()
            price = self.dialogo_agregar_bicicletas.lineEditPrice.text()
            available = True
            modell = self.dialogo_agregar_bicicletas.lineEditModel.text()
            newBike=Bike(id, name, description, price, available, modell)
            self.runin.agregar_bike(newBike)
            item = QStandardItem(str(newBike))
            item.bicis = newBike
            item.setEditable(False)
            self.listViewBicicletasDisponibles.model().appendRow(item)
        self.dialogo_agregar_bicicletas.limpiar()

#comenzamos con los dialogos 
class DialogoUsuariosAdd(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        #cargar el archivo
        uic.loadUi("gui/Dialogo-AgregarUsuario.ui", self)
        #para que la ventana no se pueda maximizar o minimizar
        self.setFixedSize(self.size())
        self.__configurar()
    def __configurar(self):
        self.lineEditCelular.setValidator(QRegExpValidator(QRegExp("\\d{11}"), self.lineEditCelular))

    def limpiar(self):
        #limpiar lineas de campo
        self.lineEditNombre.clear()
        self.lineEditCelular.clear()
        self.lineEditCorreo.clear()
        


    def accept(self) -> None:
        #aquí verificamos que se halla llenado todos los datos solicitados 
        if self.lineEditNombre.text() != "" and self.lineEditCorreo.text() != "" and self.lineEditCelular.text() != "":
           
            super().accept()
        else:
            print("error")
            msg_box = QMessageBox(None)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe Ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

class DialogoBicicletasAdd(QDialog):
    def __init__(self):
        QDialog.__init__(self)
         #cargar el archivo
        uic.loadUi("gui/Dialogo-AgregarBicicleta.ui", self)
        #para que la ventana no se pueda maximizar o minimizar
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):
        #aquí configuramos las validacion de  los line edit de los tipo de caracteretes, o enteron, floar va a recibir 
        #corregir 
        self.lineEditID.setValidator(QRegExpValidator(QRegExp("\\d{6}"), self.lineEditID))
        editNameValidator = QRegExpValidator(QRegExp("\\d{6}"), self.lineEditName)
        #self.lineEditName.setValidator(editNameValidator)
        #editDescriptionValidator = QRegExpValidator(QRegExp("\\d{6}"), self.lineEditDescription)
        #self.lineEditDescription.setValidator(editDescriptionValidator)
        editPriceValidator = QDoubleValidator(0, 9999999999, 4, self.lineEditPrice)
        self.lineEditPrice.setValidator(editPriceValidator) # Aquí se utiliza el validador para precio
        #self.lineEditModel.setValidator(QRegExpValidator(QRegExp("\\d{6}"), self.lineEditModel))

    def limpiar(self):
        #para limpiar los campos de textos
        self.lineEditID.clear()
        self.lineEditName.clear()
        self.lineEditDescription.clear()
        self.lineEditPrice.clear()
        self.lineEditModel.clear()
 
    def accept(self) -> None:
        #aquí verificamos que se halla llenado todos los datos solicitados 
        if self.lineEditID.text() != "" and self.lineEditName.text() != "" and self.lineEditDescription.text() != "" and self.lineEditPrice.text() != "" and self.lineEditModel.text() != "":
            super().accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe Ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowSistemaBicicleta()
    win.show()
    sys.exit(app.exec_())
