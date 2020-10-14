import serial
from PyQt5.QtCore import *
import time
import pandas as pd

class SerialPort(QObject):
    
    def __init__(self, parent = None):
        super(SerialPort, self).__init__(parent)
        #initialization and open the port
        pins = pd.read_csv('../files/pins.csv')
        res = pins[(pins['purpose'] == 'output')]
        portName = res['name'].item()
        self.ComPort = None
        try:
            self.ComPort = serial.Serial(portName,9600,timeout=0)
        except Exception as e:
            print('could not open port "%s"'%portName)

    # Explicit signal
    signal = pyqtSignal(str)

    #@pyqtSlot(str)
    def readSerialPort(self):
        print ("Starting up...")
        if self.ComPort is not None:
            while True:
                readOut = self.ComPort.read(268)  # Reads # Bytes
                # r = binascii.hexlify(readOut).decode('ascii')
                print(readOut)
                data = readOut.decode()
                if data != "":
                    self.signal.emit(data)
                time.sleep(1)
            if not self.ComPort.isOpen():
                print("Serial Port is Close")
    
    def writeSerialPort(self,data):
        if self.ComPort is not None:
            self.ComPort.write(data.encode())