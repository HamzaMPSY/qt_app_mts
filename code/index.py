from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
from os import path
import numpy as np
import pandas as pd
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
        else:
            users = pd.read_csv('../files/users.csv',delimiter=";")
            res = users[(users['username'] == login) & (users['password'] == password)]
            # print(res.shape)
            if res.shape[0] >= 1 :
                if res['isadmin'].item() == 1: 
                    self.switchWindow.emit(login)
                else:
                    QMessageBox.information(self,"Mazal maderna blasa lik ","Tsena tatsnsaliw admin")
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
        users = pd.read_csv('../files/users.csv',delimiter =";")
        model = pandasModel(users)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.clicked.connect(self.modifyUser)

    def modifyUser(self,item):
        row = item.row()
        res = pd.read_csv('../files/users.csv',delimiter=";").iloc[row,:]
        username = res['username']
        password = res['password']
        isadmin = res['isadmin']
        editDialog = EditDialog(username,password,isadmin,row)
        editDialog.exec_()
        self.users()
  
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

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class EditDialog(QDialog):
    def __init__(self, username,password,isadmin,row, parent=None):
        super().__init__(parent)

        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.isadmin = QLineEdit(self)
        self.row=row
        self.username.setText(username)
        self.password.setText(password)
        self.isadmin.setText(str(isadmin))
        
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("Delete", QDialogButtonBox.HelpRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        layout = QFormLayout(self)
        layout.addRow("Username :", self.username)
        layout.addRow("Password :", self.password)
        layout.addRow("Is Admin :", self.isadmin)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        # buttonBox.helpRequested.connect(self.delete)

        def accept(self):
            df = pd.read_csv('../files/users.csv',delimiter=";")
            df[self.row,'username'] = self.username.text()
            df[self.row,'password'] = self.password.text()
            df[self.row,'isadmin'] = int(self.isadmin.text())
            df.to_csv('../files/users.csv',index=False)

        def delete(self):
            pass

        def reject(self):
            pass

    def getInputs(self):
        return (self.first.text(), self.second.text())

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.showLogin()
    app.exec_()

if __name__ == '__main__':
    main()    
