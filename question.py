import sys
from random import randint
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLineEdit, QDesktopWidget, QLabel, QLayout
from PyQt5 import QtGui
import sqlite3


class Quest(QWidget):
    def __init__(self, db='questions.db'):
        super().__init__()
        self.db = db
        self.num = 26
        con = sqlite3.connect('questions.db')
        cur = con.cursor()
        self.res = cur.execute(f'''SELECT question, a, b, c, ans FROM questions WHERE id == {self.num}''').fetchall()
        self.corr = None
        con.close()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 450)
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())
        self.setWindowTitle('Question')
        self.a = QPushButton(f'a) {self.res[0][1]}', self)
        self.a.move(50, 300)
        self.a.resize(200, 50)
        self.a.clicked.connect(lambda:self.hello(ans='a'))
        self.b = QPushButton(f'b) {self.res[0][2]}', self)
        self.b.move(300, 300)
        self.b.resize(200, 50)
        self.b.clicked.connect(lambda:self.hello(ans='b'))
        self.c = QPushButton(f'c) {self.res[0][3]}', self)
        self.c.move(550, 300)
        self.c.resize(200, 50)
        self.c.clicked.connect(lambda:self.hello(ans='c'))
        self.label = QLabel(self)
        self.label.setText(self.res[0][0])
        self.label.move(20, 60)
        self.label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

    def hello(self, ans):
        if self.res[0][4] == 'а':
            print('пе')
        if self.iscorrect(ans):
            self.corr = True
        else:
            self.corr = False
        print(self.iscorrect(ans))
        print(self.res)


    def iscorrect(self, n=''):
        if n != self.res[0][4]:
            return False
        else:
            return True


app = QApplication(sys.argv)
ex = Quest()
ex.show()
sys.exit(app.exec())