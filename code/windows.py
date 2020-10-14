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



LOGIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/login.ui"))
ADMIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/admin.ui"))

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
                if res['isadmin'].item() == 1: 
                    self.switchWindow.emit(login)
                else:
                    QMessageBox.information(self,"Mazal maderna blasa lik ","Tsena tatsnsaliw admin")
            else:
                QMessageBox.warning(self,"Error","Login or Password incorrect!")
        

class Admin(QMainWindow,ADMIN_UI):
    switchWindow = pyqtSignal()
    click_flag = True
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
        self.btnhistory.clicked.connect(self.historys)
        self.btnadduser.hide()
        self.btnadduser.clicked.connect(self.adduser)

    def handleHeaders(self):
        date = datetime.datetime.now()
        self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
        self.usernameLabel.setText(self.login)

    def logout(self):
        logs(self.login, "logout")
        self.switchWindow.emit()

    def users(self):
        self.btnadduser.show()
        users = pd.read_csv('../files/users.csv')
        model = pandasModel(users)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.click_flag:
            self.tableView.clicked.connect(self.modifyUser)
            self.click_flag = False

    def historys(self):
        self.btnadduser.hide()
        logs = pd.read_csv('../files/logins.csv')
        model = pandasModel(logs)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.clicked.disconnect()
        self.click_flag = True

        
    def modifyUser(self,item):
        row = item.row()
        res = pd.read_csv('../files/users.csv').iloc[row,:]
        username = res['username']
        password = res['password']
        isadmin = res['isadmin']
        editDialog = EditDialog(username,password,isadmin,row,self.login)
        editDialog.exec_()
        editDialog.close()
        self.users()

    def adduser(self):
        editDialog = AddDialog(self.login)
        editDialog.exec_()
        editDialog.close()
        self.users()