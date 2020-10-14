from PyQt5.QtWidgets import *
import pandas as pd
from PyQt5.QtCore import Qt
import os
import datetime
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

class EditDialog(QDialog):
    def __init__(self,row,login, parent=None):
        super().__init__(parent)
        self.login = login
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.isadmin = QLineEdit(self)
        self.row=row
        res = pd.read_csv('../files/users.csv').iloc[row,:]
        username = res['username']
        password = res['password']
        isadmin = res['isadmin']
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

        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)
        buttonBox.helpRequested.connect(self.delete)

    def save(self):
        df = pd.read_csv('../files/users.csv')
        df.ix[self.row,'username'] = self.username.text()
        df.ix[self.row,'password'] = self.password.text()
        df.ix[self.row,'isadmin'] = self.isadmin.text()
        df.to_csv('../files/users.csv',index=False)
        logs(self.login,"Edit user :"+self.username.text())
        self.close()

    def delete(self):
        df = pd.read_csv('../files/users.csv')
        df = df.drop([self.row],axis = 0)
        df.to_csv('../files/users.csv',index=False)
        logs(self.login,"Delete user :"+self.username.text())
        self.close()

    def cancel(self):
        self.close()


class AddDialog(QDialog):
    def __init__(self,login, parent=None):
        super().__init__(parent)
        self.login = login
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.isadmin = QLineEdit(self)
        
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        layout = QFormLayout(self)
        layout.addRow("Username :", self.username)
        layout.addRow("Password :", self.password)
        layout.addRow("Is Admin :", self.isadmin)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)

    def save(self):
        df = pd.read_csv('../files/users.csv')
        df.loc[df.shape[0]+1] = [self.username.text(),self.password.text(),self.isadmin.text()]
        df.to_csv('../files/users.csv',index=False)
        logs(self.login,"Add user :"+self.username.text())
        self.close()

    def cancel(self):
        self.close()

class PinDialog(QDialog):
    def __init__(self,row,login, parent=None):
        super().__init__(parent)
        self.login = login
        self.purpose = QLineEdit(self)
        self.name = QLineEdit(self)
        self.row=row
        res = pd.read_csv('../files/pins.csv').iloc[row,:]
        purpose = res['purpose']
        name = res['name']
        self.purpose.setText(purpose)
        self.name.setText(name)
       
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        layout = QFormLayout(self)
        layout.addRow("Purpose :", self.purpose)
        layout.addRow("Name :", self.name)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)

    def save(self):
        df = pd.read_csv('../files/pins.csv')
        df.ix[self.row,'purpose'] = self.purpose.text()
        df.ix[self.row,'name'] = self.name.text()
        df.to_csv('../files/pins.csv',index=False)
        logs(self.login,"Edit user :"+self.purpose.text())
        self.close()

    def cancel(self):
        self.close()


class AddRefDialog(QDialog):
    def __init__(self,login, parent=None):
        super().__init__(parent)
        self.login = login
        self.reference = QLineEdit(self)
        self.code = QLineEdit(self)
        
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        layout = QFormLayout(self)
        layout.addRow("Reference :", self.reference)
        layout.addRow("Code :", self.code)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)

    def save(self):
        df = pd.read_csv('../files/references.csv')
        df.loc[df.shape[0]+1] = [self.reference.text(),self.code.text()]
        df.to_csv('../files/references.csv',index=False)
        logs(self.login,"Add reference :"+self.reference.text())
        self.close()

    def cancel(self):
        self.close()


class EditRefDialog(QDialog):
    def __init__(self,row,login, parent=None):
        super().__init__(parent)
        self.login = login
        self.reference = QLineEdit(self)
        self.code = QLineEdit(self)
        self.row=row
        res = pd.read_csv('../files/references.csv').iloc[row,:]
        reference = res['reference']
        code = res['code']
        self.reference.setText(reference)
        self.code.setText(str(code))
        
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("Delete", QDialogButtonBox.HelpRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        layout = QFormLayout(self)
        layout.addRow("reference :", self.reference)
        layout.addRow("code :", self.code)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)
        buttonBox.helpRequested.connect(self.delete)

    def save(self):
        df = pd.read_csv('../files/references.csv')
        df.ix[self.row,'reference'] = self.reference.text()
        df.ix[self.row,'code'] = self.code.text()
        df.to_csv('../files/references.csv',index=False)
        logs(self.login,"Edit Reference :"+self.reference.text())
        self.close()

    def delete(self):
        df = pd.read_csv('../files/references.csv')
        df = df.drop([self.row],axis = 0)
        df.to_csv('../files/references.csv',index=False)
        logs(self.login,"Delete Reference :"+self.reference.text())
        self.close()

    def cancel(self):
        self.close()

class AddPinDialog(QDialog):
    def __init__(self,login, parent=None):
        super().__init__(parent)
        self.login = login
        self.purpose = QLineEdit(self)
        self.name = QLineEdit(self)
        
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton("Save", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        layout = QFormLayout(self)
        layout.addRow("Purpose :", self.purpose)
        layout.addRow("Name :", self.name)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)

    def save(self):
        df = pd.read_csv('../files/pins.csv')
        df.loc[df.shape[0]+1] = [self.purpose.text(),self.name.text()]
        df.to_csv('../files/pins.csv',index=False)
        logs(self.login,"Add pin :"+self.purpose.text())
        self.close()

    def cancel(self):
        self.close()