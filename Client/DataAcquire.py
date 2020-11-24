import struct
import time

from PyQt5.Qt import *
# from Client.Util import MyDelegate
from Client.Util import Splitter
# from bluepy import btle
from queue import Queue
import pyqtgraph as pg


class DataAcquire(QWidget):
    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 800
    _size_of_y = 600
    # _address = ""
    _peripheral = None
    q = None
    result1 = []
    result2 = []
    display1 = None
    display2 = None
    original1 = []
    original2 = []
    ECG_data = [0 for i in range(500)]

    def __init__(self, peripheral):
        super(DataAcquire, self).__init__()

        # self._address = address
        self._peripheral = peripheral

        # set ICON
        self.Icon = QIcon(self._icon)

        # queue
        self.q = Queue()
        self.display1 = Queue()
        self.display2 = Queue()

        # set choice
        self.ECG = QLabel()
        self.SpO2 = QLabel()
        self.Respiration = QLabel()
        self.PulseWave = QLabel()

        # set button
        self.save = QPushButton()
        self.clear = QPushButton()
        self.receive = QPushButton()
        self.exit = QPushButton()

        # set Text Edit
        font_of_data = QFont()
        font_of_data.setFamily("Times")
        font_of_data.setPixelSize(20)
        # self.ECGWin = QTextEdit()
        # self.ECGWin.setFont(font_of_data)
        # self.SpO2Win = QTextEdit()
        # self.SpO2Win.setFont(font_of_data)
        # self.RespirationWin = QTextEdit()
        # self.RespirationWin.setFont(font_of_data)
        # self.PulseWaveWin = QTextEdit()
        # self.PulseWaveWin.setFont(font_of_data)

        # set data graph
        pg.setConfigOption('background', 'w')  # #f0f0f0
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOptions(antialias=True)

        self.ECGWin = pg.GraphicsLayoutWidget(self)
        # self.SpO2Win = pg.GraphicsLayoutWidget(self)
        self.RespirationWin = pg.GraphicsLayoutWidget(self)
        self.PulseWaveWin = pg.GraphicsLayoutWidget(self)
        # self.ECGWin.setXRange(self, )

        # pen = pg.mkPen(color='r', width=2)
        self.pen = pg.mkPen(color='r', width=2)  # (200, 200, 255)
        self.ECGWinHandle = self.ECGWin.addPlot(pen=pg.mkPen(color='b', width=2))
        # self.SpO2WinHandle = self.SpO2Win.addPlot()
        self.RespirationWinHandle = self.RespirationWin.addPlot()
        self.PulseWaveWinHandle = self.PulseWaveWin.addPlot()

        self.curveECG = self.PulseWaveWinHandle.plot(self.ECG_data, pen=self.pen)
        self.ECG_pointer = 0

        # set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_left_layout = QVBoxLayout()
        self.vertical_right_layout = QVBoxLayout()
        self.horizon_left_layout1 = QHBoxLayout()
        self.horizon_left_layout2 = QHBoxLayout()
        self.horizon_left_layout3 = QHBoxLayout()
        self.horizon_left_layout4 = QHBoxLayout()

        self.setter = Setter(self._peripheral)
        self.getter = Getter(self.original1, self.original2, self.result1, self.result2, self.display1, self.display2)
        # print(self._address)
        self.setter.sinOut.connect(self.show_data)
        # self.thread.sinOut.connect(self.thread2.get)
        # self.thread2.sigOut.connect(self.slot_display)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slot_display)
        # self.plotter = Plotter(self.curveECG, self.ECG_data, self.display1, self.display2)

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
        # self.horizon_left_layout4.addWidget(self.SpO2)
        # self.horizon_left_layout4.addWidget(self.SpO2Win)

        # self.vertical_left_layout.addStretch(1)
        self.vertical_left_layout.addLayout(self.horizon_left_layout1)
        # self.vertical_left_layout.addStretch(1)
        self.vertical_left_layout.addLayout(self.horizon_left_layout2)
        # self.vertical_left_layout.addStretch(1)
        self.vertical_left_layout.addLayout(self.horizon_left_layout3)
        # self.vertical_left_layout.addStretch(1)
        # self.vertical_left_layout.addLayout(self.horizon_left_layout4)
        # self.vertical_left_layout.addStretch(1)

        # set right
        # self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.save)
        self.vertical_right_layout.addWidget(self.clear)
        self.vertical_right_layout.addWidget(self.receive)
        self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.exit)
        # self.vertical_right_layout.addStretch(1)

        # set layout
        # self.horizon_layout.addStretch(0)
        self.horizon_layout.addLayout(self.vertical_left_layout)
        # self.horizon_layout.addStretch(0)
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
        self.save.setFixedSize(240, 120)
        self.save.setFont(font_of_button)
        self.clear.setFixedSize(240, 120)
        self.clear.setFont(font_of_button)
        self.receive.setFixedSize(240, 120)
        self.receive.setFont(font_of_button)
        self.exit.setFixedSize(240, 120)
        self.exit.setFont(font_of_button)

        self.ECG.setText("心电")
        self.SpO2.setText("血氧")
        self.PulseWave.setText("脉搏")
        self.Respiration.setText("呼吸")
        self.save.setText("保存")
        self.clear.setText("清除")
        self.receive.setText("接收")
        self.exit.setText("返回")

        self.save.clicked.connect(self.slot_save)
        self.clear.clicked.connect(self.slot_clear)
        self.receive.clicked.connect(self.slot_receive)
        self.exit.clicked.connect(self.close_win)

    def slot_stop(self):

        """
        stop the thread's loop
        :return: none
        """

        self.thread.working = False

    def slot_receive(self):

        """
        the slot function to start notification receiving thread
        :return: none
        """

        self.setter.start()
        self.getter.start()
        self.timer.start(1)
        # self.plotter.start()

    def show_data(self, msg):

        """
        add the received notification to the textedit
        :param msg: the notification
        :return: none
        """

        message = msg
        # self.ECGWin.append(message)
        self.getter.get(message)
        # self.ECGWin.append(msg2)
        # self.ECGWin.append(msg3)

    def slot_clear(self):

        """
        clear the window
        :return: none
        """

        self.ECGWin.clear()
        # self.PulseWaveWin.removeItem()

    def slot_save(self):

        """
        save data
        :return: none
        """

        self.setter.working = False
        string = self.dataWin.toPlainText()
        file_log = open('./docs/output.txt', 'w')
        file_log.write(string)
        file_log.close()

    def slot_display(self):

        """
        display the data
        :return: none
        """

        # temp1 = message['res1']
        # temp2 = message['res2']

        # print(len(self.result2))
        # print(temp2[0])
        # length = len(temp2)
        ticks1 = time.time()
        size = self.display2.qsize()
        print(size)
        if size > 0:  # 6
            data1 = self.display2.get()
            # data2 = self.display2.get()
            # data3 = self.display2.get()
            # data4 = self.display2.get()
            # data5 = self.display2.get()
            # data6 = self.display2.get()
            length = len(data1)

            # the length of the data to be plot must be larger than 0, or the display window will be shorten into 9.
            if length > 0:
                # if self.display2.qsize() > 0:
                self.ECG_data[:-length] = self.ECG_data[length:]
                self.ECG_data[-length:] = data1
                # self.ECG_data[-5] = data2
                # self.ECG_data[-4] = data3
                # self.ECG_data[-3] = data4
                # self.ECG_data[-2] = data5
                # self.ECG_data[-1] = data6
                # print(length)

                self.ECG_pointer += length
                self.curveECG.setData(self.ECG_data)
                self.curveECG.setPos(self.ECG_pointer, 0)
        ticks2 = time.time()
        print(1000 * (ticks2 - ticks1))
        # self.result1.extend(temp1)
        # self.result2.extend(temp2)
        # self.original1.extend(message['ori1'])
        # self.original2.extend(message['ori2'])

        # for index in range(length):
        #     self.display1.put(temp1[index])
        #     self.display2.put(temp2[index])

    def close_win(self):

        """
        close the window
        :return: none
        """

        self.setter.working = False
        self.getter.working = False
        # self.plotter.working = False
        self.timer.stop()
        self.close()


class Setter(QThread):
    sinOut = pyqtSignal(str)
    peripheral = None

    def __init__(self, peripheral):
        super(Setter, self).__init__()
        self.working = True
        # self.address = address
        self.peripheral = peripheral

    def run(self):
        """
        the main task to be execute
        :return: none
        """
        # self.peripheral.connect(self.address)
        # self.peripheral.setDelegate(MyDelegate(self.sinOut))
        svc = self.peripheral.getServiceByUUID("f000fff0-0451-4000-b000-000000000000")
        ch = svc.getCharacteristics()[0]
        self.peripheral.writeCharacteristic(ch.valHandle + 1, struct.pack('<bb', 0x01, 0x00))
        # print("waiting...")
        # self.sinOut.emit("waiting...")

        while self.working:
            if self.peripheral.waitForNotifications(1.0):
                # print("notification:")
                continue


class Getter(QThread):
    sigOut = pyqtSignal(dict)
    working = True

    def __init__(self, original1, original2, final1, final2, display1, display2):
        super(Getter, self).__init__()
        self.ori1 = original1
        self.ori2 = original2
        self.final1 = final1
        self.final2 = final2
        self.display1 = display1
        self.display2 = display2
        self.q = Queue()
        self.split = Splitter()

    def get(self, msg):
        # print("get")
        self.q.put(msg)

    def run(self):
        while self.working:
            if self.q.qsize() >= 3:
                message = self.q.get()
                message += self.q.get()
                message += self.q.get()
                # print(self.display2.qsize())

                # original1 = []
                # original2 = []
                # res1 = []
                # res2 = []
                # ticks1 = time.time()
                self.split.process_string(message, self.ori1, self.ori2, self.final1,
                                          self.final2, self.display1, self.display2)
                # ticks2 = time.time()
                # print((ticks2 - ticks1) * 1000)
                # original1, original2, res1, res2 = self.split.ori1, self.split.ori2, self.split.res1, self.split.res2
                # if len(original1) < 0 or len(original2) < 0 or len(res1) < 0 or len(res2) < 0:
                #     continue
                # else:
                #     # print(res2[0])
                #     # message = {'ori1': original1,
                #     #            'ori2': original2,
                #     #            'res1': res1,
                #     #            'res2': res2}
                #     # self.sigOut.emit(message)
                #     self.ori1.extend(original1)
                #     self.ori2.extend(original2)
                #     self.final1.extend(res1)
                #     self.final2.extend(res2)
                #     self.display1.put(res1)
                #     self.display2.put(res2)
                #     # length = len(res2)
                #     # for index in range(length):
                #     #     self.display1.put(res1[index])
                #     #     self.display2.put(res2[index])


# Ignore it. This class is never used.
class Plotter(QThread):
    # sigOut = pyqtSignal(dict)
    working = True

    def __init__(self, curve, data, display1, display2):
        super(Plotter, self).__init__()
        self.display1 = display1
        self.display2 = display2
        self.curve = curve
        self.data = data
        self.pointer = 0
        # self.q = Queue()

    def run(self):
        while self.working:
            ticks1 = time.time()
            size = self.display2.qsize()
            print(size)
            if size > 0:  # 6
                signal = self.display2.get()
                length = len(signal)

                # the length of the data to be plot must be larger than 0, or the display window will be shorten into 9.
                if length > 0:
                    self.data[:-length] = self.data[length:]
                    self.data[-length:] = signal

                    self.pointer += length
                    self.curve.setData(self.data)
                    self.curve.setPos(self.pointer, 0)
            ticks2 = time.time()
            print(1000 * (ticks2 - ticks1))
