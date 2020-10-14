from windows import *
import pandas as pd
import serial

class Controller:
    def __init__(self):
        self.login = MainApp()
        self.admin = Admin(login = '')
        self.user = User(login = '')
        self.conectToSrial()

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
            self.conectToSrial()
            self.user = User(login = text)
            self.user.switchWindow.connect(self.showLogin)
            self.user.sendOutput.connect(self.sendToOutput)
            self.login.close()
            self.user.show()

    def conectToSrial(self):
        pins = pd.read_csv('../files/pins.csv')
        res = pins[(pins['purpose'] == 'output')]
        self.outputName = res['name'].item()
        try:
            self.ComPort = serial.Serial(self.outputName)
        except Exception :
            print('could not open port "{1}"',self.outputName)
        
    
    def sendToOutput(self,text):
        references = pd.read_csv('../files/references.csv')
        res = references[(references['reference'] == text)]
        data = res['code'].item()
        try:
            self.ComPort.write(data.encode())
        except Exception :
            print('could not send to port "{1}"',self.outputName)
        
