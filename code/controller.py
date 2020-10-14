from windows import *

class Controller:
    def __init__(self):
        self.login = MainApp()
        self.admin = Admin(login = '')
        self.isadmin = False

    def showLogin(self):
        self.login.QTxtLogin.setText('')
        self.login.QTxtPass.setText('')
        self.login.switchWindow.connect(self.showAdmin)
        self.admin.close()
        self.login.show()

    def showAdmin(self,text):
        self.admin = Admin(login = text)
        self.admin.switchWindow.connect(self.showLogin)
        self.login.close()
        self.admin.show()
