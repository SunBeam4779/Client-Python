from PyQt5.Qt import *


class GetIP(QWidget):

    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 600
    _size_of_y = 500

    def __init__(self):
        super(GetIP, self).__init__()

        self.ip_address = ""

        # set ICON
        self.Icon = QIcon(self._icon)

        # set button
        self.confirm = QPushButton()
        self.clear = QPushButton()

        # set editor
        self.IP_address_edit = QLineEdit()

        # set label
        self.IP_label = QLabel()

        # set layout
        self.vertical_layout = QVBoxLayout()
        self.horizon_top_layout = QHBoxLayout()
        self.horizon_bottom_layout = QHBoxLayout()

        self.set_ui()
        self.add_label()
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
        self.horizon_top_layout.addWidget(self.IP_address_edit)

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

        self.clear.setFixedSize(60, 40)
        self.confirm.setFixedSize(60, 40)

        self.clear.clicked.connect(self.slot_clear)
        self.confirm.clicked.connect(self.slot_confirm)

    def add_label(self):

        """
        set the label info
        :return: none
        """

        font_of_label = QFont()
        font_of_label.setFamily("Times")
        font_of_label.setPixelSize(35)

        self.IP_label.setFont(font_of_label)
        self.IP_label.setText("请输入IP地址")

    def slot_clear(self):

        """
        clear the edit content.
        :return: none
        """

        self.IP_address_edit.clear()

    def slot_confirm(self):

        """
        set confirm action
        :return: none
        """

        self._ip_address = self.IP_address_edit.text()
        self.close()
