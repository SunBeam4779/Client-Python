from PyQt5.Qt import *


class LogReader(QWidget):
    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 1000
    _size_of_y = 500
    _path = "not defined"
    _name = "not defined"
    _date = "not defined"
    _content = []

    def __init__(self, unique_id, name, path, date):
        super(LogReader, self).__init__()

        self._name = name
        self._path = path
        self._date = date

        # set Icon
        self.Icon = QIcon(self._icon)

        # set userinfo
        self.user_unique = unique_id

        self.file_reader = QTextEdit()
        self.username = QLabel()
        self.date = QLabel()
        self.user_unique_label = QLabel()

        # set button
        self.exit = QPushButton()

        # set layout
        self.horizon_layout = QHBoxLayout()
        self.vertical_right_layout = QVBoxLayout()

        # set ui
        self.set_ui()
        self.set_button()
        self.set_reader_label()
        self.make_file()

    def set_ui(self):

        """
        set the graph layout
        :return: none
        """

        self.setLayout(self.horizon_layout)
        self.setWindowTitle("诊断报告 编号：%s" % self._date)
        self.setWindowIcon(self.Icon)
        self.setWindowState(Qt.WindowMaximized)

        # set right
        self.vertical_right_layout.addWidget(self.username)
        self.vertical_right_layout.addWidget(self.user_unique_label)
        self.vertical_right_layout.addWidget(self.date)
        self.vertical_right_layout.addStretch(1)
        self.vertical_right_layout.addWidget(self.exit)

        # set layout
        self.horizon_layout.addWidget(self.file_reader)
        # self.horizon_layout.addStretch(0)
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
        self.exit.setFont(font)

        # set text
        self.exit.setText("返回")

        self.exit.setFixedSize(300, 150)

        self.exit.clicked.connect(self.close_win)

    def set_reader_label(self):

        font = QFont()
        font.setFamily("Times")
        font.setPixelSize(50)

        self.username.setFont(font)
        self.user_unique_label.setFont(font)
        self.date.setFont(font)
        self.file_reader.setFont(font)

        self.file_reader.setFixedSize(1500, 985)

        self.username.setText("姓名：%s" % self._name)
        self.user_unique_label.setText("身份编号：%s" % self.user_unique)
        self.date.setText("报告日期编号：\n%s" % self._date)

    def make_file(self):

        log = open(self._path)
        lines = log.readlines()
        for line in lines:
            self.file_reader.append(line)

    def close_win(self):
        self.close()
