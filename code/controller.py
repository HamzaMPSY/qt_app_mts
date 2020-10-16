from windows import *
import pandas as pd
from SerialPort import *
import time

class Controller:
    def __init__(self):
        self.login = MainApp()
        self.admin = Admin(login = '')
        self.user = User(login = '')
        self.serialThread = QThread()


    def showLogin(self):
        self.login.QTxtLogin.setText('')
        self.login.QTxtPass.setText('')
        if not self.login.loaded:
            self.login.switchWindow.connect(self.showUser)
            self.login.loaded = True
        self.admin.close()
        self.user.close()
        self.login.show()

    def showUser(self,text):
        try:
            self.serialThread.started.disconnect()
            self.serialThread.terminate()
        except Exception as e:
            print(e)
        users = pd.read_csv('../files/users.csv')
        res = users[(users['username'] == text)]
        if res['isadmin'].item() == 1:
            self.admin.login = text
            self.admin.handleHeaders()
            if not self.admin.loaded:
                self.admin.switchWindow.connect(self.showLogin)
                self.admin.loaded = True
            self.login.close()
            self.admin.show()
        else :
            self.user.login = text
            self.user.handleHeaders()
            if not self.user.loaded:
                self.user.switchWindow.connect(self.showLogin)
                self.user.sendOutput.connect(self.sendToOutput)
                self.user.loaded = True
            
            self.serialPort = SerialPort()
            self.serialPort.moveToThread(self.serialThread)
            self.serialPort.signal.connect(self.user.recieveData)
            self.serialThread.started.connect(self.serialPort.readSerialPort)
            self.serialThread.setTerminationEnabled(True)
            self.serialThread.start()
            self.login.close()
            self.user.show()

    def sendToOutput(self,data):
        print('[+]Sending',data,'to serial port')
        self.serialPort.writeSerialPort(data)