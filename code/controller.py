from windows import *
import pandas as pd
from SerialPort import *
import time

class Controller:
    def __init__(self):
        self.login = MainApp()
        self.admin = Admin(login = '')
        self.user = User(login = '')
        self.scan = Scan(text = '')
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
        self.user.QTxtQuan.setText('')
        self.user.QTxtRef.setText('')
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
                self.user.switchWindow2.connect(self.showScan)
                self.user.loaded = True
            
            self.login.close()
            self.user.show()

    def sendToOutput(self,data):
        print('[+]Sending',data,'to serial port')
        self.serialPort.writeSerialPort(data)

    def showScan(self,text):
        self.scan.login = text.split(';')[0]
        self.scan.reference = text.split(';')[1]
        self.scan.quantity = int(text.split(';')[2])
        self.scan.handleHeaders()
        if not self.scan.loaded:
            self.scan.switchWindow.connect(self.showUser)
            self.scan.loaded = True

        self.serialPort = SerialPort()
        self.serialPort.moveToThread(self.serialThread)
        self.serialPort.signal.connect(self.scan.recieveData)
        self.serialThread.started.connect(self.serialPort.readSerialPort)
        self.serialThread.setTerminationEnabled(True)
        self.serialThread.start()
        self.user.close()
        self.scan.show()