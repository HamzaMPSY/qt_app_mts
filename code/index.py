from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
from os import path
import numpy as np
import datetime


LOGIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/login.ui"))
ADMIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/admin.ui"))

class MainApp(QMainWindow,LOGIN_UI):
    """docstring for MainApp"""

    switchWindow = pyqtSignal(str)

    def __init__(self, arg=None):
        super(MainApp, self).__init__(arg)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleUI()
        self.handleLogin()
        

    def handleUI(self):
        self.setWindowTitle('MTS Scanner')
        self.setFixedSize(900,575)
        self.setWindowIcon(QIcon('../assets/logo-scroll.png'))
    
    def handleLogin(self):
        self.btnlogin.clicked.connect(self.login)

    def login(self):
        login = self.QTxtLogin.text()
        password = self.QTxtPass.text()
        if login == '' or password == '':
            QMessageBox.warning(self,"Error","Please complete all fields!")
        elif login=='admin' and password == "admin":
            self.switchWindow.emit(login)
        else:
            QMessageBox.warning(self,"dzl","chkon nta ???")


class Admin(QMainWindow,ADMIN_UI):
    switchWindow = pyqtSignal()

    def __init__(self, login,arg=None,):
        super(Admin, self).__init__(arg)
        QWidget.__init__(self)
        self.setupUi(self)
        self.login = login
        self.handleUI()
        self.handleButtons()
        self.handleHeaders()

    def handleUI(self):
        self.setWindowTitle('MTS Scanner : Admin Control Panel')
        self.setFixedSize(900,575)
        self.setWindowIcon(QIcon('../assets/logo-scroll.png'))

    def handleButtons(self):
        self.btnlogout.clicked.connect(self.logout)
        self.btnusers.clicked.connect(self.users)

    def handleHeaders(self):
        date = datetime.datetime.now()
        self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
        self.usernameLabel.setText(self.login)

    def logout(self):
        self.switchWindow.emit()
        
    def users(self):
        

class Controller:

    def __init__(self):
        self.login = MainApp()
        self.admin = Admin(login = '')

    def showLogin(self):
        self.login.QTxtLogin.setText('')
        self.login.QTxtPass.setText('')
        self.login.switchWindow.connect(self.showAdmin)
        self.admin.close()
        self.login.show()

    def showAdmin(self,text):
        self.admin = Admin(login = text)
        self.admin.switchWindow.connect(self.showLogin)
        self.login.close()
        self.admin.show()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.showLogin()
    app.exec_()

if __name__ == '__main__':
    main()    
