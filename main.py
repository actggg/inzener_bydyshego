import csv
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog

class Entrance(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Начальный_Экран.ui', self)
        self.setWindowTitle('Вход')
        self.mistakes.hide()
        self.going.clicked.connect(self.allowance)
        self.registrationbutton.clicked.connect(self.register)
        self.setFixedSize(750, 520)
        self.statusBar().setVisible(False)

    def allowance(self):
        introduced_password = self.input_password.text()
        introduced_login = self.input_login.text()
        print('ddd')
        con = sqlite3.connect("аккаунты.db")
        cur = con.cursor()
        print(introduced_login, introduced_password)
        result = cur.execute(
            f""" Select login from Acc where Acc.login = '{introduced_login}'
            and Acc.password='{introduced_password}'""").fetchall()
        print(result)
        try:
            if result:
                for elem in result:
                    print(elem[0])
                    self.open_game = Quiz(elem[0])
                    self.open_game.show()
                    self.hide()
            else:
                self.mistakes.show()
            con.close()
        except Exception as e:
            print(e)

    def register(self):
        self.registration = Registration()
        self.registration.show()
        self.hide()


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('регистрация.ui', self)
        self.registration.clicked.connect(self.register_an_account)
        self.license_agreement.clicked.connect(self.license_agreement_open)
        self.statusBar().setVisible(False)
        self.setFixedSize(550, 550)

    def password_verification(self, password):
        lit_ang_connections = 'qwertyuiop        asdfghjkl      zxcvbnm'
        lit_rus_connections = 'йцукенгшщзхъ     фывапролджэё      ячсмитьбю'
        if list(set(list(password)) & set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])) == []:
            return 1
        elif len(password) <= 8:
            return 2
        elif password.isdigit():
            return 3
        elif password.isupper() or password.islower():
            return 4
        else:
            mini_password = password.lower()
            for i in lit_ang_connections.split() + lit_rus_connections.split():
                g = len(i) - 2
                for j in range(g):
                    if i[j: j + 3] in mini_password:
                        return 5
        return 0

    def register_an_account(self):
        password_errors = {
            1: 'в пароле должны содержаться цифры',
            2: 'пароль должен сосотоять из более чем 8 символов',
            3: 'в пароле должны содержаться буквы',
            4: 'в пароле должны содержаться большие и маленькие буквы',
            5: 'слишком простой пароль'
        }
        login_acc = self.login.text()
        password_acc = self.password.text()
        if login_acc != '' and password_acc != '' and self.password_2.text() != '':
            if self.statement.isChecked():
                if self.password.text() == self.password_2.text():
                    if self.password_verification(password_acc) == 0:
                        con = sqlite3.connect("аккаунты.db")
                        cursor = con.cursor()
                        cursor.execute("INSERT INTO Acc(login, password) VALUES(?, ?)", (login_acc, password_acc))
                        con.commit()
                        cursor.close()
                        con.close()
                        self.go_home = Entrance()
                        self.go_home.show()
                        self.hide()
                    else:
                        self.error_message.setText(password_errors[self.password_verification(password_acc)])
                else:
                    self.error_message.setText('пароли не совпадают')
            else:
                self.error_message.setText('вы забыли лицензионное соглашение')
        else:
            self.error_message.setText('не все поля заполнены')

    def license_agreement_open(self):
        self.setWindowTitle('Input dialog')
        self.show()
        text, ok = QInputDialog.getText(self, 'Лицензионное соглашение',
                                        f'Хоть кто то это прочитал, оставте свой отзыв')
        k = open('output.dat', 'w')
        k.write(text)


class Quiz(QMainWindow):
    def __init__(self, *accaunt):
        super().__init__()
        uic.loadUi('викторина.ui', self)
        self.setWindowTitle('Викторина')
        self.setFixedSize(800, 550)
        self.statusBar().setVisible(False)
        self.true = 0
        self.label_3.setText(f'Верно: {self.true}')
        self.dicti = {
            self.radioButton_4: 1,
            self.radioButton_3: 2,
            self.radioButton_2: 3,
            self.radioButton: 4
            }
        self.accaunt = accaunt
        self.num_qw = 1
        self.plainTextEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.entrance)
        self.pushButton_2.clicked.connect(self.true_answer)
        self.pushButton_3.clicked.connect(self.answer)
        self.pushButton_4.clicked.connect(self.refresh)
        self.file = 'Вопросы_для_викторины.txt'
        self.work_with_file(self.file)
        self.label_5.hide()
        self.pushButton_4.hide()

    def refresh(self):
        self.num_qw = 1
        self.true = 0
        self.label_5.hide()
        self.pushButton_4.hide()
        self.label_3.setText(f'Верно: {self.true}')
        self.label_4.setText('-')
        self.work_with_file(self.file)

    def work_with_file(self, file):
        print(self.num_qw)
        with open(file, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            line_list = []
            for line in reader:
                line_list.append(line)
            self.len = len(line_list)
            if self.num_qw <= len(line_list):
                self.my_list = line_list[self.num_qw - 1]
                self.plainTextEdit.clear()
                self.plainTextEdit.insertPlainText(self.my_list[0])
                self.label_2.setText(f'Вопрос № {self.num_qw}')
                self.num_qw += 1
                self.radioButton_4.setText(self.my_list[1])
                self.radioButton_3.setText(self.my_list[2])
                self.radioButton_2.setText(self.my_list[3])
                self.radioButton.setText(self.my_list[4])
                self.answer_b = self.my_list[int(self.my_list[-1])]
            else:
                self.label_5.show()
                self.pushButton_4.show()
                self.label_5.setText(f'Верно решено {self.true} из {self.len}')


    def plus_true(self):
        self.true += 1
        self.label_3.setText(f'Верно: {self.true}')

    def answer(self):
        if self.radioButton.isChecked() and int(self.my_list[-1]) == self.dicti[self.radioButton]:
            self.plus_true()
            self.work_with_file(self.file)
        elif self.radioButton_2.isChecked() and int(self.my_list[-1]) == self.dicti[self.radioButton_2]:
            self.plus_true()
            self.work_with_file(self.file)
        elif self.radioButton_3.isChecked() and int(self.my_list[-1]) == self.dicti[self.radioButton_3]:
            self.plus_true()
            self.work_with_file(self.file)
        elif self.radioButton_4.isChecked() and int(self.my_list[-1]) == self.dicti[self.radioButton_4]:
            self.plus_true()
            self.work_with_file(self.file)
        else:
            self.true_answer()

    def true_answer(self):
        self.label_4.setText(self.answer_b)
        self.work_with_file(self.file)

    def entrance(self):
        self.open_game = Entrance()
        self.open_game.show()
        self.hide()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Entrance()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
