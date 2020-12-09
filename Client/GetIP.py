from PyQt5.Qt import *


class GetIP(QWidget):

    """
    set the IP address of server
    """

    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 600
    _size_of_y = 500
    signal = pyqtSignal(dict)

    def __init__(self):
        super(GetIP, self).__init__()

        # //-set ICON
        self.Icon = QIcon(self._icon)

        # //-set button
        self.confirm = QPushButton()
        self.clear = QPushButton()

        # //-set editor
        self.IP_address1 = QLineEdit()
        self.IP_address2 = QLineEdit()
        self.IP_address3 = QLineEdit()
        self.IP_address4 = QLineEdit()
        self.IP_port = QLineEdit()

        # //-the address should not longer than 3 chars, and port should not longer than 5 chars
        self.IP_address1.setMaxLength(3)
        self.IP_address2.setMaxLength(3)
        self.IP_address3.setMaxLength(3)
        self.IP_address4.setMaxLength(3)
        self.IP_port.setMaxLength(5)

        # //-set validator which means the given range of data could be input into.
        address_validator = QIntValidator()
        address_validator.setRange(0, 255)
        port_validator = QIntValidator()
        port_validator.setRange(0, 65535)
        self.IP_address1.setValidator(address_validator)
        self.IP_address2.setValidator(address_validator)
        self.IP_address3.setValidator(address_validator)
        self.IP_address4.setValidator(address_validator)
        self.IP_port.setValidator(port_validator)

        # //-set the focus jumping signal. When address editor has 3 char, jump into the next address editor
        self.IP_address1.textChanged.connect(self.slot_jump1)
        self.IP_address2.textChanged.connect(self.slot_jump2)
        self.IP_address3.textChanged.connect(self.slot_jump3)
        self.IP_address4.textChanged.connect(self.slot_jump4)

        # set label
        self.IP_label = QLabel()
        self.dot1 = QLabel()
        self.dot2 = QLabel()
        self.dot3 = QLabel()
        self.port = QLabel()

        # set layout
        self.vertical_layout = QVBoxLayout()
        self.horizon_top_layout = QHBoxLayout()
        self.horizon_bottom_layout = QHBoxLayout()

        self.set_ui()
        self.add_label_and_edit()
        self.add_button()

    def set_ui(self):

        """
        set the graph layout
        :return: none
        """

        self.setLayout(self.vertical_layout)
        self.setWindowTitle("获取IP地址")

        self.setWindowIcon(self.Icon)
        self.resize(self._size_of_x, self._size_of_y)

        self.horizon_top_layout.addWidget(self.IP_label)
        self.horizon_top_layout.addWidget(self.IP_address1)
        self.horizon_top_layout.addWidget(self.dot1)
        self.horizon_top_layout.addWidget(self.IP_address2)
        self.horizon_top_layout.addWidget(self.dot2)
        self.horizon_top_layout.addWidget(self.IP_address3)
        self.horizon_top_layout.addWidget(self.dot3)
        self.horizon_top_layout.addWidget(self.IP_address4)
        self.horizon_top_layout.addWidget(self.port)
        self.horizon_top_layout.addWidget(self.IP_port)

        self.horizon_bottom_layout.addWidget(self.clear)
        self.horizon_bottom_layout.addStretch(0)
        self.horizon_bottom_layout.addWidget(self.confirm)

        self.vertical_layout.addLayout(self.horizon_top_layout)
        self.vertical_layout.addLayout(self.horizon_bottom_layout)

    def add_button(self):

        """
        set the button to perform the search, refresh, acquire data
        :return: none
        """

        font_of_button = QFont()
        font_of_button.setFamily("Times")
        font_of_button.setPixelSize(35)

        self.clear.setFont(font_of_button)
        self.confirm.setFont(font_of_button)

        self.clear.setText("清除")
        self.confirm.setText("确认")
        self.confirm.setDefault(True)

        self.clear.setFixedSize(180, 80)
        self.confirm.setFixedSize(180, 80)

        self.clear.clicked.connect(self.slot_clear)
        self.confirm.clicked.connect(self.slot_confirm)

    def add_label_and_edit(self):

        """
        set the label info
        :return: none
        """

        font = QFont()
        font.setFamily("Times")
        font.setPixelSize(35)

        self.IP_address1.setFont(font)
        self.IP_address2.setFont(font)
        self.IP_address3.setFont(font)
        self.IP_address4.setFont(font)
        self.IP_port.setFont(font)

        self.IP_label.setFont(font)
        self.IP_label.setText("请输入IP地址：")
        self.dot1.setFont(font)
        self.dot1.setText(".")
        self.dot2.setFont(font)
        self.dot2.setText(".")
        self.dot3.setFont(font)
        self.dot3.setText(".")
        self.port.setFont(font)
        self.port.setText("/")

    def slot_clear(self):

        """
        clear the edit content.
        :return: none
        """

        self.IP_address_edit.clear()

    def slot_jump1(self):

        """
        if the address1 has 3 char, jump to address2
        :return: none
        """

        if len(self.IP_address1.text()) == 3:
            self.IP_address2.setFocus()

    def slot_jump2(self):

        """
        if the address2 has 3 char, jump to address3
        :return: none
        """

        if len(self.IP_address2.text()) == 3:
            self.IP_address3.setFocus()

    def slot_jump3(self):

        """
        if the address3 has 3 char, jump to address4
        :return: none
        """

        if len(self.IP_address3.text()) == 3:
            self.IP_address4.setFocus()

    def slot_jump4(self):

        """
        if the address4 has 3 char, jump to port
        :return: none
        """

        if len(self.IP_address4.text()) == 3:
            self.IP_port.setFocus()

    def slot_confirm(self):

        """
        set confirm action
        :return: none
        """

        ip_address1 = self.IP_address1.text()
        ip_address2 = self.IP_address2.text()
        ip_address3 = self.IP_address3.text()
        ip_address4 = self.IP_address4.text()
        ip_port = self.IP_port.text()
        address = ip_address1 + "." + ip_address2 + "." + ip_address3 + "." + ip_address4

        # //-send the ip address and port number to the main window through signal(dict type)
        self.signal.emit({'ip': address, 'port': ip_port})
        self.close()
