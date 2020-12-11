import array
import math

# from bluepy import btle
import re
# from binascii import b2a_hex
import struct
from datetime import datetime, timedelta

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from scipy.signal import butter, firwin, ellipord, ellip, sosfilt, savgol_filter
import socket
import threading


# class MyDelegate(btle.DefaultDelegate):
#
#     """
#     handle the notification from the BLE device
#     """
#
#     def __init__(self, signal):
#         btle.DefaultDelegate.__init__(self)
#         self.signal = signal
#         # self.q = Queue()
#         # self.start = True
#         self.count = 0
#
#     def handleNotification(self, cHandle, data):
#
#         """
#         sending the data as a signal to the data acquiring window
#         :param cHandle: ignore it
#         :param data: the notification
#         :return: none
#         """
#
#         if self.count < 3:
#             self.count += 1
#             pass
#         else:
#             msg = str(b2a_hex(data))[2:-1]
#             # self.q.put(msg)
#             self.signal.emit(msg)
#             # if self.q.qsize() > 6:
#             #     res = [self.q.get(), self.q.get(), self.q.get()]
#             #     self.signal[str, str, str].emit(res[0], res[1], res[2])
#         # print("Received data:")


class Splitter:

    """
    handle the BLE string-type data splitting.
    """

    ori1 = []
    ori2 = []
    res1 = []
    res2 = []

    @staticmethod
    def process_string(message, ori1, ori2, res1, res2, display1, display2):

        """
        process the string of BLE data, to get the essential message.
        :param display2: a queue which contains the to-be-displayed data of channel2. Passed by the caller
        :param display1: a queue which contains the to-be-displayed data of channel1. Passed by the caller
        :param res2: a list which contains the final data preprocessing result of channel2. Passed by the caller
        :param res1: a list which contains the final data preprocessing result of channel1. Passed by the caller
        :param ori2: a list which contains the original raw data of channel2. Passed by the caller
        :param ori1: a list which contains the original raw data of channel1. Passed by the caller
        :param message: raw data to be preprocessed
        :return: none
        """

        # count = 0
        # data = ""
        # length = 6
        target = 72
        # head = 0
        # items = ""

        # for i in range(length):
        # message = messages.get()
        # count += 1
        # cut_head = message.split(":")[-1]
        # lower = cut_head.lower()
        # essence = lower.split("\"")[1]
        # string = "".join(essence)
        # data += string
        data1 = re.split("c0c0", message)
        item = "".join(data1[1:-1])
        if len(data1[0]) == len(data1[-1]) == 10:
            data1[0] = data1[0][2:]
            data1[-1] = data1[-1][:-2]
            item1 = data1[0] + item
            item = item1 + data1[-1]
            target = 80
        # data = item.split(" ")
        # data = "".join(data)
        # data = data.split(" ")
        # data = "".join(data)
        if len(item) == target:
            # Splitter.ori1, Splitter.ori2, Splitter.res1, Splitter.res2 = Splitter.switch_form(item)
            Splitter.switch_form(item, ori1, ori2, res1, res2, display1, display2)
            # print(Splitter.res2[0])
            # return ori1, ori2, ans1, ans2
            # data = ""

    @staticmethod
    def two_complement(value, bits):

        """
        handle the two's complement data
        :param value: value to be transformed
        :param bits: the bit width of the value
        :return: processed result
        """

        if value >= 2 ** bits:
            raise ValueError("Value: {} out of range of {}-bit value.".format(value, bits))
        else:
            return value - int((value << 1) & 2 ** bits)

    @staticmethod
    def get_dec(channel1, channel2):

        """
        switch from hex to dec
        :param channel1: value of data from channel1
        :param channel2: value of data from channel2
        :return: decimal result
        """

        res = int(channel1, 16)
        bits_width = 24
        r_e1 = Splitter.two_complement(res, bits_width)

        res = int(channel2, 16)
        bits_width = 24
        r_e2 = Splitter.two_complement(res, bits_width)
        return r_e1, r_e2

    @staticmethod
    def switch_form(string, original_channel1, original_channel2, final1, final2, display1, display2):

        """
        get the original data and final result of two channels
        :param display2: a queue which contains the to-be-displayed data of channel2. Passed by the caller
        :param display1: a queue which contains the to-be-displayed data of channel1. Passed by the caller
        :param final2: a list which contains the final data preprocessing result of channel2. Passed by the caller
        :param final1: a list which contains the final data preprocessing result of channel1. Passed by the caller
        :param original_channel2: a list which contains the original raw data of channel2. Passed by the caller
        :param original_channel1: a list which contains the original raw data of channel1. Passed by the caller
        :param string: the data of string type to be cut into two channels
        :return: processed result
        """

        # original_channel1 = []
        # original_channel2 = []
        plot1 = []
        plot2 = []
        length = len(string)
        i = 0
        while i < length:
            result1 = '0x'
            result1 = result1 + string[i:i + 4]
            # result1 = result1 + ''.join(string[i + 1])
            # result1 = result1 + ''.join(string[i + 2])
            # result1 = result1 + ''.join(string[i + 3])
            result1 = result1 + "00"

            result2 = '0x'
            result2 = result2 + string[i + 4:i + 8]
            # result2 = result2 + ''.join(string[i + 5])
            # result2 = result2 + ''.join(string[i + 6])
            # result2 = result2 + ''.join(string[i + 7])
            result2 = result2 + "00"

            i += 8

            original_channel1.append(result1)
            original_channel2.append(result2)
            value1, value2 = Splitter.get_dec(result1, result2)
            final1.append(value1)
            final2.append(value2)
            plot1.append(value1)
            plot2.append(value2)

        display1.put(plot1)
        display2.put(plot2)
        # print(result1)
        # print(result2)
        # return original_channel1, original_channel2, final1, final2


class RoundProgress(QWidget):

    """
    draw the circle, when something is not getting done.
    """

    def __init__(self):
        super(RoundProgress, self).__init__()
        self.pen = QPen()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # set transparent
        self.center()
        self.percent = 0
        self.my_thread = Counter()
        self.my_thread.my_signal.connect(self.parameter_update)
        self.my_thread.start()

    def center(self):

        """
        move the circle to the central position
        :return: none
        """

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def parameter_update(self, p):

        """
        update the circle percent
        :param p: percent
        :return: none
        """

        self.percent = p

    def paintEvent(self, event):

        """
        handle the drawing event, to draw the circle
        :param event: drawing event
        :return: none
        """

        rotate_angle = int(360 * self.percent / 100)
        painter = QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)

        gradient = QConicalGradient(50, 50, 91)
        gradient.setColorAt(0, QColor("#95BBFF"))
        gradient.setColorAt(1, QColor("#5C86FF"))
        self.pen.setBrush(gradient)
        self.pen.setWidth(10)
        self.pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.pen)
        painter.drawArc(QtCore.QRectF(25, 25, 58, 58), (90 - 0) * 16, -rotate_angle * 16)  # draw the circle
        self.update()


class Counter(QThread):

    """
    a thread to update the circle percent
    """

    my_signal = pyqtSignal(int)
    p = 0

    def __init__(self):
        super(Counter, self).__init__()

    def run(self):
        while self.p < 100:
            self.p += 1
            self.my_signal.emit(self.p)
            self.msleep(10)
            if self.p == 100:
                self.p = 0
                self.my_signal.emit(self.p)
                self.msleep(10)


class SignalProcess:

    """
    the signal processing class
    """

    def __init__(self):
        self.order = 4
        self.fs = 2000  # sample rate, Hz
        # //-desired cutoff frequency of the filter, Get the filter coefficients so we can check its frequency response.
        self.cutoff = 50  # Hz
        self.data_ = []
        self.raw = []
        self.baseline = []
        self.final_data = []

    def _butter_low_pass(self):

        """
        generate the low pass filter(this should not be use directly)
        :return: the parameter of filter
        """

        nyq = 0.5 * self.fs
        normal_cutoff1 = 180 / nyq
        normal_cutoff = 0.1 / nyq
        # window = get_window('hann', 512)
        sos = butter(self.order, [normal_cutoff, normal_cutoff1], btype='band', output='sos')
        # a, b = butter(order_, normal_cutoff1, btype='low')
        h_ = firwin(512, normal_cutoff, window='hamming', pass_zero='lowpass')
        return sos, h_
        # return a, b, h_

    def _butter_low_pass_filter(self):

        """
        execute the filtering(this should not be use directly)
        :return: the result after filtering
        """

        sos, h_ = self._butter_low_pass()
        # first, second, h_ = butter_low_pass(cutoff_, fs_, order_)
        res = sosfilt(sos, self.data_)
        # res = filtfilt(first, second, data_)
        # res2 = filtfilt(h_, 1, self.data_)
        return res  # Filter requirements.

    def _base_line(self):

        """
        remove the baseline(this should not be use directly)
        :return: the data without baseline
        """

        if len(self.raw) != 0:
            wp = 1.5 * 2 / 512
            ws_ = 0.2 * 2 / 512
            devel = 0.005
            rp = 20 * math.log10((1 + devel) / (1 - devel))
            rs = 20
            n, wn = ellipord(wp, ws_, rp, rs, True)
            sos = ellip(n, rp, rs, wn, 'high', output='sos')
            res = sosfilt(sos, self.raw)
            return res
        else:
            return []

    def _smooth(self):

        """
        smooth the data(this should not be use directly)
        :return: smooth data
        """

        if len(self.baseline) != 0:
            return savgol_filter(self.baseline, 11, 3)
        else:
            return []

    def setter(self, data):

        """
        input the data to be processed
        :param data: the target data
        :return: none
        """

        self.data_ = data

    def execute(self):

        """
        the signal process executor.
        if you want to process the signal you should only use this function
        :return:
        """

        self.raw = self._butter_low_pass_filter()
        self.baseline = self._base_line()
        self.final_data = self._smooth()

    def getter(self):

        """
        get the final result
        :return: processed signal
        """

        return self.raw, self.final_data


class Caller:

    """
    handle the socket communication with remote server
    """

    # signal = pyqtSignal(int)
    _tcp_socket = None
    _server_address = None
    _server_port = None
    _message1 = None
    _message2 = None
    _receive = None

    def __init__(self, address, port):
        # super(Caller, self).__init__()
        self._server_address = address
        self._server_port = port
        self.client_thread = None
        # self.receive = None

    def setter(self, message1, message2):
        """
        set the header and body to be sent
        :param message1: the header
        :param message2: the body
        :return: none
        """
        self._message1 = message1
        self._message2 = message2
        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def getter(self):

        """
        get the feedback from server
        :return: the feedback
        """

        return self._receive

    def save(self, info):

        """
        save the feedback from server
        :param info: the feedback from server
        :return: none
        """

        self._receive = info

    def client_send(self):

        """
        handle the client sending task and start the thread
        :return: none
        """

        address = (self._server_address, self._server_port)
        try:
            self._tcp_socket.connect(address)
        except Exception as ret:
            # self.signal.emit(ret.__str__())
            print("wrong" + ret.__str__())
        else:
            self.client_thread = threading.Thread(target=self.tcp_client_send_concurrency)
            self.client_thread.start()
            self.client_thread.join()

    def tcp_client_send_concurrency(self):

        """
        the client sending sub thread
        :return: none
        """

        self._tcp_socket.send(self._message1)  # //-send the header

        # //- if it's time check, the message2 should be ""
        if self._message2 != "":
            self._tcp_socket.send(self._message2)

        # //-get the feedback from server
        receive_msg = self._tcp_socket.recv(1024)

        # //-store the feedback
        self.save(receive_msg)

        self._tcp_socket.close()

    def client_receive(self):

        """
        handle the diagnosis log from server(not be used right now)
        :return: none
        """

        address = (self._server_address, self._server_port)
        try:
            self._tcp_socket.connect(address)
        except Exception as ret:
            # self.signal.emit(ret.__str__())
            print(ret.__str__())
        else:
            self.client_thread = threading.Thread(target=self.tcp_client_receive_concurrency)
            self.client_thread.start()

    def tcp_client_receive_concurrency(self):

        """
        the client receiving sub thread
        :return:
        """

        while True:
            self._receive = self._tcp_socket.recv(1024)
            if self._receive:
                self._tcp_socket.send(self._message1)

            self._tcp_socket.close()


class Type:
    """
    get the Chinese name
    """
    _type = {'ECG': "心电",
             'RESP': "呼吸",
             'PULSE': "脉搏",
             'HR': "心率",
             'RESPR': "呼吸率",
             'SPO2': "血氧",
             'BP': "血压"}

    @staticmethod
    def get_type(type_):
        """
        get the Chinese name of the type
        :param type_: data type
        :return: the Chinese name of it
        """
        return Type._type[type_]


class TimeSwitcher:

    """
    a utility to switch ColeDatetime into datetime(Python), or switch from datetime to ColeDatetime(MFC).
    """

    @staticmethod
    def ColeDatetime_to_datetime(date_val):

        """
        switch from ColeDatetime to datetime
        :param date_val: date-and-time value in ColeDatetime type
        :return: value in datetime(Python) type
        """

        base_date = datetime(year=1899, month=12, day=30, hour=0, minute=0, second=0)
        parts = math.modf(date_val)
        days = timedelta(parts[1])
        days_second = timedelta(abs(parts[0]))
        return base_date + days + days_second

    @staticmethod
    def datetime_to_ColeDatetime(date_val):

        """
        switch from datetime to ColeDatetime
        :param date_val: date-and-time value in datetime(Python) type
        :return: value in ColeDatetime type
        """

        base_date = datetime(year=1899, month=12, day=30, hour=0, minute=0, second=0)
        dist = date_val - base_date
        # right_now = base_date + dist
        # print(dist)
        # print(repr(dist))
        # print(dist.days)
        # print(dist.seconds)
        # print(dist.microseconds)
        seconds = dist.seconds + dist.microseconds / 1000000
        result = dist.days + seconds / 3600 / 24
        return result


class Encoding:

    """
    handle the code of header type
    """

    _coding = {
        'data': 0x1111,
        'connect': 0x2211,
        'diagnosis': 0x2222,
        'time_check': 0x2233,
        'request': 0x3311,
        'correct': 0x3322,
        'wrong': 0x3333,
        'userinfo': 0x4411,
        'reqnon': 0x5511
    }

    @staticmethod
    def encode(message):
        """
        return the code of the given type of header
        :param message: the type of header
        :return: the code
        """
        return Encoding._coding[message]


class BCCCRC:

    """
    handle the CRC calculation
    """

    @staticmethod
    def calc(value):

        """
        calculate the result of CRC
        :param value: the data content
        :return: the result of CRC
        """

        result = 0
        temp = array.array('B', value)
        for item in temp:
            # print(type(item))
            result ^= item
        return result
