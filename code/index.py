from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
from os import path
import torch
import numpy as np

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"ui/main.ui"))

def test1():
	print('it works')

class MainApp(QMainWindow,FORMCLASS):
    """docstring for MainApp"""
    def init(self, arg=None):
        super(MainApp, self).init(arg)
        QMainWindow.init(self)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()

if name == 'main':
    main()