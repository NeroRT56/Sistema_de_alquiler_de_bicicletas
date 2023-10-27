from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QMessageBox
from PyQt5 import QtCore, uic
from model import Bike, BikeRentalSystem, User
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QDoubleValidator

class ModeloView():
    def __init__(self):
        pass
    def __cinfigurar(self):
        table_model = QStandardItemModel()
        table_model.setHorizontalHeaderLabels(["usuario", "bicicleta", ])
        self.tableViewPosible.setModel(table_model)
        self.tableViewPosible.setEditTriggers(QAbstractItemView.noEditTriggers)
        self.tableViewPosible.setColumnWidth(0, 230)
        self.tableViewPosible.setColumnWidth(1, 230)
        

