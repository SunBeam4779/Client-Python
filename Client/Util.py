# from bluepy import btle
import datetime
import time
from binascii import b2a_hex
import random
from PyQt5.QtChart import QDateTimeAxis, QValueAxis, QSplineSeries, QChart, QChartView
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate


#
# class MyDelegate(btle.DefaultDelegate):
#
#     """
#     handle the notification from the BLE device
#     """
#
#     def __init__(self, param):
#         btle.DefaultDelegate.__init__(self)
#         self.signal = param
#
#     def handleNotification(self, cHandle, data):
#         """
#         sending the data as a signal to the data acquiring window
#         :param cHandle: ignore it
#         :param data: the notification
#         :return: none
#         """
#         msg = str(b2a_hex(data))
#         self.signal.emit(msg)
#         # print("Received data: %s" % msg)


class ChartView(QChartView,QChart):

    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        # 声明并初始化X轴，Y轴
        self.vlaxisY = QValueAxis()
        self.dtaxisX = QValueAxis()
        self.series = QSplineSeries()
        self.chart = QChart()
        self.timer = QTimer(self)
        self.resize(1800, 400)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.chart_init()
        # self.timer_init()

    def timer_init(self):
        # 使用QTimer
        self.timer.timeout.connect(self.drawLine)
        self.timer.start(100)

    def chart_init(self):
        # 设置曲线名称
        # self.series.setName("实时数据")
        # 把曲线添加到QChart的实例中
        # self.chart.addSeries(self.series)

        # 设置坐标轴显示范围
        self.dtaxisX.setMin(0)
        self.dtaxisX.setMax(1500)
        self.vlaxisY.setMin(-3)
        self.vlaxisY.setMax(3)
        # 设置X轴时间样式
        # self.dtaxisX.setFormat("MM月dd hh:mm:ss")
        # 设置坐标轴上的格点
        self.dtaxisX.setTickCount(10)
        self.vlaxisY.setTickCount(5)
        # 设置坐标轴名称
        self.dtaxisX.setTitleText("时间/s")
        self.vlaxisY.setTitleText("电压/mV")
        # 设置网格不显示
        self.vlaxisY.setGridLineVisible(False)
        # 把坐标轴添加到chart中
        self.chart.addAxis(self.dtaxisX, Qt.AlignBottom)
        self.chart.addAxis(self.vlaxisY, Qt.AlignLeft)
        # 把曲线关联到坐标轴
        self.series.attachAxis(self.dtaxisX)
        self.series.attachAxis(self.vlaxisY)

        self.setChart(self.chart)

    def drawLine(self):
        # 获取当前时间
        bjtime = QDateTime.currentDateTime()
        # 更新X轴坐标
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-20*1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        # 当曲线上的点超出X轴的范围时，移除最早的点
        if self.series.count() > 200:
            self.series.removePoints(0, self.series.count()-200)
        # 产生随即数
        yint = random.randint(0, 1500)
        # 添加数据到曲线末端
        self.series.append(bjtime.toMSecsSinceEpoch(), yint)
