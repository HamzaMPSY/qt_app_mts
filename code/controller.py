from windows import *
import pandas as pd
from SerialPort import *


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
            self.serialPort = SerialPort()
            self.user = User(login = text)
            self.user.switchWindow.connect(self.showLogin)
            self.user.sendOutput.connect(self.sendToOutput)
            self.serialThread = QThread()
            self.serialPort.moveToThread(self.serialThread)
            self.serialPort.signal.connect(self.user.recieveData)
            self.serialThread.started.connect(self.serialPort.readSerialPort)
            self.serialThread.start()
            self.login.close()
            self.user.show()

    def sendToOutput(self,data):
        print('[+]Sending',data,'to serial port')
        self.serialPort.writeSerialPort(data)