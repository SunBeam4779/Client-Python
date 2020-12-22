import os

import numpy
import pymysql
from PyQt5.Qt import *
from Client.LogReader import LogReader


class LogManager(QWidget):

    """
    manage the diagnosis.
    you can choose to check or delete them.
    """

    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 1000
    _size_of_y = 500
    _data_path = "not defined"
    _file_number = "not defined"
    _name = "not defined"
    # _data_type = "not defined"
    _item_row = None

    def __init__(self, unique_id):
        super(LogManager, self).__init__()

        # set Icon
        self.Icon = QIcon(self._icon)

        # set userinfo
        self.user_unique_id = unique_id

        # window
        self.check_data_win = None

        # set data container
        font_of_table = QFont()
        font_of_table.setFamily("Times")
        font_of_table.setPixelSize(35)

        self.items = self.select_data()  # get data

        self.table = QTableWidget()
        self.table.setFont(font_of_table)
        self.table.setFixedSize(1500, 985)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['姓名', '身份编号', '报告编号'])
        self.table.setShowGrid(False)
        self.table.setColumnWidth(0, 210)
        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(2, 500)

        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.clicked.connect(self.select_item)
        self.set_table()

        # set button
        self.check_data = QPushButton()
        self.delete_data = QPushButton()
        self.exit = QPushButton()

        # set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_right_layout = QVBoxLayout()

        # set ui
        self.set_ui()
        self.set_button()

    def set_ui(self):

        """
        set the graph layout
        :return: none
        """

        self.setLayout(self.horizon_layout)
        self.setWindowTitle("报告查看")
        self.setWindowIcon(self.Icon)
        self.setWindowState(Qt.WindowMaximized)
        # self.resize(self._size_of_x, self._size_of_y)

        # set right
        self.vertical_right_layout.addWidget(self.check_data)
        self.vertical_right_layout.addWidget(self.delete_data)
        self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.exit)

        # set layout
        self.horizon_layout.addWidget(self.table)
        self.horizon_layout.addLayout(self.vertical_right_layout)

    def set_button(self):

        """
        set up the button
        :return: none
        """

        font = QFont()
        font.setFamily("Times")
        font.setPixelSize(50)

        # set font
        self.check_data.setFont(font)
        self.delete_data.setFont(font)
        self.exit.setFont(font)

        # set text
        self.check_data.setText("查看")
        self.delete_data.setText("删除")
        self.exit.setText("返回")

        self.check_data.setFixedSize(300, 150)
        self.delete_data.setFixedSize(300, 150)
        self.exit.setFixedSize(300, 150)

        self.check_data.clicked.connect(self.slot_check)
        self.delete_data.clicked.connect(self.delete_item)
        self.exit.clicked.connect(self.close_win)

    def set_table(self):

        """
        set up the data table
        :return: none
        """

        row = len(self.items)
        if row == 0:
            return

        font_of_table = QFont()
        font_of_table.setFamily("Times")
        font_of_table.setPixelSize(30)

        self.table.setRowCount(row)
        self.table.setHorizontalHeaderLabels(['姓名', '身份编号', '日期', '报告编号'])

        # display item
        index = 0
        for item in self.items:
            check_item = QRadioButton()
            check_item.setFont(font_of_table)
            check_item.setText(item[1])  # name
            # item_time = QTableWidgetItem(item[3])  # data number
            item_number = QTableWidgetItem(item[2])  # log number
            item_id = QTableWidgetItem(self.user_unique_id)
            self.table.setCellWidget(index, 0, check_item)
            self.table.setItem(index, 1, item_id)
            self.table.setItem(index, 2, item_number)
            index += 1

    def select_data(self):

        """
        get the user's log from database
        :return: the data list
        """

        if self.user_unique_id == "not defined":
            return []

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
            sql = "select * from LOG where unique_id='%s';" % self.user_unique_id  # sort order
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print("select data wrong" + e.__str__())

        return result

    def slot_check(self):

        """
        display the chosen log
        :return: none
        """

        if self._data_path == "not defined":
            QMessageBox.information(self, 'Error', 'The path of data not defined',
                                    QMessageBox.Ok)
        else:
            try:
                self.check_data_win = LogReader(self.user_unique_id, self._name, self._data_path, self._file_number)
                self.check_data_win.show()
            except Exception as e:
                QMessageBox.information(self, '错误！', e.__str__(), QMessageBox.Ok)

    def select_item(self):

        """
        get the path of the chosen log
        :return: none
        """

        row_index = self.table.currentIndex().row()
        self._item_row = row_index
        self._data_path = self.items[row_index][5]  # path
        self._name = self.items[row_index][1]
        self._file_number = self.items[row_index][2]
        # print(self._data_path)

    def delete_item(self):

        """
        delete the chosen log
        :return: none
        """

        if self._data_path == "not defined" or self.user_unique_id == "not defined":
            QMessageBox.information(self, '错误！', '报告的路径未定义', QMessageBox.Ok)
        else:
            db = None
            cursor = None
            try:
                db = pymysql.connect(host='localhost', user='root', password='root', db='user')
                cursor = db.cursor()
            except Exception as e:
                print("database connection wrong" + e.__str__())
                QMessageBox.information(self, '错误！', '数据库连接出错。', QMessageBox.Ok)

            question = QMessageBox()
            question.setWindowTitle("删除")
            question.setText("确认要删除编号为'%s'的报告吗？" % self.items[self._item_row][3])
            question.setIcon(QMessageBox.Question)
            question.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            question.setDefaultButton(QMessageBox.No)
            yes = question.button(QMessageBox.Yes)
            no = question.button(QMessageBox.No)
            yes.setText("确定")
            no.setText("取消")
            question.exec_()
            if question.clickedButton() == yes:
                try:
                    print(self.items[self._item_row][2])
                    sql = "delete from LOG where (file_number='%s' and unique_id='%s');" % \
                          (self.items[self._item_row][2], self.user_unique_id)
                    cursor.execute(sql)
                    db.commit()
                    os.remove(self.items[self._item_row][5])  # delete the local file
                    # result = cursor.fetchall()
                    self.items = self.select_data()
                    self.table.clear()
                    self.set_table()
                except Exception as e:
                    print("select data wrong" + e.__str__())
                    QMessageBox.information(self, '错误！', '报告删除失败！', QMessageBox.Ok)
                    db.rollback()
            else:
                return
            QMessageBox.information(self, '成功！', '报告已成功删除！', QMessageBox.Ok)
            # //-update the table and data to be shown
            # self.items = self.select_data()
            # self.set_table()

    def close_win(self):

        """
        never mind
        :return: none
        """

        self.close()
