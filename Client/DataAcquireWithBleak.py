import asyncio
import struct

from PyQt5.Qt import *
# from Client.Util import MyDelegate
# from bluepy import btle
from bleak import BleakClient


class DataAcquireWithBleak(QWidget):
    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 800
    _size_of_y = 600
    # _address = ""
    _peripheral = None

    def __init__(self, address):
        super(DataAcquireWithBleak, self).__init__()

        self._address = address
        # self._peripheral = peripheral

        # set ICON
        self.Icon = QIcon(self._icon)

        # set choice
        self.ECG = QLabel()
        self.SpO2 = QLabel()
        self.Respiration = QLabel()
        self.PulseWave = QLabel()

        # set button
        self.save = QPushButton()
        self.clear = QPushButton()
        self.acquire = QPushButton()
        self.exit = QPushButton()

        # set Text Edit
        font_of_data = QFont()
        font_of_data.setFamily("Times")
        font_of_data.setPixelSize(20)
        self.ECGWin = QTextEdit()
        self.ECGWin.setFont(font_of_data)
        self.SpO2Win = QTextEdit()
        self.SpO2Win.setFont(font_of_data)
        self.RespirationWin = QTextEdit()
        self.RespirationWin.setFont(font_of_data)
        self.PulseWaveWin = QTextEdit()
        self.PulseWaveWin.setFont(font_of_data)

        # set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_left_layout = QVBoxLayout()
        self.vertical_right_layout = QVBoxLayout()
        self.horizon_left_layout1 = QHBoxLayout()
        self.horizon_left_layout2 = QHBoxLayout()
        self.horizon_left_layout3 = QHBoxLayout()
        self.horizon_left_layout4 = QHBoxLayout()

        self.thread = Worker(self._peripheral)
        # print(self._address)
        self.thread.sinOut.connect(self.slot_data)

        # set ui
        self.add_button_and_label()
        self.set_ui()
        # self.start()

    def set_ui(self):
        """
        set the graph layout
        :return: none
        """

        self.setLayout(self.horizon_layout)
        self.setWindowTitle("数据采集")
        self.setWindowIcon(self.Icon)
        self.setWindowState(Qt.WindowMaximized)
        # self.resize(self._size_of_x, self._size_of_y)

        # set left
        self.horizon_left_layout1.addWidget(self.ECG)
        self.horizon_left_layout1.addWidget(self.ECGWin)
        self.horizon_left_layout2.addWidget(self.Respiration)
        self.horizon_left_layout2.addWidget(self.RespirationWin)
        self.horizon_left_layout3.addWidget(self.PulseWave)
        self.horizon_left_layout3.addWidget(self.PulseWaveWin)
        self.horizon_left_layout4.addWidget(self.SpO2)
        self.horizon_left_layout4.addWidget(self.SpO2Win)

        self.vertical_left_layout.addStretch(1)
        self.vertical_left_layout.addLayout(self.horizon_left_layout1)
        self.vertical_left_layout.addStretch(1)
        self.vertical_left_layout.addLayout(self.horizon_left_layout2)
        self.vertical_left_layout.addStretch(1)
        self.vertical_left_layout.addLayout(self.horizon_left_layout3)
        self.vertical_left_layout.addStretch(1)
        self.vertical_left_layout.addLayout(self.horizon_left_layout4)
        self.vertical_left_layout.addStretch(1)

        # set right
        # self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.save)
        self.vertical_right_layout.addWidget(self.clear)
        self.vertical_right_layout.addWidget(self.acquire)
        self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.exit)
        # self.vertical_right_layout.addStretch(1)

        # set layout
        self.horizon_layout.addLayout(self.vertical_left_layout)
        # self.horizon_layout.addStretch(1)
        # self.horizon_layout.addWidget(self.dataWin)
        self.horizon_layout.addLayout(self.vertical_right_layout)

    def add_button_and_label(self):
        """
        set the button to receive the notification or clear the textedit
        :return: none
        """

        font_of_label = QFont()
        font_of_label.setFamily("Times")
        font_of_label.setPixelSize(35)

        font_of_button = QFont()
        font_of_button.setFamily("Times")
        font_of_button.setPixelSize(55)

        # label
        self.ECG.setFont(font_of_label)
        self.SpO2.setFont(font_of_label)
        self.PulseWave.setFont(font_of_label)
        self.Respiration.setFont(font_of_label)

        # button
        self.save.setFixedSize(120, 120)
        self.save.setFont(font_of_button)
        self.clear.setFixedSize(120, 120)
        self.clear.setFont(font_of_button)
        self.acquire.setFixedSize(120, 120)
        self.acquire.setFont(font_of_button)
        self.exit.setFixedSize(120, 120)
        self.exit.setFont(font_of_button)

        self.ECG.setText("心电")
        self.SpO2.setText("血氧")
        self.PulseWave.setText("脉搏")
        self.Respiration.setText("呼吸")
        self.save.setText("保存")
        self.clear.setText("清除")
        self.acquire.setText("采集")
        self.exit.setText("返回")

        self.save.clicked.connect(self.slot_stop)
        self.clear.clicked.connect(self.slot_clear)
        self.acquire.clicked.connect(self.start)
        self.exit.clicked.connect(self.close_win)

    def slot_stop(self):
        """
        stop the thread's loop
        :return: none
        """

        self.thread.stop.set()

    def start(self):
        """
        the slot function to start notification receiving thread
        :return: none
        """

        self.thread.start()
        if not self.thread.state:
            QMessageBox.information(self, '错误！', '蓝牙连接失败！请返回重连。', QMessageBox.Ok)

    def slot_clear(self):
        """
        clear the window
        :return: none
        """

        self.ECGWin.clear()

    def slot_data(self, msg):
        """
        add the received notification to the textedit
        :param msg: the notification
        :return: none
        """

        self.ECGWin.append(msg)

    def close_win(self):
        """
        close the window
        :return: none
        """

        self.close()


class Worker(QThread):
    sinOut = pyqtSignal(str)
    address = None
    CHAR_NBR_UUID = "f000fff1-0451-4000-b000-000000000000"
    state = True

    def __init__(self, address):
        super(Worker, self).__init__()
        self.working = True
        # self.address = address
        self.address = address
        self.stop = asyncio.Event()

    @staticmethod
    async def running(address_, loop_, stop):

        stop_event = stop

        def data_handler(sender, data_):
            Worker.sinOut.emit(data_.hex())
            # print("{0}: {1}".format(sender, data_.hex()))

        async with BleakClient(address_, loop=loop_) as client:
            x = await client.is_connected()
            if not x:
                return False
            else:

                await client.start_notify(Worker.CHAR_NBR_UUID, data_handler)

                await stop_event.wait()

                await client.stop_notify(Worker.CHAR_NBR_UUID)
            return True

    def run(self):
        """
        the main task to be execute
        :return: none
        """

        loop = asyncio.get_event_loop()
        futures = asyncio.ensure_future(Worker.running(self.address, loop, self.stop))
        loop.run_until_complete(futures)
        if not futures.result():
            self.state = False
