import pymysql
from PyQt5.Qt import *


class Synchronize(QWidget):

    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 600
    _size_of_y = 500
    _data_path = "not defined"
    _data_type = "not defined"
    _item_row = None

    def __init__(self, unique_id):
        super(Synchronize, self).__init__()

        self.user_unique = unique_id
        self.items = self.to_be_synchronized()

        # set Icon
        self.Icon = QIcon(self._icon)

        # set Button
        self.data_sync = QPushButton()
        self.time_sync = QPushButton()
        self.user_sync = QPushButton()
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
        self.exit.setFont(font)

        self.data_sync.setFixedSize(300, 150)
        self.time_sync.setFixedSize(300, 150)
        self.user_sync.setFixedSize(300, 150)
        self.exit.setFixedSize(300, 150)

        # set text
        self.data_sync.setText("数据同步")
        self.time_sync.setText("时间同步")
        self.user_sync.setText("用户同步")
        self.exit.setText("退出")

        self.exit.clicked.connect(self.closeWin)

    def set_table(self):
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
            item_type = QTableWidgetItem(item[4])  # data type
            item_value = QTableWidgetItem(item[5])  # value or path
            item_checkable = QTableWidgetItem(item[6])  # checkable
            self.table.setCellWidget(index, 0, check_item)
            self.table.setItem(index, 1, item_time)
            self.table.setItem(index, 2, item_type)
            self.table.setItem(index, 3, item_value)
            self.table.setItem(index, 4, item_checkable)
            index += 1

    def select_item(self):
        row_index = self.table.currentIndex().row()
        self._item_row = row_index
        self._data_path = self.items[row_index][5]  # path
        self._data_type = self.items[row_index][4]  # type
        # print(self._data_path)

    def to_be_synchronized(self):
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

        return result

    def closeWin(self):
        self.close()
