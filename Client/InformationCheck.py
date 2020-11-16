from PyQt5.Qt import *


class InformationCheck(QWidget):
    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 400
    _size_of_y = 300

    def __init__(self):
        super(InformationCheck, self).__init__()

        # set ICON
        self.Icon = QIcon(self._icon)

        # set label
        self.gender = QLabel(self)
        self.NumOfInfo = QLabel(self)
        self.username = QLabel(self)

        # set button
        self.button_check = QPushButton()
        self.PULSE = QRadioButton("Pulse Wave")
        self.SPO2 = QRadioButton("SpO2")
        self.BP = QRadioButton("Blood Pressure")
        self.RESP = QRadioButton("Respiration")
        self.ECG = QRadioButton("ECG")

        # set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_layout = QVBoxLayout()

        # add item
        self.add_button()
        self.add_label()

        # self.line = QPainter()
        # self.pen = QPen(Qt.black, 2, Qt.DashDotLine)
        # self.line.setPen(self.pen)
        # self.line.drawLine(80, 0, 80, 300)

        # set ui
        self.set_ui()

    def add_button(self):
        """set the button of user bio-parameter which can be chosen to display"""
        font_of_param = QFont()
        font_of_param.setFamily('Times')
        font_of_param.setPixelSize(22)

        self.ECG.setChecked(True)
        self.ECG.setFont(font_of_param)
        self.RESP.setFont(font_of_param)
        self.BP.setFont(font_of_param)
        self.SPO2.setFont(font_of_param)
        self.PULSE.setFont(font_of_param)

        self.button_check.setFont(font_of_param)
        self.button_check.setText("check")  # check button can display the kind of parameter chosen by the radiobutton.

    def add_label(self):
        """labels contain the user's information"""
        font_of_user = QFont()
        font_of_user.setFamily('Times')
        font_of_user.setPixelSize(18)

        self.username.setFont(font_of_user)
        self.NumOfInfo.setFont(font_of_user)
        self.gender.setFont(font_of_user)
        self.username.setText("name: Universal Voyage")
        self.NumOfInfo.setText("number of info: 20201013084453")
        self.gender.setText("gender: male")

    def set_ui(self):
        """set the graph layout"""
        self.setLayout(self.horizon_layout)
        self.setWindowTitle("Information checking")

        self.setWindowIcon(self.Icon)
        self.resize(self._size_of_x, self._size_of_y)

        self.vertical_layout.addWidget(self.username)
        self.vertical_layout.addWidget(self.NumOfInfo)
        self.vertical_layout.addWidget(self.gender)
        self.vertical_layout.addStretch(1)
        self.vertical_layout.addWidget(self.ECG, alignment=Qt.AlignLeft)
        self.vertical_layout.addWidget(self.RESP, alignment=Qt.AlignLeft)
        self.vertical_layout.addWidget(self.BP, alignment=Qt.AlignLeft)
        self.vertical_layout.addWidget(self.SPO2, alignment=Qt.AlignLeft)
        self.vertical_layout.addWidget(self.PULSE, alignment=Qt.AlignLeft)
        self.vertical_layout.addStretch(0)

        self.horizon_layout.addLayout(self.vertical_layout)
        self.horizon_layout.addWidget(self.button_check)
