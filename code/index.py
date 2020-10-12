from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
from os import path
import torch
import numpy as np

FORM_CLASS,_= loadUiType(r"C:/Users/Otman/Desktop/PLC/qt_app_mts/ui/login.ui")

def test1():
	print('it works')

class MainApp(QMainWindow,FORM_CLASS):
    """docstring for MainApp"""
    def init(self, arg=None):
        super(MainApp, self).init(arg)
        QMainWindow.init(self)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


def ui():
	print('test')

if __name__ == '__main__':
    print(path.join(path.dirname(__file__),"ui\main.ui"))
    main()    