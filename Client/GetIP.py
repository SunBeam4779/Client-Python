from PyQt5.Qt import *


class GetIP(QWidget):

    def __init__(self):
        super(GetIP, self).__init__()

        self.IP_address_edit = QTextEdit()
        self.IP_label = QLabel()

