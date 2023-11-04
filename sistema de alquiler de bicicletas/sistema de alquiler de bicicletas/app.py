from model import BikeRentalSystem
from interfax  import MainWindowSistemaBicicleta
import sys
import typing
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QMessageBox, QListView
from PyQt5 import QtCore, uic
from model import Bike, BikeRentalSystem, User
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QDoubleValidator
from datetime import datetime
BikeRentalSystem()
QApplication(sys.argv)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowSistemaBicicleta()
    win.show()
    sys.exit(app.exec_())
