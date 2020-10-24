from PyQt5.QtWidgets import QApplication
from controller import *
import sys
from pyqt5_material import apply_stylesheet

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml',light_secondary=True)
    controller = Controller()
    controller.showLogin()
    app.exec_()

if __name__ == '__main__':
    main()