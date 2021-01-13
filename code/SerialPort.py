import serial
from PyQt5.QtCore import *
import time
import pandas as pd
import os
home_path = os.path.dirname(os.path.realpath(__file__))

class SerialPort(QObject):
    
    def __init__(self, purpose , parent = None):
        super(SerialPort, self).__init__(parent)
        #initialization and open the port
        pins = pd.read_csv(home_path[:-4]+'/files/settings.csv')
        res = pins[(pins['purpose'] == purpose)]
        self.portName = res['name'].item()
        self.ComPort = None
        self.portConnect()
        self.is_connected = False

    def portConnect(self):
        try:
            self.ComPort = serial.Serial(self.portName,9600,timeout=0,rtscts=True,dsrdtr=True)
        except Exception as e:
            print('could not connect with port "%s"'%self.portName)

    # Explicit signal
    signal = pyqtSignal(str)

    def readSerialPort(self):
        print ("Start reading from port")
        if self.ComPort is not None:
            while True:
                try:
                    readOut = self.ComPort.read(268)
                    data = readOut.decode().strip()
                    print(readOut)
                    if data != "":
                        self.signal.emit(data)
                except Exception as e:
                    self.open()
                time.sleep(1)
        print ("Finish reading from port")
    
    def writeSerialPort(self,data):
        try:
            if self.ComPort is not None:
                self.ComPort.write(data.encode())
        except Exception as e:
            print("Port not connect yet")

    def open(self):
        try:
            self.ComPort.open()
        except Exception as e:
            print("Cannot open this port", self.portName)

    def close(self):
        # if self.ComPort.is_open:
        self.ComPort.close()
