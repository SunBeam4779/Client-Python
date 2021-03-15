from PyQt5.Qt import *
from Client.Util import Scanner
from Client.DataAcquire import DataAcquire
# from bluepy import btle


class BLE(QWidget):

    """
    the entrance of BLE message handling
    """

    signal = pyqtSignal(int)
    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 600
    _size_of_y = 350
    _row = 0
    _result_of_scan = {}
    _address = ""
    _peripheral = None
    _user_unique = "not defined"
    _connect_state = 'disc'
    _data_type = "not defined"

    def __init__(self, user_unique):
        super(BLE, self).__init__()
        self.data_acquire_win = None

        self._user_unique = user_unique

        # set ICON
        self.Icon = QIcon(self._icon)

        # set label
        self.StatusOfBLE = QLabel(self)

        # set status image
        self.status = QFrame(self)
        self.status.setFixedSize(70, 70)
        self.color = QColor(0, 0, 0)
        self.color.setRed(255)
        self.status.setStyleSheet('QWidget { background-color:%s }' % self.color.name())

        # set button
        self.Refresh = QPushButton()
        self.Search = QPushButton()
        self.Connect = QPushButton()
        self.Disconnect = QPushButton()
        self.Acquire = QPushButton()
        self.Exit = QPushButton()

        # set table container
        font_of_table = QFont()
        font_of_table.setFamily("Times")
        font_of_table.setPixelSize(45)

        self.table = QTableWidget()
        self.table.setFont(font_of_table)
        self.table.setFixedSize(1500, 880)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Name', 'MAC'])
        self.table.setShowGrid(False)
        self.table.setColumnWidth(0, 840)
        self.table.setColumnWidth(1, 650)
        self.table.clicked.connect(self.select_item)

        # set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_left_layout = QVBoxLayout()
        self.horizon_left_top_layout = QHBoxLayout()
        self.vertical_right_layout = QVBoxLayout()

        # add item
        self.add_label()
        self.add_button()

        # set UI
        self.set_ui()

    def set_ui(self):

        """
        set the graph layout
        :return: none
        """

        self.setLayout(self.horizon_layout)
        self.setWindowTitle("蓝牙连接")

        self.setWindowIcon(self.Icon)
        self.setWindowState(Qt.WindowMaximized)
        # self.resize(self._size_of_x, self._size_of_y)

        # set left-top
        self.horizon_left_top_layout.addWidget(self.StatusOfBLE)
        self.horizon_left_top_layout.addWidget(self.status)
        self.horizon_left_top_layout.addStretch(0)

        # set left
        self.vertical_left_layout.addLayout(self.horizon_left_top_layout)
        self.vertical_left_layout.addWidget(self.table)

        # set right
        self.vertical_right_layout.addWidget(self.Refresh)
        self.vertical_right_layout.addWidget(self.Search)
        self.vertical_right_layout.addWidget(self.Connect)
        self.vertical_right_layout.addWidget(self.Disconnect)
        self.vertical_right_layout.addWidget(self.Acquire)
        self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.Exit)

        # set layout
        self.horizon_layout.addLayout(self.vertical_left_layout)
        self.horizon_layout.addStretch(0)
        self.horizon_layout.addLayout(self.vertical_right_layout)

    def add_button(self):

        """
        set the button to perform the search, refresh, acquire data
        :return: none
        """

        font_of_button = QFont()
        font_of_button.setFamily("Times")
        font_of_button.setPixelSize(50)

        self.Refresh.setFont(font_of_button)
        self.Search.setFont(font_of_button)
        self.Connect.setFont(font_of_button)
        self.Disconnect.setFont(font_of_button)
        self.Acquire.setFont(font_of_button)
        self.Exit.setFont(font_of_button)

        self.Refresh.setText("刷新")
        self.Search.setText("搜索")
        self.Connect.setText("连接")
        self.Disconnect.setText("断开")
        self.Acquire.setText("采集")
        self.Exit.setText("返回")

        self.Refresh.setFixedSize(300, 110)
        self.Search.setFixedSize(300, 110)
        self.Connect.setFixedSize(300, 110)
        self.Disconnect.setFixedSize(300, 110)
        self.Acquire.setFixedSize(300, 110)
        self.Exit.setFixedSize(300, 110)

        self.Refresh.clicked.connect(self.slot_search_or_refresh)
        self.Search.clicked.connect(self.slot_search_or_refresh)
        self.Connect.clicked.connect(self.slot_connect)
        self.Disconnect.clicked.connect(self.slot_disconnect)
        self.Acquire.clicked.connect(self.slot_acquire_data)
        self.Exit.clicked.connect(self.close_win)

    def add_label(self):

        """
        add the label
        :return: none
        """

        font_of_label = QFont()
        font_of_label.setFamily("Times")
        font_of_label.setPixelSize(80)

        self.StatusOfBLE.setFont(font_of_label)

        self.StatusOfBLE.setText("蓝牙连接状态：")

    def slot_search_or_refresh(self):

        """
        slot function to realize the BLE peripherals scanning or rescanning.
        :return: none
        """

        # self.table.clearContents()
        scanner = Scanner()
        self._result_of_scan = scanner.scan()
        self._row = len(self._result_of_scan)
        self.table.setRowCount(self._row)
        self.table.setHorizontalHeaderLabels(['名称', 'MAC'])

        # font
        font = QFont()
        font.setFamily("Times")
        font.setPixelSize(20)

        keys = list(self._result_of_scan.keys())
        # print(type(keys))
        for index in range(len(keys)):
            name = QTableWidgetItem()
            mac = QTableWidgetItem()
            name.setFont(font)
            mac.setFont(font)
            name.setText(str(keys[index]))
            mac.setText(self._result_of_scan[keys[index]])

            self.table.setItem(index, 0, name)
            self.table.setItem(index, 1, mac)

    def select_item(self):

        """
        slot function to get the MAC address of the selected item
        :return:
        """

        row_index = self.table.currentIndex().row()
        items = list(self._result_of_scan.keys())
        self._address = self._result_of_scan[items[row_index]]
        name = str(items[row_index])  # get the name of BLE peripheral
        if name == "BW-ECG-01":
            self._data_type = "ECG01"
        else:
            self._data_type = name[-3:]
        # print(self._data_type)

    def slot_connect(self):

        """
        slot function to connect the BLE peripheral
        :return: none
        """

        # self.data_acquire_win = DataAcquire(self._address)
        # self.data_acquire_win.show()
        # self._peripheral = btle.Peripheral()
        self._peripheral._startHelper()
        self._peripheral.connect(self._address)
        self._connect_state = self._peripheral.getState()
        self.change_BLE_state()

    def slot_acquire_data(self):

        """
        slot function to start the data acquiring window
        :return: none
        """

        self.data_acquire_win = DataAcquire(self._peripheral, self._user_unique, self._data_type)
        self.data_acquire_win.show()

    def change_BLE_state(self):

        """
        change the color to describe the state of BLE connection
        :return: none
        """

        if self._connect_state == 'conn':
            self.color.setGreen(255)
        elif self._connect_state == 'disc':
            self.color.setRed(255)
        self.status.setStyleSheet('QWidget { background-color:%s }' % self.color.name())

    def slot_disconnect(self):

        """
        disconnect from the peripheral
        :return: none
        """

        # self._peripheral._startHelper()

        self._connect_state = 'disc'
        self._peripheral.disconnect()
        self.change_BLE_state()

    def close_win(self):

        """
        close the window
        :return: none
        """

        self.signal.emit(1)
        self.close()
