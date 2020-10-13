from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
from os import path
import numpy as np


FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"../ui/login.ui"))

class MainApp(QMainWindow,FORM_CLASS):
    """docstring for MainApp"""
    def __init__(self, arg=None):
        super(MainApp, self).__init__(arg)
        QMainWindow.__init__(self)
        self.setupUi(self)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()    
