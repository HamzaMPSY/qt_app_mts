from PyQt5.QtWidgets import *
import pandas as pd
from PyQt5.QtCore import Qt

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

        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(self.cancel)
        buttonBox.helpRequested.connect(self.delete)

    def save(self):
        df = pd.read_csv('../files/users.csv')
        df.ix[self.row,'username'] = self.username.text()
        df.ix[self.row,'password'] = self.password.text()
        df.ix[self.row,'isadmin'] = self.isadmin.text()
        df.to_csv('../files/users.csv',index=False)
        self.close()

    def delete(self):
        df = pd.read_csv('../files/users.csv')
        df = df.drop([self.row],axis = 0)
        df.to_csv('../files/users.csv',index=False)
        self.close()

    def cancel(self):
        self.close()


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.close()
        
    def cancel(self):
        self.close()
