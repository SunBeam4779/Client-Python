# from PyQt5.Qt import QDate
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication
from Client.StartWindow import StartWindow
from Client.InformationCheck import InformationCheck  # this should be neglected
from Client.MainWindow import MainWindow
from Client.BLE import BLE
from Client.DataAcquire import DataAcquire
from Client.Synchronize import Synchronize
from Client.DataManager import DataManager
from Client.Display import Display
from Client.DataAcquire import DataAcquire
from Client.LogManager import LogManager
import sys

# date = QDate().currentDate()
# thisday = date.day()
# day = str(date.day())
# if thisday < 10:
#     day = "0" + day
# year = str(date.year())
# month = str(date.month())
# thisDate = year + month + day
# print(thisDate)
app = QApplication(sys.argv)
# window = DataAcquire(None)
# window = MainWindow([])
# window = InformationCheck()  # this should be neglected
# window = Synchronize(None)
window = StartWindow()
# window = BLE()
# window = DataManager(0)
# window = LogManager("not defined")
# window = Display("D:\\My Documents\\ECG Detector Project\\data\\ECG\\Filtered\\data999_Channel1_dec.txt")
window.show()
app.exec_()
