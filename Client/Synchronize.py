import os
import time
from _datetime import datetime
import struct

import pymysql
from PyQt5.Qt import *
from Client.Util import Caller, TimeSwitcher, Encoding, BCCCRC
from Client.LogReader import LogReader
import numpy as np


class Synchronize(QWidget):

    """
    handle the data, information or time synchronizing
    """

    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 600
    _size_of_y = 500
    _data_path = "not defined"
    _data_type = "not defined"
    _data_time = "not defined"
    _item_row = None
    _ip_address = "not defined"
    _ip_port = "not defined"
    _received = None

    def __init__(self, unique_id, ip_address, ip_port):
        super(Synchronize, self).__init__()

        self.user_unique = unique_id
        self._ip_address = ip_address
        self._ip_port = ip_port
        self.items = self.to_be_synchronized()
        self.check_data_win = None

        # set Icon
        self.Icon = QIcon(self._icon)

        # set Button
        self.data_sync = QPushButton()
        self.time_sync = QPushButton()
        self.user_sync = QPushButton()
        self.diagnosis_request = QPushButton()
        self.exit = QPushButton()

        # set table container
        font_of_table = QFont()
        font_of_table.setFamily("Times")
        font_of_table.setPixelSize(35)

        self.table = QTableWidget()
        self.table.setFont(font_of_table)
        # self.table.setFixedSize(500, 450)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['姓名', '身份编号', '数据类型', '数据编号', '同步状态'])
        self.table.setShowGrid(False)
        self.table.setColumnWidth(0, 210)
        self.table.setColumnWidth(1, 400)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 400)
        self.table.setColumnWidth(4, 300)
        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # # fake item
        # check_item = QRadioButton()
        # check_item.setFont(font_of_table)
        # check_item.setText("20201020140521")
        # self.table.setCellWidget(0, 0, check_item)
        self.table.clicked.connect(self.select_item)
        self.set_table()

        # set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_right_layout = QVBoxLayout()

        # set ui
        self.set_ui()
        self.set_button()

    def set_ui(self):

        self.setLayout(self.horizon_layout)
        self.setWindowTitle("Data Synchronize")
        self.setWindowIcon(self.Icon)
        self.setWindowState(Qt.WindowMaximized)
        # self.resize(self._size_of_x, self._size_of_y)

        # set right layout
        # self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.data_sync)
        # self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.time_sync)
        # self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.user_sync)
        self.vertical_right_layout.addWidget(self.diagnosis_request)
        self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.exit)

        # set layout
        self.horizon_layout.addWidget(self.table)
        # self.horizon_layout.addStretch(0)
        self.horizon_layout.addLayout(self.vertical_right_layout)

    def set_button(self):

        font = QFont()
        font.setFamily("Times")
        font.setPixelSize(50)

        # set font
        self.data_sync.setFont(font)
        self.time_sync.setFont(font)
        self.user_sync.setFont(font)
        self.diagnosis_request.setFont(font)
        self.exit.setFont(font)

        self.data_sync.setFixedSize(300, 150)
        self.time_sync.setFixedSize(300, 150)
        self.user_sync.setFixedSize(300, 150)
        self.diagnosis_request.setFixedSize(300, 150)
        self.exit.setFixedSize(300, 150)

        # set text
        self.data_sync.setText("数据同步")
        self.time_sync.setText("时间同步")
        self.user_sync.setText("用户同步")
        self.diagnosis_request.setText("诊断报告")
        self.exit.setText("退出")

        self.user_sync.clicked.connect(self.slot_user_sync)
        self.time_sync.clicked.connect(self.slot_time_sync)
        self.data_sync.clicked.connect(self.slot_data_sync)
        self.diagnosis_request.clicked.connect(self.slot_diagnosis)
        self.exit.clicked.connect(self.closeWin)

    def set_table(self):

        """
        display the data to be synchronized
        :return: none
        """

        row = len(self.items)

        font_of_table = QFont()
        font_of_table.setFamily("Times")
        font_of_table.setPixelSize(30)

        self.table.setRowCount(row)
        # self.table.setHorizontalHeaderLabels(['姓名', '数据编号', '数据类型', '数值', '可查看'])

        # display item
        index = 0
        for item in self.items:
            check_item = QRadioButton()
            check_item.setFont(font_of_table)
            check_item.setText(item[1])  # name
            item_time = QTableWidgetItem(item[3])  # data number
            item_id = QTableWidgetItem(item[2])  # unique id
            item_type = QTableWidgetItem(item[5])  # data type
            # item_value = QTableWidgetItem(item[6])  # value or path
            item_checkable = QTableWidgetItem(item[7])  # checkable
            self.table.setCellWidget(index, 0, check_item)
            self.table.setItem(index, 1, item_id)
            self.table.setItem(index, 2, item_type)
            self.table.setItem(index, 3, item_time)
            self.table.setItem(index, 4, item_checkable)
            index += 1

    def select_item(self):

        """
        handle the click on the data should be sent.
        :return: none
        """

        row_index = self.table.currentIndex().row()
        self._item_row = row_index
        self._data_path = self.items[row_index][6]  # path
        self._data_type = self.items[row_index][5]  # type
        self._data_time = self.items[row_index][3]  # get time
        # print(self._data_time)

    def to_be_synchronized(self):

        """
        get those data which not be synchronized.
        :return: those data
        """

        if self.user_unique == "not defined":
            return []
        db = pymysql.connect(host='localhost', user='root', password='root', db='user')
        # cursor = db.cursor()
        try:
            db = pymysql.connect(host='localhost', user='root', password='root', db='user')
            # cursor = db.cursor()
        except Exception as e:
            print("database connection wrong" + e.__str__())

        result = None
        try:
            sql = "select * from userdata where(unique_id=%s and synchronized='No');" % self.user_unique
            cursor = db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print("get non-synchronized data fail" + e.__str__())

        db.close()

        return result

    def slot_time_sync(self):

        """
        request the time checking
        :return: none
        """

        # //-get the time of right now
        now = TimeSwitcher.datetime_to_ColeDatetime(datetime.now())
        print("%13f", now)
        value = float('%.12f' % now)
        print(value)
        another = TimeSwitcher.ColeDatetime_to_datetime(now)
        print(another)

        # //-set the header of time check
        message = Encoding.encode('time_check')
        ecc = 1
        length = struct.calcsize("idhh")
        print(length)
        head = struct.pack("<id4h", message, now, 0, 0, length, ecc)  # Those two 0s are placeholder token

        # //-send header
        caller = Caller(self._ip_address, int(self._ip_port))
        # caller.signal.connect(self.slot_getter)
        caller.setter(head, "")
        caller.client_send()
        receive1, receive2 = caller.getter()
        # print(receive)
        first, second, third, fourth, fifth, six = struct.unpack("<id4h", receive1)
        if first == 8755:
            new_time = TimeSwitcher.ColeDatetime_to_datetime(second)
            # //-the time fixing function should be placed here
            QMessageBox.information(self, '校时成功！', new_time.__str__(), QMessageBox.Ok)
        else:
            QMessageBox.information(self, '错误！', '请重新发送请求！', QMessageBox.Ok)

    def slot_user_sync(self):

        """
        send the user information to server
        :return: none
        """

        if self.user_unique == "not defined":
            return

        # //-get user information
        db = None
        try:
            db = pymysql.connect(host='localhost', user='root', password='root', db='user')
        except Exception as e:
            print("database connection wrong" + e.__str__())

        result = None
        try:
            sql = "select * from userinfo where unique_id=%s;" % self.user_unique
            cursor = db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print("get non-synchronized data fail" + e.__str__())

        db.close()

        # //-set the header and body of the information to to sent.
        result = result[0]
        enter_date = result[12]
        enter_time = TimeSwitcher.datetime_to_ColeDatetime(
            datetime(year=int(enter_date[0:4]), month=int(enter_date[4:6]), day=int(enter_date[6:])))

        birth = result[3][-12:-4]
        print(birth)
        birth_day = TimeSwitcher.datetime_to_ColeDatetime(
            datetime(year=int(birth[0:4]), month=int(birth[4:6]), day=int(birth[6:])))
        # gender = None
        if result[4] == "male":
            gender = 1
        else:
            gender = 0
        print(gender)

        userinfo = struct.pack("<ii40s20s20s40s40s40s200s400sd2hd2h",
                               int(self.user_unique),  # //-user id
                               gender,  # //-gender
                               bytearray(result[2], encoding='utf-16'),  # //-name
                               bytearray(result[9], encoding='utf-16'),  # //-height
                               bytearray(result[10], encoding='utf-16'),  # //-weight
                               bytearray(result[3], encoding='utf-16'),  # //-identity id
                               bytearray(result[7], encoding='utf-16'),  # //-phone
                               bytearray(result[8], encoding='utf-16'),  # //-cellphone
                               bytearray(result[6], encoding='utf-16'),  # //-address
                               bytearray(result[11], encoding='utf-16'),  # //-note
                               birth_day, 0, 0,
                               enter_time, 0, 0)
        length = struct.calcsize("idhh")
        ecc = BCCCRC.calc(userinfo)
        message = Encoding.encode('userinfo')
        time_now = TimeSwitcher.datetime_to_ColeDatetime(datetime.now())
        head = struct.pack("<id4h", message, time_now, 0, 0, length, ecc)

        # //-send header and body of data
        caller = Caller(self._ip_address, int(self._ip_port))
        caller.setter(head, userinfo)
        caller.client_send()
        receive1, receive2 = caller.getter()
        first, second, third, fourth, fifth, six = struct.unpack("<id4h", receive1)
        # print(first)
        if first == 13090:  # //- data was sent without mistake
            QMessageBox.information(self, '成功！', '用户信息已由工作站保存！', QMessageBox.Ok)
        if first == 13107:  # //- the data sent was not received correctly
            QMessageBox.information(self, '错误！', '校验码出错，请重新发送！', QMessageBox.Ok)

    def slot_data_sync(self):

        """
        data synchronizing
        :return: None
        """

        if self._data_path == "not defined":
            return

        # //-set the default value
        bp = [0, 0]
        bp_map = 0
        bp_pr = 0
        spo2 = 0
        ecg_channel_1 = [0.0 for _ in range(8192)]
        ecg_channel_2 = [0.0 for _ in range(8192)]
        respiration = [0.0 for _ in range(8192)]
        heart_rate = 0.0
        glu_data = 0.0
        temp_of_body = 0.0

        # //-set the data value according to the chosen data
        if self._data_type == "ECG":
            data = np.loadtxt(self._data_path)
            temp = data.reshape(1, len(data))
            signal = temp.tolist()
            ecg_channel_1 = list.copy(signal[0][:8192])
        elif self._data_type == "RESP":
            data = np.loadtxt(self._data_path)
            temp = data.reshape(1, len(data))
            signal = temp.tolist()
            respiration = list.copy(signal[0][:8192])
        elif self._data_type == "PULSE":
            data = np.loadtxt(self._data_path)
            temp = data.reshape(1, len(data))
            signal = temp.tolist()
            ecg_channel_2 = list.copy(signal[0][:8192])
        elif self._data_type == "HR":
            heart_rate = float(self._data_path)  # //-The value of heart rate and spo2 was transformed into float type,
        elif self._data_type == "SPO2":          # //-I have no idea why our sister use float type to store these
            spo2 = float(self._data_path)        # //-data. (=。=)...

        # //-set the header and body of the information to to sent.
        message = Encoding.encode('data')
        length = struct.calcsize("idhh")
        time_now = TimeSwitcher.datetime_to_ColeDatetime(datetime.now())
        if self._data_type == "PULSE" or self._data_type == "ECG" or self._data_type == "RESP":
            time_of_data = self._data_time[1:]
        else:
            time_of_data = self._data_time
        year = int(time_of_data[0:4])
        month = int(time_of_data[4:6])
        day = int(time_of_data[6:8])
        hour = int(time_of_data[8:10])
        minute = int(time_of_data[10:12])
        second = int(time_of_data[12:])
        acquire_time = TimeSwitcher.datetime_to_ColeDatetime(
            datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second))
        phy = struct.pack("<i2iiii%sf%sf%sffffd2h" % (len(ecg_channel_1), len(ecg_channel_2), len(respiration)),
                          int(self.user_unique),
                          *bp,
                          bp_map,
                          bp_pr,
                          spo2,
                          *ecg_channel_1,
                          *ecg_channel_2,
                          *respiration,
                          heart_rate,
                          glu_data,
                          temp_of_body,
                          acquire_time, 0, 0)
        ecc = BCCCRC.calc(phy)

        head = struct.pack("<id4h", message, time_now, 0, 0, length, ecc)

        # //-send header and body of data
        caller = Caller(self._ip_address, int(self._ip_port))
        caller.setter(head, phy)
        caller.client_send()
        receive1, receive2 = caller.getter()
        # print(receive)
        first, second, third, fourth, fifth, six = struct.unpack("<id4h", receive1)
        if first == 13090:  # //- data was sent without mistake
            # //-update the data showing table and the content in database
            db = None
            try:
                db = pymysql.connect(host='localhost', user='root', password='root', db='user')
            except Exception as e:
                print("database connection wrong" + e.__str__())

            try:
                sql = "update userdata set synchronized='Yes' " \
                      "where(unique_id=%s and data_number=%s and data_type='%s');"\
                      % (self.user_unique, self._data_time, self._data_type)
                cursor = db.cursor()
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                print("update data fail" + e.__str__())
            db.close()
            # //-update the table and data to be shown
            self.items = self.to_be_synchronized()
            self.set_table()
            QMessageBox.information(self, '成功！', '数据已由工作站保存！', QMessageBox.Ok)
        if first == 13107:
            QMessageBox.information(self, '错误！', '校验码出错，请重新发送！', QMessageBox.Ok)

    def slot_diagnosis(self):

        """
        sent the diagnosis request to server
        :return: none
        """

        # //-get the time of right now
        now = TimeSwitcher.datetime_to_ColeDatetime(datetime.now())
        # //-set the header of time check
        message = Encoding.encode('diagnosis')
        ecc = 1
        length = struct.calcsize("idhh")
        print(length)
        head = struct.pack("<id4h", message, now, 0, 0, length, ecc)  # Those two 0s are placeholder token

        # //- the code below should be remove, and place the diagnosis receiving code here.
        # //- the code here is just a fake diagnosis generator.
        # //- the Caller code should be uncomment if you wanna add the diagnosis receiving code.
        # //-send header
        caller = Caller(self._ip_address, int(self._ip_port))
        caller.setter(head, "")
        caller.client_send()
        receive1, receive2 = caller.getter()
        # print(receive)

        first, second, third, fourth, fifth, six = struct.unpack("<id4h", receive1)
        if first == 8738:

            db = None
            try:
                db = pymysql.connect(host='localhost', user='root', password='root', db='user')
            except Exception as e:
                print("database connection wrong" + e.__str__())

            result = None
            try:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM USERINFO WHERE unique_id='%s';" % self.user_unique)
                result = cursor.fetchall()
                # print(type(result))
                # print(len(result[0]))
            except Exception as e:
                print("login" + e.__str__())

            username = result[0][0]
            name = result[0][2]
            file_number = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
            date = file_number[:8]
            log_path = os.path.join("./docs/data/", (name + self.user_unique + "/LOG/diag" + file_number + ".txt"))
            file = open(log_path, 'a+')
            diagnosis = struct.unpack("=%ds" % len(receive2), receive2)
            file.write(str(diagnosis[0], encoding="gbk"))
            file.close()
            try:
                cursor = db.cursor()
                cursor.execute("Insert into log(username, name, file_number, date, unique_id, log_path)"
                               "values('%s', '%s', '%s', '%s', '%s', '%s');" %
                               (username, name, file_number, date,
                                self.user_unique, log_path))
                db.commit()
            except Exception as e:
                print("update data fail" + e.__str__())
            db.close()

            try:
                self.check_data_win = LogReader(self.user_unique, name, log_path, file_number)
                self.check_data_win.show()
            except Exception as e:
                QMessageBox.information(self, 'Error', e.__str__(), QMessageBox.Ok)
        else:
            QMessageBox.information(self, '错误！', '请重新发送请求！', QMessageBox.Ok)
        # QMessageBox.information(self, '祝您身体健康！', self.user_unique, QMessageBox.Ok)

    def closeWin(self):

        """
        never mind
        :return:
        """

        self.close()
