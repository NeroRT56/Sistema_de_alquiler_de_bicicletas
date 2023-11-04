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
        self.listViewUsuariosDisponibles.setModel(QStandardItemModel())
        self.listViewBicicletasDisponibles.setModel(QStandardItemModel())
        self.listViewrentas.setModel(QStandardItemModel())
        self.listViewUsuariosDisponibles.selectionModel().selectionChanged.connect(self.obternerItemSeleccionadoUsuario)
        self.listViewBicicletasDisponibles.selectionModel().selectionChanged.connect(self.obternerItemSeleccionadoBicicletas)
        self.listViewrentas.selectionModel().selectionChanged.connect(self.obtenerItemSeleccionadoRenta)
        self.pushButtonAgrega_Nuevo_usuario.clicked.connect(self.abrir_dialogo_Agregar_usuario)
        self.pushButtonAgregar_Nueva_Bicicleta.clicked.connect(self.abrir_dialogo_Agregar_bicicletas)
        self.pushButtonEliminar_Usuario.clicked.connect(self.eliminarItemSeleccionadoUsuario)
        self.pushButtonEliminar_Bicicleta.clicked.connect(self.eliminarItemSeleccionadoBicicleta)
        self.pushButtonAlquilar_Bicicleta.clicked.connect(self.obtenerRentaBicicletas)
        self.pushButtonDevolver_Bicicleta.clicked.connect(self.devolverRentaBicicletas)
 
    def obternerItemSeleccionadoUsuario(self):
        indice_seleccionado = self.listViewUsuariosDisponibles.currentIndex()
        if indice_seleccionado.isValid(): 
            self.usuario_seleccionado = self.listViewUsuariosDisponibles.model(
            ).itemFromIndex(indice_seleccionado) 
            print(f"Elemento seleccionado: {self.usuario_seleccionado.user}")

    def obternerItemSeleccionadoBicicletas(self):
        indice_seleccionado = self.listViewBicicletasDisponibles.currentIndex()
        if indice_seleccionado.isValid():  
            self.bicicleta_seleccionada = self.listViewBicicletasDisponibles.model(
            ).itemFromIndex(indice_seleccionado) 
            print(f"Elemento seleccionado: {self.bicicleta_seleccionada.bicis}")

    def eliminarItemSeleccionadoUsuario(self):         
        usuario = self.usuario_seleccionado
        if usuario is None:
            msg_box = QMessageBox(None)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe Seleccionar el usuario para poder eliminarlo")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            return  
        question =  question =QMessageBox.question(self,"Eliminar","¿Deseas eliminar el usuario {}".format(usuario.user.name),QMessageBox.Yes | QMessageBox.No)
        if question == QMessageBox.Yes:
            self.runin.eliminar_usuario(usuario.user)            
            self.__cargar_datos_usuario()
        
    def eliminarItemSeleccionadoBicicleta(self):
        bicicleta = self.bicicleta_seleccionada
        if bicicleta is None:
            msg_box = QMessageBox(None)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe Seleccionar una bicicleta para poder eliminarla")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            return
        else:
            question = question = QMessageBox.question(self,"Eliminar","¿Deseas eliminar la bicicleta {}?".format(bicicleta.bicis.name) , QMessageBox.Yes | QMessageBox.No)
        if question == QMessageBox.Yes:
            self.runin.eliminar_bicicleta(bicicleta.bicis)           
            self.__cargar_datos_bicicletas()

    def obtenerRentaBicicletas(self):
        usuario_selec = self.usuario_seleccionado
        bicicleta_selec = self.bicicleta_seleccionada 
        end_date = datetime.strptime("2999-10-10 0:0:0" , "%Y-%m-%d %H:%M:%S")
        if usuario_selec is not None and bicicleta_selec is not None:
            start_date = datetime.now()
            start_date = datetime.strptime(str(start_date).split(".")[0], "%Y-%m-%d %H:%M:%S")
            print(start_date.hour)
            id_rental = usuario_selec.user.name + usuario_selec.user.phone
            new_rental = self.runin.rentar_bike(bicicleta_selec.bicis,usuario_selec.user,start_date, end_date, id_rental)            
            item =QStandardItem(str(new_rental))
            item.rent= new_rental
            item.setEditable(False)
            self.listViewrentas.model().appendRow(item) 
        else:
            msg_box = QMessageBox(None)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe Seleccionar el usuario y la bicicleta para poder rentarla")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def obtenerItemSeleccionadoRenta(self):
        indice_seleccionado = self.listViewrentas.currentIndex()
        if indice_seleccionado.isValid():
            self.rentas_seleccionada = self.listViewrentas.model(
            ).itemFromIndex(indice_seleccionado) 
            print(f"Elemento seleccionado: {self.rentas_seleccionada.rent}")

    def devolverRentaBicicletas(self):
        selec_rent = self.rentas_seleccionada
        if selec_rent is None:
            msg_box = QMessageBox(None)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe Seleccionar una renta ")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        else:
            dialogo = QMessageBox.information(
            self, "Ventana de pago", "su valor a pagar es 10.000")
            
    def __cargar_datos_usuario(self):
        usuarios = self.runin.users
        self.listViewUsuariosDisponibles.model().clear()
        for user in usuarios:
            item =QStandardItem(str(user))
            item.user = user
            item.setEditable(False)
            self.listViewUsuariosDisponibles.model().appendRow(item)
    def __cargar_datos_rentas(self):
        rentas = self.runin.rentals
        self.listViewrentas.model().clear()
        for rent in rentas:
            item = QStandardItem(str(rent))
            item.rent = rent
            item.setEditable(False)
            self.listViewrentas.model().appendRow(item)

    def __cargar_datos_bicicletas(self):
        bicicletas = self.runin.bikes
        self.listViewBicicletasDisponibles.model().clear()
        for bicis in bicicletas:
            item = QStandardItem(str(bicis))
            item.bicis = bicis
            item.setEditable(False)
            self.listViewBicicletasDisponibles.model().appendRow(item)            

    def abrir_dialogo_Agregar_usuario(self):
        resp = self.dialogo_agregar_usuario.exec()
        if resp == QDialog.Accepted: 
            name = self.dialogo_agregar_usuario.lineEditNombre.text()
            email = self.dialogo_agregar_usuario.lineEditCorreo.text()
            phone = self.dialogo_agregar_usuario.lineEditCelular.text()
            newUser = User(name, email, phone)
            self.runin.agregar_user(newUser)
            item =QStandardItem(str(newUser))
            item.user = newUser
            item.setEditable(False)
            self.listViewUsuariosDisponibles.model().appendRow(item) 
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

class DialogoUsuariosAdd(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/Dialogo-AgregarUsuario.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):
        self.lineEditCelular.setValidator(QRegExpValidator(QRegExp("\\d{11}"), self.lineEditCelular))

    def limpiar(self):
        self.lineEditNombre.clear()
        self.lineEditCelular.clear()
        self.lineEditCorreo.clear()
        
    def accept(self) -> None:
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
        uic.loadUi("gui/Dialogo-AgregarBicicleta.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):
        self.lineEditID.setValidator(QRegExpValidator(QRegExp("\\d{6}"), self.lineEditID))
        editNameValidator = QRegExpValidator(QRegExp("\\d{6}"), self.lineEditName)
        editPriceValidator = QDoubleValidator(0, 9999999999, 4, self.lineEditPrice)
        self.lineEditPrice.setValidator(editPriceValidator)

    def limpiar(self):
        self.lineEditID.clear()
        self.lineEditName.clear()
        self.lineEditDescription.clear()
        self.lineEditPrice.clear()
        self.lineEditModel.clear()
 
    def accept(self) -> None:
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
