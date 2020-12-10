# import sqlite3
import pymysql

from PyQt5.Qt import *
from Client.SignUp import SignUp
from Client.MainWindow import MainWindow


class StartWindow(QWidget):
    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 1000
    _size_of_y = 800

    def __init__(self):
        super(StartWindow, self).__init__()
        self.set_ui()
        self.sign_up_win = SignUp()
        self.main_win = None
        self.init_database()

        # icon
        self.icon = QIcon(self._icon)
        self.change_icon()

        # label
        self.username_label = QLabel(self)
        self.username_label.setAlignment(Qt.AlignRight)
        self.password_label = QLabel(self)
        self.password_label.setAlignment(Qt.AlignRight)
        self.set_label()

        # input
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.add_line_edit()

        # button
        self.login_button = QPushButton("登录", self)
        self.sign_button = QPushButton("注册", self)
        self.add_button()

        # set layout
        wide_layout = QVBoxLayout(self)
        self.setLayout(wide_layout)
        horizon_layout1 = QHBoxLayout()
        horizon_layout2 = QHBoxLayout()

        # horizon_layout1.addStretch(0)
        horizon_layout1.addWidget(self.username_label)
        horizon_layout1.addWidget(self.username_edit)
        horizon_layout1.addWidget(self.login_button)

        horizon_layout2.addWidget(self.password_label)
        horizon_layout2.addWidget(self.password_edit)
        horizon_layout2.addWidget(self.sign_button)

        wide_layout.addStretch(0)
        wide_layout.addLayout(horizon_layout1)
        wide_layout.addLayout(horizon_layout2)

        # self.sign_up_win.sign_button.clicked.connect(self.sign_up_win.sign_up)

    def set_ui(self):
        self.resize(self._size_of_x, self._size_of_y)
        self.setWindowTitle("欢迎使用！")

    def change_icon(self):

        """
        change the icon of a window
        :return: none
        """

        self.setWindowIcon(self.icon)

    def set_label(self):

        """
        add the line label which contains the tips into the window
        :return: none
        """

        # text
        self.username_label.setText("账号")
        self.password_label.setText("密码")

        # configuration
        self.username_label.setFixedSize(240, 40)
        self.password_label.setFixedSize(240, 40)
        # self.username_label.move(120, 530)
        # self.password_label.move(120, 600)

        # font
        label_font = QFont()
        label_font.setFamily('Times')
        label_font.setPixelSize(35)
        self.username_label.setFont(label_font)
        self.password_label.setFont(label_font)

    def add_line_edit(self):

        """
        add the line edit for inputting user's information
        :return: none
        """

        line_edit_font = QFont()
        line_edit_font.setFamily('Times')
        line_edit_font.setPixelSize(30)

        # set pattern
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.username_edit.setEchoMode(QLineEdit.Normal)

        # set font
        self.username_edit.setFont(line_edit_font)
        self.password_edit.setFont(line_edit_font)

        # set placeholder
        self.username_edit.setPlaceholderText("请输入账号")
        self.password_edit.setPlaceholderText("请输入密码")

        # size
        self.username_edit.setFixedSize(350, 40)
        self.password_edit.setFixedSize(350, 40)

        # position
        # self.username_edit.move(320, 530)
        # self.password_edit.move(320, 600)

    def add_button(self):

        """
        add the button of signup and login into the window
        :return: none
        """

        button_font = QFont()
        button_font.setFamily('Times')
        button_font.setPixelSize(30)

        # fixed size
        self.login_button.setFixedSize(160, 50)
        self.sign_button.setFixedSize(160, 50)

        # set font
        self.login_button.setFont(button_font)
        self.sign_button.setFont(button_font)

        # position
        # self.login_button.move(750, 530)
        # self.sign_button.move(750, 600)

        # text of notice
        self.login_button.setText("登录")
        self.sign_button.setText("注册")

        # action
        self.login_button.clicked.connect(self.login)
        self.sign_button.clicked.connect(self.sign_up_window)
        self.sign_up_win.my_Signal.connect(self.sign_up_close)

    def paintEvent(self, event):

        """
        draw the background
        :param event: drawing event
        :return: none
        """

        painter = QPainter(self)
        pixmap = QPixmap("./docs/20191012094812.jpg")
        painter.drawPixmap(self.rect(), pixmap)

    def sign_up_window(self):

        """
        showing the sign up window
        :return: none
        """

        # clear the user's information before the window showing
        self.password_edit.setText('')
        self.username_edit.setText('')

        self.sign_up_win.show()

    @staticmethod
    def init_database():

        """
        database initial
        :return: none
        """

        connect = pymysql.connect(host='localhost', user='root', password='root', db='user')

        cursor = connect.cursor()
        # data type TEXT -> strings or words
        # REAL -> the float type
        # BIT ->  byte type
        sql1 = "CREATE TABLE IF NOT EXISTS USERINFO(username TEXT, password TEXT, " \
               "name TEXT, identity_number TEXT, gender TEXT, " \
               "room_number TEXT, address TEXT, phone_number TEXT, " \
               "cellphone TEXT, height TEXT, weight TEXT, " \
               "history TEXT, enter_date TEXT, unique_id TEXT);"
        try:
            cursor.execute(sql1)
            connect.commit()
        except Exception as e:
            print(e.__str__())
        sql2 = "CREATE TABLE IF NOT EXISTS PROFILE(username TEXT, name TEXT, unique_id TEXT, profile_path TEXT);"
        try:
            cursor.execute(sql2)
            connect.commit()
        except Exception as e:
            print(e.__str__())
        sql3 = "CREATE TABLE IF NOT EXISTS USERDATA(username TEXT, name TEXT, unique_id TEXT, data_number TEXT, " \
               "date TEXT, data_type TEXT, value TEXT, checkable TEXT, synchronized TEXT);"
        try:
            cursor.execute(sql3)
            connect.commit()
        except Exception as e:
            print(e.__str__())

        sql4 = "CREATE TABLE IF NOT EXISTS LOG(username TEXT, name TEXT, file_number TEXT, date TEXT," \
               "unique_id TEXT, log_path TEXT);"
        try:
            cursor.execute(sql4)
            connect.commit()
        except Exception as e:
            print(e.__str__())
        connect.close()

    def login(self):

        """
        the function of login
        :return: none
        """

        connect = pymysql.connect(host="localhost", user="root", password="root", db="user")
        cursor = connect.cursor()
        username = self.username_edit.text()
        password = self.password_edit.text()
        sql = "SELECT * FROM USERINFO WHERE username='%s';" % username  # query information from database
        result = None
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # print(type(result))
            # print(len(result[0]))
        except Exception as e:
            print("login" + e.__str__())
        if username and password:  # if the username and password are both notnull
            if result:
                if str(result[0][1]) == password:
                    QMessageBox.information(self, '成功！', '登录成功 \n 欢迎您！ {}'.format(username),
                                            QMessageBox.Ok)
                    self.main_win = MainWindow(result[0])
                    self.main_win.show()
                    self.close()
                else:
                    QMessageBox.information(self, '错误！', '用户名或密码错误，请重试！',
                                            QMessageBox.Ok)
                    self.password_edit.setText("")
                    self.username_edit.setText("")

            else:
                QMessageBox.information(self, '错误！', '用户名或密码错误，请重试！', QMessageBox.Ok)
        elif username:
            QMessageBox.information(self, '错误！', '请输入密码！', QMessageBox.Ok)
        else:
            QMessageBox.information(self, '错误！', '请填写用户名和密码！', QMessageBox.Ok)

    def sign_up_close(self):

        """
        never mind
        :return: none
        """

        pass

    def closeEvent(self, event):

        """
        handle the signup window closing event
        :param event: the signup window closing event
        :return: none
        """

        # when the main window is about to close, closing the sub-window
        self.sign_up_win.close()
        event.accept()
