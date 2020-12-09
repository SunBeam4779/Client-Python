import time

import pymysql
import os

from PyQt5 import QtWidgets
from PyQt5.Qt import *
from Client.BLE import BLE
# from Client.BLEwithBleak import BLEwithBleak
from Client.DataManager import DataManager
from Client.Synchronize import Synchronize
from Client.LogManager import LogManager
from Client.GetIP import GetIP

import pyqtgraph as pg
import numpy as np
from pyqtgraph import GraphicsLayoutWidget


class MainWindow(QWidget):
    _icon = "./docs/20190702211158.jpg"
    _size_of_x = 800
    _size_of_y = 450
    _size_of_profile_x = 300
    _size_of_profile_y = 300

    def __init__(self, user):
        super(MainWindow, self).__init__()

        # user info
        self.user_account_name = "UniversalVoyage"
        self.user_name = "UniversalVoyage"
        self.user_id = "3118113030"
        self.user_gender = "男"
        self.user_room = "413"
        self.user_enter_date = "2020-10-25"
        self.user_unique = "not defined"
        self.profile = "./docs/20190702211158.jpg"
        self.get_user_info(user)
        self.profile = self.get_user_profile(self.user_unique)
        self.ip_address = "not defined"
        self.port = "not defined"

        # make directories for user
        self.make_user_dir()

        # set ICON
        self.Icon = QIcon(self._icon)

        # set sub-window
        self.acquire_win = None
        self.data_manager_win = None
        self.data_sync_win = None
        self.log_win = None
        self.getIP_win = None

        # set label
        self.gender = QLabel(self)
        self.ID = QLabel(self)
        self.username = QLabel(self)
        self.EnterDate = QLabel(self)
        self.Profile = QLabel(self)

        self.HeartRate = QLabel(self)
        self.BloodPressure = QLabel(self)
        self.RespirationRate = QLabel(self)
        self.ECG = QLabel(self)
        self.SpO2 = QLabel(self)
        self.PulseWave = QLabel(self)
        self.Respiration = QLabel(self)
        self.Video = QLabel(self)

        # set data graph
        pg.setConfigOption('background', '#f0f0f0')
        pg.setConfigOption('foreground', 'd')
        pg.setConfigOptions(antialias=True)

        self.central_widget = QtWidgets.QWidget(self)
        self.ECG_graph = GraphicsLayoutWidget(self)
        self.Pulse_graph = GraphicsLayoutWidget(self)
        self.RESP_graph = GraphicsLayoutWidget(self)

        # fake data
        data = np.loadtxt("./docs/data/yuhang4131130301/ECG/filtered/data332_Channel1_dec.txt")
        data2 = np.loadtxt("./docs/data/yuhang4131130301/ECG/filtered/data312_Channel1_dec.txt")
        print(data.shape)
        print(data2.shape)

        self.ECG_graph.addPlot(y=data, pen=pg.mkPen(color='b', width=2))
        self.Pulse_graph.addPlot(y=data, pen=pg.mkPen(color='b', width=2))
        self.RESP_graph.addPlot(y=data2, pen=pg.mkPen(color='b', width=2))

        self.valueOfHeartRate = QLabel()
        self.valueOfBloodPressure = QLabel()
        self.valueOfRespRate = QLabel()
        self.valueOfSpO2 = QLabel()

        # set button
        self.Acquire = QPushButton()
        self.CheckAndManage = QPushButton()
        self.Synchronize = QPushButton()
        self.Log = QPushButton()
        self.VideoSaving = QPushButton()
        self.Pause = QPushButton()
        self.Stop = QPushButton()
        self.time = QPushButton()

        # set layout
        self.vertical_layout = QVBoxLayout()

        self.horizon_top_layout = QHBoxLayout()
        self.vertical_top_left_info_layout = QVBoxLayout()
        self.horizon_top_left_button_layout = QHBoxLayout()
        self.horizon_top_left_profile = QHBoxLayout()
        self.vertical_top_left_layout = QVBoxLayout()
        self.horizon_top_right_layout = QHBoxLayout()
        self.vertical_right_top_left_layout = QVBoxLayout()

        self.vertical_bottom_layout = QVBoxLayout()
        self.horizon_bottom_top_layout_value = QHBoxLayout()
        self.horizon_bottom_left_layout_ECG = QHBoxLayout()
        self.horizon_bottom_left_layout_PW = QHBoxLayout()
        self.horizon_bottom_left_layout_RESP = QHBoxLayout()

        # add item
        self.add_label()
        self.add_button()

        # set layout
        self.set_ui()

    def set_ui(self):

        """
        set the graph layout
        :return: none
        """

        self.setLayout(self.vertical_layout)
        self.setWindowTitle("欢迎使用！" + self.user_name)

        # desktop = QtWidgets.QApplication.desktop()
        # self._size_of_x = desktop.width()
        # self._size_of_y = desktop.height()

        self.setWindowIcon(self.Icon)
        # self.resize(self._size_of_x, self._size_of_y)
        # print(self._size_of_x.__str__() + " " + self._size_of_y.__str__())
        self.setWindowState(Qt.WindowMaximized)
        # print(self.height())
        print(self.geometry().width(), self.geometry().height())
        # self.setFixedWidth(26)
        # self.setFixedHeight(650)
        # self.setFixedSize(self.width(), self.height())

        # set left-top-mid
        # self.vertical_left_top_right_layout.addStretch(0)
        self.vertical_top_left_info_layout.addWidget(self.username)
        self.vertical_top_left_info_layout.addWidget(self.gender)
        self.vertical_top_left_info_layout.addWidget(self.ID)
        self.vertical_top_left_info_layout.addWidget(self.EnterDate)

        # set left-top-right
        self.horizon_top_left_button_layout.addWidget(self.Acquire)
        # self.horizon_top_left_button_layout.addStretch(0)
        self.horizon_top_left_button_layout.addWidget(self.CheckAndManage)
        # self.horizon_top_left_button_layout.addStretch(0)
        self.horizon_top_left_button_layout.addWidget(self.Synchronize)
        # self.horizon_top_left_button_layout.addStretch(0)
        self.horizon_top_left_button_layout.addWidget(self.time)
        # self.horizon_top_left_button_layout.addStretch(0)
        self.horizon_top_left_button_layout.addWidget(self.Log)
        self.horizon_top_left_button_layout.addStretch(0)

        # set left-top
        self.horizon_top_left_profile.addWidget(self.Profile, alignment=Qt.AlignBottom)
        self.horizon_top_left_profile.addLayout(self.vertical_top_left_info_layout)
        self.horizon_top_left_profile.addStretch(0)

        self.vertical_top_left_layout.addLayout(self.horizon_top_left_profile)
        self.vertical_top_left_layout.addLayout(self.horizon_top_left_button_layout)

        # set top-right
        self.vertical_right_top_left_layout.addWidget(self.VideoSaving)
        # self.vertical_right_top_left_layout.addStretch(0)
        self.vertical_right_top_left_layout.addWidget(self.Pause)
        # self.vertical_right_top_left_layout.addStretch(0)
        self.vertical_right_top_left_layout.addWidget(self.Stop)

        self.horizon_top_right_layout.addLayout(self.vertical_right_top_left_layout)
        self.horizon_top_right_layout.addWidget(self.Video)

        # set top
        self.horizon_top_layout.addLayout(self.vertical_top_left_layout)
        self.horizon_top_layout.addLayout(self.horizon_top_right_layout)

        # set bottom-left
        self.horizon_bottom_top_layout_value.addWidget(self.HeartRate)
        self.horizon_bottom_top_layout_value.addWidget(self.valueOfHeartRate)
        self.horizon_bottom_top_layout_value.addStretch(0)

        self.horizon_bottom_top_layout_value.addWidget(self.BloodPressure)
        self.horizon_bottom_top_layout_value.addWidget(self.valueOfBloodPressure)
        self.horizon_bottom_top_layout_value.addStretch(0)

        self.horizon_bottom_top_layout_value.addWidget(self.RespirationRate)
        self.horizon_bottom_top_layout_value.addWidget(self.valueOfRespRate)
        self.horizon_bottom_top_layout_value.addStretch(0)

        self.horizon_bottom_top_layout_value.addWidget(self.SpO2)
        self.horizon_bottom_top_layout_value.addWidget(self.valueOfSpO2)
        self.horizon_bottom_top_layout_value.addStretch(0)
        # self.vertical_bottom_layout.addLayout(self.horizon_bottom_top_layout_value)

        self.horizon_bottom_left_layout_ECG.addWidget(self.ECG)
        self.horizon_bottom_left_layout_ECG.addWidget(self.ECG_graph)
        # self.horizon_bottom_left_layout_ECG.addStretch(0)
        self.vertical_bottom_layout.addLayout(self.horizon_bottom_left_layout_ECG)

        self.horizon_bottom_left_layout_PW.addWidget(self.PulseWave)
        self.horizon_bottom_left_layout_PW.addWidget(self.Pulse_graph)
        # self.horizon_bottom_left_layout_PW.addStretch(0)
        self.vertical_bottom_layout.addLayout(self.horizon_bottom_left_layout_PW)

        self.horizon_bottom_left_layout_RESP.addWidget(self.Respiration)
        self.horizon_bottom_left_layout_RESP.addWidget(self.RESP_graph)
        # self.horizon_bottom_left_layout_RESP.addStretch(0)
        self.vertical_bottom_layout.addLayout(self.horizon_bottom_left_layout_RESP)

        # set the whole layout
        self.vertical_layout.addLayout(self.horizon_top_layout)
        # self.vertical_layout.addStretch(0)
        self.vertical_layout.addLayout(self.horizon_bottom_top_layout_value)
        # self.vertical_layout.addStretch(0)
        self.vertical_layout.addLayout(self.vertical_bottom_layout)

    def add_button(self):

        """
        set the button to operate the video and the other common function
        :return: none
        """

        # set the font of button
        font_of_button = QFont()
        font_of_button.setFamily('Times')
        font_of_button.setPixelSize(22)

        self.Acquire.setFont(font_of_button)
        self.CheckAndManage.setFont(font_of_button)
        self.Synchronize.setFont(font_of_button)
        self.time.setFont(font_of_button)
        self.Log.setFont(font_of_button)
        self.VideoSaving.setFont(font_of_button)
        self.Pause.setFont(font_of_button)
        self.Stop.setFont(font_of_button)

        self.Acquire.setText("数据采集")
        self.CheckAndManage.setText("查看与管理")
        self.Synchronize.setText("数据同步")
        self.time.setText("校时")
        self.Log.setText("查看报告")
        self.VideoSaving.setText("保存")
        self.Pause.setText("暂停")
        self.Stop.setText("停止")

        self.Acquire.setFixedSize(165, 100)
        self.CheckAndManage.setFixedSize(165, 100)
        self.Synchronize.setFixedSize(165, 100)
        self.time.setFixedSize(165, 100)
        self.Log.setFixedSize(165, 100)

        self.VideoSaving.setFixedSize(100, 100)
        self.Pause.setFixedSize(100, 100)
        self.Stop.setFixedSize(100, 100)

        self.Acquire.clicked.connect(self.slot_acquire)
        self.CheckAndManage.clicked.connect(self.slot_data_manager)
        self.Synchronize.clicked.connect(self.slot_get_ip)
        self.Log.clicked.connect(self.slot_log_check)

    def add_label(self):

        """
        labels contain the tips and user's information
        :return: none
        """

        font_of_profile = QFont()
        font_of_profile.setFamily('Times')
        font_of_profile.setPixelSize(55)

        font_of_info = QFont()
        font_of_info.setFamily('Times')
        font_of_info.setPixelSize(35)

        self.Profile.setFont(font_of_profile)
        self.username.setFont(font_of_profile)
        self.gender.setFont(font_of_profile)
        self.ID.setFont(font_of_profile)
        self.EnterDate.setFont(font_of_profile)

        self.HeartRate.setFont(font_of_info)
        self.BloodPressure.setFont(font_of_info)
        self.RespirationRate.setFont(font_of_info)
        self.ECG.setFont(font_of_info)
        self.SpO2.setFont(font_of_info)
        self.PulseWave.setFont(font_of_info)
        self.Respiration.setFont(font_of_info)

        self.valueOfHeartRate.setFont(font_of_info)
        self.valueOfBloodPressure.setFont(font_of_info)
        self.valueOfRespRate.setFont(font_of_info)
        self.valueOfSpO2.setFont(font_of_info)

        self.valueOfHeartRate.setText("--")
        self.valueOfBloodPressure.setText("--")
        self.valueOfRespRate.setText("--")
        self.valueOfSpO2.setText("--")

        # set the text color
        self.HeartRate.setStyleSheet("color:green")
        self.BloodPressure.setStyleSheet("color:green")
        self.RespirationRate.setStyleSheet("color:green")
        self.ECG.setStyleSheet("color:green")
        self.SpO2.setStyleSheet("color:green")
        self.PulseWave.setStyleSheet("color:green")
        self.Respiration.setStyleSheet("color:green")

        self.valueOfHeartRate.setStyleSheet("color:green")
        self.valueOfBloodPressure.setStyleSheet("color:green")
        self.valueOfRespRate.setStyleSheet("color:green")
        self.valueOfSpO2.setStyleSheet("color:green")

        # this will be replaced by the user's image later
        self.Profile.setPixmap(QPixmap(self.profile).scaled(self._size_of_profile_x, self._size_of_profile_y))
        self.username.setText("用户姓名：" + self.user_name)
        self.gender.setText("性别：" + self.user_gender)
        self.ID.setText("身份编号：" + self.user_unique)
        self.EnterDate.setText("入园日期：" + self.user_enter_date)

        # this will be replaced by the video preview later
        self.Video.setPixmap((QPixmap("./docs/20191012094812.jpg").scaled(720, 400)))

        self.HeartRate.setText("心率：")
        self.BloodPressure.setText("血压：")
        self.RespirationRate.setText("呼吸率：")
        self.ECG.setText("心电：")
        self.SpO2.setText("血氧：")
        self.PulseWave.setText("脉搏：")
        self.Respiration.setText("呼吸：")

    def get_user_info(self, user):

        """
        get the user's information
        :param user: a list contains the user's information
        :return: none
        """

        if len(user) == 0:
            return
        self.user_account_name = user[0]
        self.user_name = user[2]
        self.user_id = user[3]
        if user[4] == "male":
            self.gender = "男"
        else:
            self.gender = "女"
        self.user_room = user[5]
        date = user[-2]
        self.user_enter_date = date[:4] + "-" + date[4:6] + "-" + date[-2:]
        self.user_unique = user[-1]
        # print(self.user_unique)

    def get_user_profile(self, unique):

        """
        set the user's profile
        search the profile in the database by user's unique id.
        :param unique: the user's unique id
        :return: the path that stored the user's profile
        """

        if unique == "not defined":
            # print(unique)
            return self._icon
        db = pymysql.connect(host='localhost', user='root', password='root', db='user')
        cursor = db.cursor()
        result = None
        sql = "SELECT * FROM PROFILE WHERE unique_id='%s';" % unique
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print(e.__str__())
        # print(len(result))
        if len(result) == 0:
            return self.profile
        return result[0][-1]

    def slot_acquire(self):

        """
        open the BLE managing window
        :return: none
        """

        self.acquire_win = BLE(self.user_unique)
        self.acquire_win.signal.connect(self.update_data)
        # self.acquire_win = BLEwithBleak()
        self.acquire_win.show()

    def update_data(self):

        """
        update the recently acquired data
        :return: none
        """

        day = str(time.strftime("%Y%m%d", time.localtime()))
        # set database
        db = None
        # cursor = None
        try:
            db = pymysql.connect(host='localhost', user='root', password='root', db='user')
            # cursor = db.cursor()
        except Exception as e:
            print("database connection wrong" + e.__str__())

        result = None
        try:
            cursor = db.cursor()
            sql = "select * from userdata where (unique_id='%s' and date='%s') order by data_number" % \
                  (self.user_unique_id, day)
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print("select data wrong" + e.__str__())

        # //-get the data to display
        # //-by the way, this part of code is definite a piece of shit.
        # //-however, I cannot find a more decent way to go.
        mark_ecg = False
        mark_resp = False
        mark_pulse = False
        mark_hr = False
        mark_respr = False
        mark_spo2 = False
        mark_bp = False
        ecg_new = None
        resp_new = None
        pulse_new = None
        hr_new = None
        respr_new = None
        spo2_new = None
        bp_new = None
        for i in range(len(result)):
            if result[i][5] == "ECG" and mark_ecg is not True:
                mark_ecg = True
                ecg_new = np.loadtxt(result[i][6])
            if result[i][5] == "RESP" and mark_resp is not True:
                mark_resp = True
                resp_new = np.loadtxt(result[i][6])
            if result[i][5] == "PULSE" and mark_pulse is not True:
                mark_pulse = True
                pulse_new = np.loadtxt(result[i][6])
            if result[i][5] == "HR" and mark_hr is not True:
                mark_hr = True
                hr_new = result[i][6]
            if result[i][5] == "RESPR" and mark_respr is not True:
                mark_respr = True
                respr_new = result[i][6]
            if result[i][5] == "SPO2" and mark_spo2 is not True:
                mark_spo2 = True
                spo2_new = result[i][6]
            if result[i][5] == "BP" and mark_bp is not True:
                mark_bp = True
                bp_new = result[i][6]

        if mark_ecg:
            self.ECG_graph.addPlot(y=ecg_new, pen=pg.mkPen(color='b', width=2))
        if mark_pulse:
            self.Pulse_graph.addPlot(y=pulse_new, pen=pg.mkPen(color='b', width=2))
        if mark_resp:
            self.RESP_graph.addPlot(y=resp_new, pen=pg.mkPen(color='b', width=2))
        if mark_hr:
            self.valueOfHeartRate.setText(hr_new)
        if mark_bp:
            self.valueOfBloodPressure.setText(bp_new)
        if mark_spo2:
            self.valueOfSpO2.setText(spo2_new)
        if mark_respr:
            self.valueOfRespRate.setText(respr_new)
        # //-THE shit is over.

    def slot_data_manager(self):

        """
        open the Data manager window
        :return: none
        """

        # print(self.user_unique)
        self.data_manager_win = DataManager(self.user_unique)
        self.data_manager_win.show()

    def slot_data_sync(self):

        """
        open the data synchronizing window
        :return: none
        """

        self.data_sync_win = Synchronize(self.user_unique, self.ip_address, self.port)
        self.data_sync_win.show()

    def slot_get_ip(self):

        """
        get the server's ip address
        :return: none
        """

        self.getIP_win = GetIP()
        self.getIP_win.signal.connect(self.slot_set_ip)
        self.getIP_win.show()

    def slot_set_ip(self, message):

        """
        set the ip address
        :return: none
        """

        self.ip_address = message['ip']
        self.port = message['port']
        print("ip: " + self.ip_address + " port: " + self.port)
        self.slot_data_sync()

    def slot_log_check(self):

        """
        open the log manager window
        :return: none
        """

        self.log_win = LogManager(self.user_unique)
        self.log_win.show()

    def make_user_dir(self):

        """
        make the data directories for user
        :return: none
        """

        if self.user_unique == "not defined":
            return

        data = "./docs/data/"
        path = data + self.user_name + self.user_unique + "/"  # user's own dir
        ecg = path + "ECG/"  # ECG
        ecg_original = ecg + "original/"
        ecg_filtered = ecg + "filtered/"
        resp = path + "RESP/"  # respiration
        resp_original = resp + "original/"
        resp_filtered = resp + "filtered/"
        pulse = path + "PULSE/"  # pulse wave
        pulse_original = pulse + "original/"
        pulse_filtered = pulse + "filtered/"
        video = path + "VIDEO/"  # video

        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(ecg):
            try:
                os.mkdir(ecg)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(ecg_original):
            try:
                os.mkdir(ecg_original)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(ecg_filtered):
            try:
                os.mkdir(ecg_filtered)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(resp):
            try:
                os.mkdir(resp)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(resp_original):
            try:
                os.mkdir(resp_original)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(resp_filtered):
            try:
                os.mkdir(resp_filtered)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(pulse):
            try:
                os.mkdir(pulse)
            except Exception as e:
                print(e)

        if not os.path.exists(pulse_original):
            try:
                os.mkdir(pulse_original)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(pulse_filtered):
            try:
                os.mkdir(pulse_filtered)
            except Exception as e:
                print(e.__str__())

        if not os.path.exists(video):
            try:
                os.mkdir(video)
            except Exception as e:
                print(e.__str__())

    def closeEvent(self, event):

        """
        handle the main window closing event
        :param event: the main window closing event
        :return: none
        """

        question = QMessageBox()
        question.setWindowTitle("退出")
        question.setText("确认要退出吗？")
        question.setIcon(QMessageBox.Question)
        question.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        question.setDefaultButton(QMessageBox.No)
        yes = question.button(QMessageBox.Yes)
        no = question.button(QMessageBox.No)
        yes.setText("确定")
        no.setText("取消")
        question.exec_()
        # //-when the main window is about to close, ask user to choose operation.
        if question.clickedButton() == yes:
            event.accept()
        else:
            event.ignore()
