# from PyQt5.Qt import QDate
import sys
import os
# //-add the address of this project so that this code could be executed in command line
sys.path.append(os.path.dirname(sys.path[0]))

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
from Client.LogReader import LogReader

# os.environ['QT_IM_MODULE'] = "ibus"  # enable this program to use Chinese input in Linux environment.
app = QApplication(sys.argv)
# window = DataAcquire(None)
# window = MainWindow([])
# window = InformationCheck()  # this should be neglected
# window = Synchronize(None)
window = StartWindow()
# window = LogReader("", "", "", "")
# window = BLE()
# window = DataManager(0)
# window = LogManager("not defined")
# window = Display("D:\\My Documents\\ECG Detector Project\\data\\ECG\\Filtered\\data999_Channel1_dec.txt")
window.show()
app.exec_()
