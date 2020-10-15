from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import path
import pandas as pd
import datetime
from pandasModel import *
from dialogs import *
import os
import time



LOGIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/login.ui"))
ADMIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/admin.ui"))
USER_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/user.ui"))

def logs(username, action):
    path = '../files/logins.csv'
    if not os.path.isfile(path):
        logs = open(path, 'w')
        logs.write("username,date,action\n")
        logs.close()
    logs = open(path, 'a')
    date = datetime.datetime.now()
    line = username + "," + date.strftime("%Y/%m/%d %H:%M") + "," + action + "\n" 
    logs.write(line)
    logs.close()

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
        else:
            users = pd.read_csv('../files/users.csv')
            res = users[(users['username'] == login) & (users['password'] == password)]
            if res.shape[0] >= 1 :
                logs(login, "login") 
                self.switchWindow.emit(login)
            else:
                QMessageBox.warning(self,"Error","Login or Password incorrect!")
        

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
        self.users_click_flag = True
        self.pins_click_flag = True
        self.ref_click_flag = True

    def handleUI(self):
        self.setWindowTitle('MTS Scanner : Admin Control Panel')
        self.setFixedSize(900,575)
        self.setWindowIcon(QIcon('../assets/logo-scroll.png'))

    def handleButtons(self):
        self.btnlogout.clicked.connect(self.logout)
        self.btnusers.clicked.connect(self.users)
        self.btnhistory.clicked.connect(self.history)
        self.btnadduser.hide()
        self.btnpins.clicked.connect(self.pins)
        self.btnreferences.clicked.connect(self.references)

    def handleHeaders(self):
        date = datetime.datetime.now()
        self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
        self.usernameLabel.setText(self.login)

    def logout(self):
        logs(self.login, "logout")
        self.switchWindow.emit()

    def users(self):
        self.btnadduser.show()
        self.btnadduser.setText('Add user')
        try:
            self.btnadduser.clicked.disconnect()
        except Exception :
            pass
        self.btnadduser.clicked.connect(self.adduser)
        users = pd.read_csv('../files/users.csv')
        model = pandasModel(users)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.users_click_flag:
            try:
                self.tableView.clicked.disconnect()
            except Exception:
                pass
            self.tableView.clicked.connect(self.modifyUser)
            self.users_click_flag = False
        self.pins_click_flag = True
        self.ref_click_flag = True

    def history(self):
        self.btnadduser.hide()
        logs = pd.read_csv('../files/logins.csv')
        model = pandasModel(logs)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        try:
            self.tableView.clicked.disconnect()
        except Exception:
            pass
        self.users_click_flag = True
        self.pins_click_flag = True
        self.ref_click_flag = True

        
    def modifyUser(self,item):
        row = item.row()
        editDialog = EditDialog(row,self.login)
        editDialog.setWindowTitle('Edit User')
        editDialog.setWindowIcon(QIcon('../assets/logo-scroll.png'))
        editDialog.exec_()
        editDialog.close()
        self.users()

    def adduser(self):
        addUserDialog = AddDialog(self.login)
        addUserDialog.setWindowTitle('Add User')
        addUserDialog.setWindowIcon(QIcon('../assets/logo-scroll.png'))
        addUserDialog.exec_()
        addUserDialog.close()
        self.users()

    def pins(self):
        self.btnadduser.show()
        self.btnadduser.setText('add pin')
        try:
            self.btnadduser.clicked.disconnect()
        except Exception :
            pass
        self.btnadduser.clicked.connect(self.addpin)
        pins = pd.read_csv('../files/pins.csv')
        model = pandasModel(pins)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.pins_click_flag:
            try:
                self.tableView.clicked.disconnect()
            except Exception:
                pass
            self.tableView.clicked.connect(self.modifypin)
            self.pins_click_flag = False
        self.users_click_flag = True
        self.ref_click_flag = True

    def modifypin(self,item):
        row = item.row()
        editPin = PinDialog(row,self.login)
        editPin.setWindowTitle('Edit Pin')
        editPin.setWindowIcon(QIcon('../assets/logo-scroll.png'))
        editPin.exec_()
        editPin.close()
        self.pins()

    def addpin(self):
        addPin = AddPinDialog(self.login)
        addPin.setWindowTitle('Add Pin')
        addPin.setWindowIcon(QIcon('../assets/logo-scroll.png'))
        addPin.exec_()
        addPin.close()
        self.pins()

    def references(self):
        self.btnadduser.show()
        self.btnadduser.setText('add refrerence')
        try:
            self.btnadduser.clicked.disconnect()
        except Exception :
            pass
        self.btnadduser.clicked.connect(self.addrefrence)
        refereces = pd.read_csv('../files/references.csv')
        model = pandasModel(refereces)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.ref_click_flag:
            try:
                self.tableView.clicked.disconnect()
            except Exception:
                pass
            self.tableView.clicked.connect(self.modifyref)
            self.ref_click_flag = False
        self.users_click_flag = True
        self.pins_click_flag = True

    def modifyref(self,item):
        row = item.row()
        editRef = EditRefDialog(row,self.login)
        editRef.setWindowTitle('Edit Reference')
        editRef.setWindowIcon(QIcon('../assets/logo-scroll.png'))
        editRef.exec_()
        editRef.close()
        self.references()

    def addrefrence(self):
        addRef = AddRefDialog(self.login)
        addRef.setWindowTitle('Add Reference')
        addRef.setWindowIcon(QIcon('../assets/logo-scroll.png'))
        addRef.exec_()
        addRef.close()
        self.references()

class User(QMainWindow,USER_UI):
    switchWindow = pyqtSignal()
    sendOutput = pyqtSignal(str)

    def __init__(self, login,arg=None,):
        super(User, self).__init__(arg)
        QWidget.__init__(self)
        self.setupUi(self)
        self.login = login
        self.handleUI()
        self.handleButtons()
        self.handleHeaders()

    def handleUI(self):
        self.setWindowTitle('MTS Scanner : User')
        self.setFixedSize(900,575)
        self.setWindowIcon(QIcon('../assets/logo-scroll.png'))

    def handleButtons(self):
        self.btnLogout.clicked.connect(self.logout)
        self.btnSend.clicked.connect(self.send)

    def handleHeaders(self):
        date = datetime.datetime.now()
        self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
        self.usernameLabel.setText(self.login)

    def logout(self):
        logs(self.login, "logout")
        self.switchWindow.emit()

    def send(self):
        tosend = self.lineEdit.text()
        if tosend == '':
            QMessageBox.warning(self,"Error","Please fill referece product field!")
        else:
            self.sendOutput.emit(tosend)

    def recieveData(self,data):
        self.btnRv.setText(data)
        self.btnRv.setStyleSheet("background-color: lightgreen")
        time.sleep(0.5)
