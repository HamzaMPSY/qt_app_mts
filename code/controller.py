from windows import *
import pandas as pd
import serial

class Controller:
    def __init__(self):
        self.login = MainApp()
        self.admin = Admin(login = '')
        self.user = User(login = '')

    def showLogin(self):
        self.login.QTxtLogin.setText('')
        self.login.QTxtPass.setText('')
        self.login.switchWindow.connect(self.showUser)
        self.admin.close()
        self.user.close()
        self.login.show()

    def showUser(self,text):
        users = pd.read_csv('../files/users.csv')
        res = users[(users['username'] == text)]
        if res['isadmin'].item() == 1:
            self.admin = Admin(login = text)
            self.admin.switchWindow.connect(self.showLogin)
            self.login.close()
            self.admin.show()
        else :
            self.user = User(login = text)
            self.user.switchWindow.connect(self.showLogin)
            self.user.sendOutput.connect(self.sendToOutput)
            self.login.close()
            self.user.show()

    def sendToOutput(self,text):
        #users = pd.read_csv('../files/pins.csv')
        #res = users[(users['purpose'] == 'output')]
        #name = res['name'].item()
        #ComPort = serial.Serial(name)
        print(text)
