from windows import *
import pandas as pd
from SerialPort import *
import time

import os
home_path = os.path.dirname(os.path.realpath(__file__))

class Controller:
    def __init__(self):
        self.login = MainApp()
        self.cpuThread = QThread()
        self.scannerThread = QThread()
        self.open_admin = False
        self.open_user = False
        self.open_stats = False
        self.cpu = SerialPort('CPU')
        self.scanner = SerialPort('Scanner')
        self.cpu.moveToThread(self.cpuThread)
        self.scanner.moveToThread(self.scannerThread)

    def showLogin(self):
        if self.cpu.ComPort is None:
            self.cpu.portConnect()
        try:
            self.cpu.close()
        except Exception as e:
            print("Error Port :",e)

        if self.scanner.ComPort is None:
            self.scanner.portConnect()
        try:
            self.scanner.close()
        except Exception as e:
            print("Error Port:",e)

        self.login.QTxtLogin.setText('')
        self.login.QTxtPass.setText('')
        if not self.login.loaded:
            self.login.switchWindow.connect(self.showUser)
            self.login.loaded = True
        if self.open_admin:    
            self.admin.close()
        if self.open_user:
            self.user.close()
        self.login.show()

    def showUser(self,text):
        try:
            self.cpuThread.started.disconnect()
            self.cpuThread.terminate()
            self.scannerThread.started.disconnect()
            self.scannerThread.terminate()
        except Exception as e:
            print(e)
        users = pd.read_csv(home_path[:-4]+'/files/users.csv')
        res = users[(users['username'] == text)]
        if res['username'].item() == "admin":
            if not self.open_admin:
                self.admin = Admin('')
                self.open_admin = True
            self.admin.login = text
            self.admin.handleHeaders()
            if not self.admin.loaded:
                self.admin.switchWindow.connect(self.showLogin)
                self.admin.switchWindow2.connect(self.showStats)
                self.admin.loaded = True
            if self.open_stats:
                self.stats.close()
            self.login.close()
            self.admin.show()
        else :
            if not self.open_user:
                self.user = User('')
                self.open_user = True
            self.user.QTxtRef.setText('')
            self.user.login = text
            self.user.handleHeaders()
            self.user.handleUI()
            if not self.user.loaded:
                self.user.switchWindow.connect(self.showLogin)
                self.user.switchWindow2.connect(self.showStats)
                self.user.sendsignal.connect(self.sendToOutput)
                self.user.loaded = True
            self.cpu.open()
            self.scanner.open()
            if not self.cpu.is_connected:
                self.cpu.signal.connect(self.user.recieveData)
                self.cpu.is_connected = True
            if not self.scanner.is_connected:
                self.scanner.signal.connect(self.user.recieveData)
                self.scanner.is_connected = True
            self.cpuThread.started.connect(self.cpu.readSerialPort)
            self.scannerThread.started.connect(self.scanner.readSerialPort)
            self.cpuThread.setTerminationEnabled(True)
            self.cpuThread.start()
            self.scannerThread.setTerminationEnabled(True)
            self.scannerThread.start()
            self.login.close()
            if self.open_stats:
                self.stats.close()
            self.user.show()

    def sendToOutput(self,data):
        print('[+]Sending',data,'to serial port')
        self.cpu.writeSerialPort(data)

    def showScan(self,text):
        if not self.open_scan:
            self.scan = Scan('')
            self.open_scan = True
        self.scan.login = text.split(';')[0]
        self.scan.reference = text.split(';')[1]
        self.scan.quantity = int(text.split(';')[2])
        self.scan.processed = 0
        self.scan.handleHeaders()
        self.scan.handel_progressBar()
        if not self.scan.loaded:
            self.scan.switchWindow.connect(self.showUser)
            self.scan.loaded = True

        self.cpu.moveToThread(self.cpuThread)
        self.cpu.signal.connect(self.scan.recieveData)
        self.cpuThread.started.connect(self.cpu.readSerialPort)
        self.cpuThread.setTerminationEnabled(True)
        self.cpuThread.start()

        self.scanner.moveToThread(self.scannerThread)
        self.scanner.signal.connect(self.scan.recieveData)
        self.scannerThread.started.connect(self.scanner.readSerialPort)
        self.scannerThread.setTerminationEnabled(True)
        self.scannerThread.start()

        self.user.close()
        time.sleep(0.5)
        self.scan.show()

    def showStats(self,text):
        try:
            self.serialPort.close()
        except Exception as e:
            print("error PORT :",e)
        if not self.open_stats:
            self.stats = Statistics('')
            self.open_stats = True
        self.stats.login = text
        self.stats.handleHeaders()
        if not self.stats.loaded:
            self.stats.switchWindow.connect(self.showUser)
            self.stats.loaded = True
        self.stats.show()
        if self.open_admin:
            self.admin.close()
        if self.open_user:
            self.user.close()