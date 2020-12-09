import pymysql

from PyQt5 import QtCore
from PyQt5.Qt import *


class SignUp(QWidget):
    _icon = ".\\docs\\20190702211158.jpg"
    _size_of_x = 1000
    _size_of_y = 800
    my_Signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(SignUp, self).__init__()
        self.set_ui()

        # icon
        self.icon = QIcon(self._icon)
        self.change_icon()

        # label
        self.username_label = QLabel(self)
        self.username_label.setAlignment(Qt.AlignRight)
        self.password_label = QLabel(self)
        self.password_label.setAlignment(Qt.AlignRight)
        self.confirmed_label = QLabel(self)
        self.confirmed_label.setAlignment(Qt.AlignRight)
        self.identity_name = QLabel(self)
        self.identity_name.setAlignment(Qt.AlignRight)
        self.identity_number = QLabel(self)
        self.identity_number.setAlignment(Qt.AlignRight)
        self.gender = QLabel(self)
        self.gender.setAlignment(Qt.AlignRight)
        self.building_and_room = QLabel(self)
        self.building_and_room.setAlignment(Qt.AlignRight)
        self.home_address = QLabel(self)
        self.home_address.setAlignment(Qt.AlignRight)
        self.phone_number = QLabel(self)
        self.phone_number.setAlignment(Qt.AlignRight)
        self.cellphone = QLabel(self)
        self.cellphone.setAlignment(Qt.AlignRight)
        self.user_height = QLabel(self)
        self.user_height.setAlignment(Qt.AlignRight)
        self.user_weight = QLabel(self)
        self.user_weight.setAlignment(Qt.AlignRight)
        self.history_of_disease = QLabel(self)
        self.history_of_disease.setAlignment(Qt.AlignRight)

        self.set_label()

        # input
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.confirmed_edit = QLineEdit(self)
        self.identity_name_edit = QLineEdit(self)
        self.identity_number_edit = QLineEdit(self)
        self.building_and_room_edit = QLineEdit(self)
        self.home_address_edit = QTextEdit(self)
        self.phone_number_edit = QLineEdit(self)
        self.cellphone_edit = QLineEdit(self)
        self.user_height_edit = QLineEdit(self)
        self.user_weight_edit = QLineEdit(self)
        self.history_of_disease_edit = QTextEdit(self)
        self.add_line_edit()

        # button
        self.sign_button = QPushButton("注册", self)
        self.back = QPushButton("返回", self)
        self.male = QRadioButton("男")
        self.female = QRadioButton("女")
        self.add_button()

        # set layout
        horizon_layout = QHBoxLayout(self)
        wide_layout1 = QVBoxLayout()
        wide_layout2 = QVBoxLayout()
        self.setLayout(horizon_layout)
        horizon_layout1 = QHBoxLayout()
        horizon_layout2 = QHBoxLayout()
        horizon_layout3 = QHBoxLayout()
        horizon_layout4 = QHBoxLayout()
        horizon_layout5 = QHBoxLayout()
        horizon_layout6 = QHBoxLayout()
        horizon_layout7 = QHBoxLayout()
        horizon_layout8 = QHBoxLayout()

        horizon_layout1.addWidget(self.username_label)
        horizon_layout1.addWidget(self.username_edit)
        horizon_layout1.addWidget(self.identity_name)
        horizon_layout1.addWidget(self.identity_name_edit)

        horizon_layout2.addWidget(self.password_label)
        horizon_layout2.addWidget(self.password_edit)
        horizon_layout2.addWidget(self.confirmed_label)
        horizon_layout2.addWidget(self.confirmed_edit)

        horizon_layout3.addWidget(self.identity_number)
        horizon_layout3.addWidget(self.identity_number_edit)
        horizon_layout3.addWidget(self.building_and_room)
        horizon_layout3.addWidget(self.building_and_room_edit)

        horizon_layout4.addWidget(self.home_address)
        horizon_layout4.addWidget(self.home_address_edit)

        horizon_layout5.addWidget(self.phone_number)
        horizon_layout5.addWidget(self.phone_number_edit)
        horizon_layout5.addWidget(self.cellphone)
        horizon_layout5.addWidget(self.cellphone_edit)

        horizon_layout6.addWidget(self.user_height)
        horizon_layout6.addWidget(self.user_height_edit)
        horizon_layout6.addWidget(self.user_weight)
        horizon_layout6.addWidget(self.user_weight_edit)

        horizon_layout7.addWidget(self.gender)
        horizon_layout7.addWidget(self.male)
        horizon_layout7.addWidget(self.female)

        horizon_layout8.addWidget(self.history_of_disease)
        horizon_layout8.addWidget(self.history_of_disease_edit)

        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout1)
        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout2)
        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout3)
        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout4)
        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout5)
        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout6)
        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout7)
        wide_layout1.addStretch(1)
        wide_layout1.addLayout(horizon_layout8)

        wide_layout2.addStretch(1)
        wide_layout2.addWidget(self.sign_button, alignment=Qt.AlignVCenter)
        wide_layout2.addWidget(self.back, alignment=Qt.AlignVCenter)

        # horizon_layout.addStretch(1)
        horizon_layout.addLayout(wide_layout1)
        horizon_layout.addStretch(0)
        horizon_layout.addLayout(wide_layout2)
        # horizon_layout.addStretch(1)

    def set_ui(self):
        self.resize(self._size_of_x, self._size_of_y)
        self.setWindowTitle('注册')

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
        self.username_label.setText('账号')
        self.password_label.setText("密码")
        self.confirmed_label.setText("确认密码")
        self.identity_name.setText("姓名")
        self.identity_number.setText("身份证号")
        self.gender.setText("性别")
        self.building_and_room.setText("房间号")
        self.home_address.setText("家庭住址")
        self.phone_number.setText("电话号码")
        self.cellphone.setText("手机号码")
        self.user_height.setText("身高")
        self.user_weight.setText("体重")
        self.history_of_disease.setText("既往病史")

        # configuration
        self.username_label.setFixedSize(240, 40)
        self.password_label.setFixedSize(240, 40)
        self.confirmed_label.setFixedSize(240, 40)
        self.identity_name.setFixedSize(240, 40)
        self.identity_number.setFixedSize(240, 40)
        self.gender.setFixedSize(240, 40)
        self.building_and_room.setFixedSize(240, 40)
        self.home_address.setFixedSize(240, 40)
        self.phone_number.setFixedSize(240, 40)
        self.cellphone.setFixedSize(240, 40)
        self.user_height.setFixedSize(240, 40)
        self.user_weight.setFixedSize(240, 40)
        self.history_of_disease.setFixedSize(240, 40)

        # font
        label_font = QFont()
        label_font.setFamily('Times')
        label_font.setPixelSize(35)

        self.username_label.setFont(label_font)
        self.password_label.setFont(label_font)
        self.confirmed_label.setFont(label_font)
        self.identity_name.setFont(label_font)
        self.identity_number.setFont(label_font)
        self.gender.setFont(label_font)
        self.building_and_room.setFont(label_font)
        self.home_address.setFont(label_font)
        self.phone_number.setFont(label_font)
        self.cellphone.setFont(label_font)
        self.user_height.setFont(label_font)
        self.user_weight.setFont(label_font)
        self.history_of_disease.setFont(label_font)

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
        self.confirmed_edit.setEchoMode(QLineEdit.Password)
        self.username_edit.setEchoMode(QLineEdit.Normal)
        self.identity_name_edit.setEchoMode(QLineEdit.Normal)
        self.identity_number_edit.setEchoMode(QLineEdit.Normal)
        self.building_and_room_edit.setEchoMode(QLineEdit.Normal)
        self.phone_number_edit.setEchoMode(QLineEdit.Normal)
        self.cellphone_edit.setEchoMode(QLineEdit.Normal)
        self.user_height_edit.setEchoMode(QLineEdit.Normal)
        self.user_weight_edit.setEchoMode(QLineEdit.Normal)

        # set font
        self.username_edit.setFont(line_edit_font)
        self.password_edit.setFont(line_edit_font)
        self.confirmed_edit.setFont(line_edit_font)
        self.identity_name_edit.setFont(line_edit_font)
        self.identity_number_edit.setFont(line_edit_font)
        self.building_and_room_edit.setFont(line_edit_font)
        self.home_address_edit.setFont(line_edit_font)
        self.phone_number_edit.setFont(line_edit_font)
        self.cellphone_edit.setFont(line_edit_font)
        self.user_height_edit.setFont(line_edit_font)
        self.user_weight_edit.setFont(line_edit_font)
        self.history_of_disease_edit.setFont(line_edit_font)

        # set placeholder
        self.username_edit.setPlaceholderText("账号")
        self.password_edit.setPlaceholderText("密码")
        self.confirmed_edit.setPlaceholderText("确认密码")
        self.identity_name_edit.setPlaceholderText("姓名")
        self.identity_number_edit.setPlaceholderText("身份证号")
        self.building_and_room_edit.setPlaceholderText("房间号")
        self.home_address_edit.setPlaceholderText("家庭住址")
        self.phone_number_edit.setPlaceholderText("电话号码")
        self.cellphone_edit.setPlaceholderText("手机号码")
        self.user_height_edit.setPlaceholderText("身高/CM")
        self.user_weight_edit.setPlaceholderText("体重/kg")
        self.history_of_disease_edit.setPlaceholderText("既往病史")

        # size
        self.username_edit.setFixedSize(350, 40)
        self.password_edit.setFixedSize(350, 40)
        self.confirmed_edit.setFixedSize(350, 40)
        self.identity_name_edit.setFixedSize(350, 40)
        self.identity_number_edit.setFixedSize(350, 40)
        self.building_and_room_edit.setFixedSize(350, 40)
        self.home_address_edit.setFixedSize(955, 80)
        self.phone_number_edit.setFixedSize(350, 40)
        self.cellphone_edit.setFixedSize(350, 40)
        self.user_height_edit.setFixedSize(350, 40)
        self.user_weight_edit.setFixedSize(350, 40)
        self.history_of_disease_edit.setFixedSize(955, 80)

    def add_button(self):

        """
        add the button of executing signup into the window
        :return: none
        """

        # set font
        button_font = QFont()
        button_font.setFamily('Times')
        button_font.setPixelSize(30)
        self.sign_button.setFont(button_font)
        self.back.setFont(button_font)
        self.male.setFont(button_font)
        self.female.setFont(button_font)

        # fixed size
        self.sign_button.setFixedSize(160, 50)
        self.back.setFixedSize(160, 50)
        self.male.setFixedSize(160, 50)
        self.female.setFixedSize(160, 50)

        # text of notice
        self.sign_button.setText("注册")

        # action
        # self.login_button.clicked.connect(self.login)
        self.sign_button.clicked.connect(self.sign_up)
        self.back.clicked.connect(self.close_self)

    def paintEvent(self, event):

        """
        draw the background
        :param event: drawing event
        :return: none
        """

        painter = QPainter(self)
        pixmap = QPixmap("./docs/20191012094812.jpg")
        painter.drawPixmap(self.rect(), pixmap)

    @staticmethod
    def has_name(username):

        """
        check if the username is notnull
        :param username: username which the user input in the textedit
        :return: the username exists or not
        """

        # connect = sqlite3.connect('./data.db')
        db = pymysql.connect(host='localhost', user='root', password='root', db='user')

        # cursor = connect.cursor()
        cursor = db.cursor()
        result = None
        sql = "SELECT * FROM USERINFO WHERE username='%s';" % username  # sqlite statement
        try:
            cursor.execute(sql)
        # connect.commit()
        #     db.commit()
            result = cursor.fetchall()  # get the result of execution
        except Exception as e:
            print("hasname wrong" + e.__str__())
            db.rollback()
        cursor.close()
        # connect.close()
        db.close()
        if result:
            return True
        else:
            return False

    def sign_up(self):

        """
        the logic of signing up
        :return: none
        """

        # user info
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm = self.confirmed_edit.text()
        name = self.identity_name_edit.text()
        identity_number = self.identity_number_edit.text()
        gender = None
        if self.male.isChecked():
            gender = "male"
        if self.female.isChecked():
            gender = "female"
        room_number = self.building_and_room_edit.text()
        address = self.home_address_edit.toPlainText()
        phone_number = self.phone_number_edit.text()
        cellphone = self.cellphone_edit.text()
        height = self.user_height_edit.text()
        weight = self.user_weight_edit.text()
        history = self.history_of_disease_edit.toPlainText()
        date = QDate().currentDate()
        this_day = date.day()
        day = str(date.day())
        if this_day < 10:
            day = "0" + day
        year = str(date.year())
        this_month = date.month()
        month = str(date.month())
        if this_month < 10:
            month = "0" + month
        enter_date = year + month + day
        unique_id = self.get_unique_id(room_number, gender, identity_number)
        hasname = self.has_name(username)
        if not password or not confirm:  # if the password or confirm is null
            QMessageBox.information(self, '错误！', '密码为空！', QMessageBox.Ok)
        elif hasname:  # if the username has exists
            QMessageBox.information(self, '错误!', '账号已存在！', QMessageBox.Ok)
        else:
            # if the password and the confirmed password are both the same and notnull
            if password == confirm and password:
                # connect = sqlite3.connect('./data.db')
                db = pymysql.connect(host='localhost', user='root', password='root', db='user')
                # cursor = connect.cursor()
                cursor = db.cursor()
                sql = "INSERT INTO USERINFO (username, password, name, " \
                      "identity_number, gender, room_number, address, phone_number," \
                      "cellphone, height, weight, history, enter_date, unique_id) " \
                      "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % \
                      (username, password, name, identity_number,
                       gender, room_number, address, phone_number,
                       cellphone, height, weight, history, enter_date, unique_id)  # insert the data into database
                # data = None
                try:
                    cursor.execute(sql)
                    # connect.commit()
                    db.commit()
                except Exception as e:
                    print("wrong" + e.__str__())
                    db.rollback()
                # cursor.close()
                db.close()
                # connect.close()
                QMessageBox.information(self, '成功！', '注册成功！'.format(username),
                                        QMessageBox.Ok)
                self.close()  # close the window after signing up

            else:
                QMessageBox.information(self, '错误！', '两次输入的密码不一致！', QMessageBox.Ok)

    @staticmethod
    def get_unique_id(room, gender, identity):

        """
        generate the unique id of user
        :param room: room number
        :param gender: user's gender
        :param identity: user's identity id
        :return: the unique id
        """

        if gender == "male":
            return room + identity[-6:] + "1"
        else:
            return room + identity[-6:] + "0"

    def close_window(self):

        """
        never mind
        :return: none
        """

        content = '1'
        self.my_Signal.emit(content)
        self.close()

    def close_self(self):

        """
        clear the input after closing the window
        :return: none
        """

        self.username_edit.setText('')
        self.confirmed_edit.setText('')
        self.password_edit.setText('')
        self.identity_name_edit.setText('')
        self.identity_number_edit.setText('')
        self.building_and_room_edit.setText('')
        self.close_window()
