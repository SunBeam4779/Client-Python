import os
import struct
import time

import pymysql
from PyQt5.Qt import *
# from Client.Util import MyDelegate
from Client.Util import SignalProcess, Splitter, SplitterD
# from bluepy import btle
from queue import Queue
import pyqtgraph as pg
import numpy as np


class DataAcquire(QWidget):

    """
    receive the data through BLE
    """

    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 800
    _size_of_y = 600
    # _address = ""
    _peripheral = None
    user_unique = "not defined"
    data_type = "not defined"
    device_type = "not defined"
    channel1_type = "not defined"
    channel2_type = "not defined"
    start_time = "not defined"
    two_channel = False
    q = None
    result1 = []  # dec type
    result2 = []
    display1 = None  # dec type
    display2 = None
    original1 = []  # hex type
    original2 = []
    display_channel1 = [0 for i in range(500)]
    display_channel2 = [0 for j in range(500)]
    curve_channel1 = None
    curve_channel2 = None
    pointer_channel1 = 0
    pointer_channel2 = 0

    def __init__(self, peripheral, user_unique, data_type):
        super(DataAcquire, self).__init__()

        # self._address = address
        self._peripheral = peripheral
        self.user_unique = user_unique
        if data_type == "ECG01":  # if the device is the bought module
            self.data_type = "ECG"
            self.device_type = "BW"
        else:  # if the device is the module made by ourselves
            self.data_type = data_type

        # //-set ICON
        self.Icon = QIcon(self._icon)

        # //-queue
        self.q = Queue()
        self.display1 = Queue()
        self.display2 = Queue()

        # //-set choice
        self.ECG = QLabel()
        self.SpO2 = QLabel()
        self.Respiration = QLabel()
        self.PulseWave = QLabel()

        # //-set button
        self.save = QPushButton()
        self.clear = QPushButton()
        self.receive = QPushButton()
        self.exit = QPushButton()

        # //-set Text Edit
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

        # //-set data graph
        pg.setConfigOption('background', 'k')  # #f0f0f0
        pg.setConfigOption('foreground', 'w')
        pg.setConfigOptions(antialias=True)

        self.ECGWin = pg.GraphicsLayoutWidget(self)
        # self.SpO2Win = pg.GraphicsLayoutWidget(self)
        self.RespirationWin = pg.GraphicsLayoutWidget(self)
        self.PulseWaveWin = pg.GraphicsLayoutWidget(self)
        # self.ECGWin.setXRange(self, )

        self.pen = pg.mkPen(color='r', width=2)  # (200, 200, 255)
        self.ECGWinHandle = self.ECGWin.addPlot()
        # self.SpO2WinHandle = self.SpO2Win.addPlot()
        self.RespirationWinHandle = self.RespirationWin.addPlot()
        self.PulseWaveWinHandle = self.PulseWaveWin.addPlot()

        # self.curve_channel1, self.curve_channel2 = self.PulseWaveWinHandle.plot(self.display_channel2, pen=self.pen)
        self.type_determine()

        # //-set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_left_layout = QVBoxLayout()
        self.vertical_right_layout = QVBoxLayout()
        self.horizon_left_layout1 = QHBoxLayout()
        self.horizon_left_layout2 = QHBoxLayout()
        self.horizon_left_layout3 = QHBoxLayout()
        self.horizon_left_layout4 = QHBoxLayout()

        self.setter = Setter(self._peripheral, self.device_type)
        self.getter = Getter(self.original1, self.original2, self.result1, self.result2,
                             self.display1, self.display2, self.device_type)
        # print(self._address)
        self.setter.sinOut.connect(self.show_data)
        # self.thread.sinOut.connect(self.thread2.get)
        # self.thread2.sigOut.connect(self.slot_display)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slot_display)
        # self.plotter = Plotter(self.curveECG, self.ECG_data, self.display1, self.display2)

        # //-set ui
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

        # //-set left
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

        # //-set right
        # self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.save)
        self.vertical_right_layout.addWidget(self.clear)
        self.vertical_right_layout.addWidget(self.receive)
        self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.exit)
        # self.vertical_right_layout.addStretch(1)

        # //-set layout
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

        # //-label
        self.ECG.setFont(font_of_label)
        self.SpO2.setFont(font_of_label)
        self.PulseWave.setFont(font_of_label)
        self.Respiration.setFont(font_of_label)

        # //-button
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

    def type_determine(self):

        """
        determine the data type to be acquired by the device connected.
        if the type is ECG or ENR(means the ECG and Respiration), the channel1 should be ECG,
        the channel2 should be respiration or ECG.
        if the data type is pulse, there should be only one channel which is the channel 2.
        :return: None
        """

        if self.data_type == "ECG" or self.data_type == "ENR":
            self.curve_channel2 = self.ECGWinHandle.plot(self.display_channel2, pen=self.pen)
            self.curve_channel1 = self.RespirationWinHandle.plot(self.display_channel1, pen=self.pen)
            self.two_channel = True
            if self.data_type == "ECG":
                self.channel1_type = "RESP"
                self.channel2_type = "ECG"
            else:
                self.channel1_type = "RESP"
                self.channel1_type = "ECG"
        else:
            self.curve_channel2 = self.PulseWaveWinHandle.plot(self.display_channel2, pen=self.pen)
            self.curve_channel1 = None
            self.two_channel = False
            self.channel2_type = "PULSE"

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

        self.start_time = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))

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

        # //-stop the thread and timer
        self.setter.working = False
        self.getter.working = False
        self.timer.stop()

        # //-get the user info
        db = None
        try:
            db = pymysql.connect(host='localhost', user='root', password='root', db='user')
        except Exception as e:
            print("database connection wrong" + e.__str__())

        result = None
        try:
            cursor = db.cursor()
            sql = "select * from USERINFO where unique_id='%s';" % self.user_unique
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print("select data wrong" + e.__str__())
        result = result[0]
        username = result[0]
        name = result[2]

        # //-process data
        data_processor = SignalProcess()
        data_processor.setter(self.result2)
        data_processor.execute()

        # //-oriX means the data which not be remove the baseline
        # //-resultX means the data which be smoothed and removed the baseline
        # //-rawX means the data which not be filtered
        ori2, result2, heart_rate2 = data_processor.getter()
        # print(ori2.shape)
        # print(result2.shape)
        # print(type(result2))
        # print(type(self.result2))
        result2 = result2.reshape(len(result2), 1)
        ori2 = ori2.reshape(len(ori2), 1)
        raw2 = np.array(self.result2)
        # print(raw2.shape)
        raw2 = raw2.reshape(len(raw2), 1)

        if self.two_channel:
            data_processor.setter(self.result1)
            data_processor.execute()
            ori1, result1, heart_rate1 = data_processor.getter()

            result1 = result1.reshape(len(result1), 1)
            ori1 = ori1.reshape(len(ori1), 1)
            raw1 = np.array(self.result1)
            raw1 = raw1.reshape(len(raw1), 1)

            raw_data1 = os.path.join("./docs/data/", (name + self.user_unique + "/" + self.channel1_type +
                                                      "/original/raw_1_" + self.start_time + ".txt"))
            ori_data1 = os.path.join("./docs/data/", (name + self.user_unique + "/" + self.channel1_type +
                                                      "/filtered/filtered_1_" + self.start_time + ".txt"))
            final_data1 = os.path.join("./docs/data/", (name + self.user_unique + "/" + self.channel1_type +
                                                        "/filtered/final_1_" + self.start_time + ".txt"))
            np.savetxt(raw_data1, raw1[1000:-500])
            np.savetxt(ori_data1, ori1[1000:-500])
            np.savetxt(final_data1, result1[1000:-500])

            try:
                cursor = db.cursor()
                cursor.execute("insert into USERDATA(username, name, unique_id, data_number, date, "
                               "data_type, value, checkable, synchronized)"
                               "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %
                               (username, name, self.user_unique, "1" + self.start_time, self.start_time[:8],
                                self.channel1_type, final_data1, 'Yes', 'No'))
                db.commit()
            except Exception as e:
                print("wrong!" + e.__str__())

        raw_data2 = os.path.join("./docs/data/", (name + self.user_unique + "/" + self.channel2_type +
                                                  "/original/raw_2_" + self.start_time + ".txt"))
        ori_data2 = os.path.join("./docs/data/", (name + self.user_unique + "/" + self.channel2_type +
                                                  "/filtered/filtered_2_" + self.start_time + ".txt"))
        final_data2 = os.path.join("./docs/data/", (name + self.user_unique + "/" + self.channel2_type +
                                                    "/filtered/final_2_" + self.start_time + ".txt"))

        np.savetxt(raw_data2, raw2)
        np.savetxt(ori_data2, ori2)
        np.savetxt(final_data2, result2)

        try:
            cursor = db.cursor()
            cursor.execute("insert into USERDATA(username, name, unique_id, data_number, date, "
                           "data_type, value, checkable, synchronized)"
                           "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %
                           (username, name, self.user_unique, "2" + self.start_time, self.start_time[:8],
                            self.channel2_type, final_data2, 'Yes', 'No'))
            db.commit()
        except Exception as e:
            print("wrong!" + e.__str__())

        try:
            cursor = db.cursor()
            cursor.execute("insert into USERDATA(username, name, unique_id, data_number, date, "
                           "data_type, value, checkable, synchronized)"
                           "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %
                           (username, name, self.user_unique, "2" + self.start_time, self.start_time[:8],
                            "HR", heart_rate2, 'No', 'No'))
            db.commit()
        except Exception as e:
            print("wrong!" + e.__str__())

        QMessageBox.information(self, "数据保存成功！", "数据已保存！", QMessageBox.Ok)

    def slot_display(self):

        """
        display the data
        :return: none
        """

        if self.two_channel:
            # ticks1 = time.time()
            size = self.display2.qsize()
            # print(size)
            if size > 0:
                data1 = self.display1.get()
                data2 = self.display2.get()
                length = len(data1)

                # //-the length of the data to be plot must be larger than 0,
                # //-or the display window will be shorten into 9.
                if length > 0:
                    self.display_channel1[:-length] = self.display_channel1[length:]
                    self.display_channel1[-length:] = data1
                    self.display_channel2[:-length] = self.display_channel2[length:]
                    self.display_channel2[-length:] = data2
                    # print(length)

                    self.pointer_channel1 += length
                    self.curve_channel1.setData(self.display_channel1)
                    self.curve_channel1.setPos(self.pointer_channel1, 0)
                    self.pointer_channel2 += length
                    self.curve_channel2.setData(self.display_channel2)
                    self.curve_channel2.setPos(self.pointer_channel2, 0)
            # ticks2 = time.time()
            # print(1000 * (ticks2 - ticks1))
        else:
            # ticks1 = time.time()
            size = self.display2.qsize()
            # print(size)
            if size > 0:
                data1 = self.display2.get()
                length = len(data1)

                # //-the length of the data to be plot must be larger than 0,
                # //-or the display window will be shorten into 9.
                if length > 0:
                    self.display_channel2[:-length] = self.display_channel2[length:]
                    self.display_channel2[-length:] = data1
                    # print(length)

                    self.pointer_channel2 += length
                    self.curve_channel2.setData(self.display_channel2)
                    self.curve_channel2.setPos(self.pointer_channel2, 0)
            # ticks2 = time.time()
            # print(1000 * (ticks2 - ticks1))

    def close_win(self):

        """
        close the window
        :return: none
        """

        self.setter.working = False
        self.getter.working = False
        # self.plotter.working = False
        self.timer.stop()
        self.display_channel1 = [0 for _ in range(500)]
        self.display_channel2 = [0 for _ in range(500)]
        self.ECGWinHandle.plot(self.display_channel2, pen=self.pen)
        self.RespirationWinHandle.plot(self.display_channel1, pen=self.pen)
        self.PulseWaveWinHandle.plot(self.display_channel2, pen=self.pen)
        self.close()


class Setter(QThread):
    """
    to get the bluetooth characteristics, send them as a signal to another thread.
    """

    sinOut = pyqtSignal(str)
    peripheral = None
    _type = None

    def __init__(self, peripheral, types):
        super(Setter, self).__init__()
        self.working = True
        # self.address = address
        self.peripheral = peripheral
        self._type = types

    def run(self):
        """
        the main task to be execute, to start the BLE notification receiving.
        send the received notification as signal to Getter thread.
        the sending affair would be handled by the MyDelegate().
        :return: none
        """

        # self.peripheral.connect(self.address)

        # //-set the delegate to handle notification message process
        # self.peripheral.setDelegate(MyDelegate(self.sinOut))
        if self._type == "BW":
            uuid = "0000fff0-0000-1000-8000-00805f9b34fb"  # the bought module distinguished by the name.
            # BW means the bought module's name "BW-ECG-01".
            svc = self.peripheral.getServiceByUUID(uuid)

            # //-the characteristic that data can be written to
            chr_of_writable = svc.getCharacteristics()[0]
            # //-the characteristic that receives notification from other peripheral.
            chr_of_notify = svc.getCharacteristics()[1]
            # //-enable the notify
            self.peripheral.writeCharacteristic(chr_of_notify.valHandle + 1, struct.pack('<bb', 0x01, 0x00), True)
            # //-bind user ID to BW-ECG-01, the ID could be a random ID.
            chr_of_writable.write(b'\xE8\x41\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                                  True)
            # //-start the acquiring, a time(Y/M/D/H/H/S/deltaT) should be given. the time could be a random time
            # //-but the delta T should have meaning which is the acquiring time. 0x01 means 1 minutes.
            # //-the delta T could be modified as other number, this could be done by UI.
            # //-if the number could be set by user, that will be perfection.
            chr_of_writable.write(b'\xE8\x23\x15\x03\x0b\x10\x15\x00\x00\x01', True)
            # //-start continually acquiring
            chr_of_writable.write(b'\xE8\20', True)

            while self.working:
                if self.peripheral.waitForNotifications(1.0):
                    # print("notification:")
                    continue
        else:
            uuid = "f000fff0-0451-4000-b000-000000000000"  # the module made by ourselves
            svc = self.peripheral.getServiceByUUID(uuid)
            ch = svc.getCharacteristics()[0]
            self.peripheral.writeCharacteristic(ch.valHandle + 1, struct.pack('<bb', 0x01, 0x00))
            # print("waiting...")
            # self.sinOut.emit("waiting...")

            while self.working:
                if self.peripheral.waitForNotifications(1.0):
                    # print("notification:")
                    continue


class Getter(QThread):
    """
    get the bluetooth data from the signal, put them into the queue and do some preprocess.
    """

    sigOut = pyqtSignal(dict)
    working = True
    _device_type = None

    def __init__(self, original1, original2, final1, final2, display1, display2, types):
        super(Getter, self).__init__()
        self.ori1 = original1
        self.ori2 = original2
        self.final1 = final1
        self.final2 = final2
        self.display1 = display1
        self.display2 = display2
        self.q = Queue()
        if types == "BW":
            self.split = SplitterD()
        else:
            self.split = Splitter()
        self._device_type = types

    def get(self, msg):

        """
        put the data into queue
        :param msg:
        :return: none
        """

        # print("get")
        self.q.put(msg)

    def run(self):

        """
        process the data which is the string type to get the essential content.
        :return:
        """

        if self._device_type == "BW":
            while self.working:
                if self.q.qsize() >= 1:
                    message = self.q.get()
                    print(self.q.qsize())

                    # //-process the data use Util.SplitterD
                    self.split.process_string(message, self.ori1, self.ori2, self.final1,
                                              self.final2, self.display1, self.display2)
        else:
            while self.working:
                if self.q.qsize() >= 3:
                    message = self.q.get()
                    message += self.q.get()
                    message += self.q.get()
                    print(self.q.qsize())

                    # original1 = []
                    # original2 = []
                    # res1 = []
                    # res2 = []
                    # ticks1 = time.time()

                    # //-process the data use Util.Splitter
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


# //-Ignore it. This class is never used.
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

                # //-the length of the data to be plot must be larger than 0,
                # //-or the display window will be shorten into 9.
                if length > 0:
                    self.data[:-length] = self.data[length:]
                    self.data[-length:] = signal

                    self.pointer += length
                    self.curve.setData(self.data)
                    self.curve.setPos(self.pointer, 0)
            ticks2 = time.time()
            print(1000 * (ticks2 - ticks1))
