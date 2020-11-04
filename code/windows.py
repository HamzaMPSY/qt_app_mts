from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import path
import pandas as pd
import datetime
from pandasModel import *
from dialogs import *
from statistics import *
import os
import time


LOGIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/login.ui"))
ADMIN_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/admin.ui"))
USER_UI,_ = loadUiType(path.join(path.dirname(__file__),"../ui/user.ui"))
STATS_UI,_= loadUiType(path.join(path.dirname(__file__),"../ui/statistics.ui"))

home_path = os.path.dirname(os.path.realpath(__file__))

def logs(username, reference,response):
    path = home_path[:-4] + '/files/history.csv'
    if not os.path.isfile(path):
        logs = open(path, 'w')
        logs.write("username,date,reference,response\n")
        logs.close()
    logs = open(path, 'a')
    date = datetime.datetime.now()
    line = username + "," + date.strftime("%Y/%m/%d %H:%M") + "," + reference + "," + response +  "\n" 
    logs.write(line)
    logs.close()

class MainApp(QMainWindow,LOGIN_UI):
    switchWindow = pyqtSignal(str)

    def __init__(self, arg=None):
        super(MainApp, self).__init__(arg)
        QMainWindow.__init__(self)
        self.loaded = False
        self.setupUi(self)
        self.handleUI()
        self.handleLogin()
        
    def handleUI(self):
        self.setWindowTitle('Pick to light System')
        self.showMaximized()
        self.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        pix1 =  QPixmap(home_path[:-4] +'/assets/logo-s.png')
        self.logo1.setPixmap(pix1.scaled(self.logo1.size()))
        pix2 =  QPixmap(home_path[:-4] +'/assets/logo-c.jpg')
        self.logo2.setPixmap(pix2.scaled(self.logo1.size()))
    
    def handleLogin(self):
        self.btnlogin.clicked.connect(self.login)

    def login(self):
        login = self.QTxtLogin.text()
        password = self.QTxtPass.text()
        if login == '' or password == '':
            QMessageBox.warning(self,"Error","Please complete all fields!")
        else:
            users = pd.read_csv(home_path[:-4] +'/files/users.csv')
            res = users[(users['username'] == login) & (users['password'] == password)]
            if res.shape[0] >= 1 :
                # logs(login, "login") 
                self.switchWindow.emit(login)
            else:
                QMessageBox.warning(self,"Error","Login or Password incorrect!")
        
class Admin(QMainWindow,ADMIN_UI):
    switchWindow = pyqtSignal()
    switchWindow2 = pyqtSignal(str)

    def __init__(self, login,arg=None,):
        super(Admin, self).__init__(arg)
        QWidget.__init__(self)
        self.setupUi(self)
        self.loaded = False
        self.login = login
        self.handleUI()
        self.handleButtons()
        self.handleHeaders()
        self.users_click_flag = True
        self.pins_click_flag = True
        self.ref_click_flag = True

    def handleUI(self):
        self.setWindowTitle('Pick to light System : Admin Control Panel')
        self.showMaximized()
        self.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        pix1 =  QPixmap(home_path[:-4] +'/assets/logo-small.png')
        self.logo1.setPixmap(pix1.scaled(self.logo1.size()))
        pix2 =  QPixmap(home_path[:-4] +'/assets/logo-csmall.png')
        self.logo2.setPixmap(pix2.scaled(self.logo2.size()))
        QCoreApplication.processEvents()

    def handleButtons(self):
        self.btnlogout.clicked.connect(self.logout)
        self.btnusers.clicked.connect(self.users)
        self.btnhistory.clicked.connect(self.history)
        self.btnadduser.hide()
        self.btnpins.clicked.connect(self.pins)
        self.btnreferences.clicked.connect(self.references)
        self.stats.clicked.connect(self.statistics)

    def handleHeaders(self):
        date = datetime.datetime.now()
        self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
        self.usernameLabel.setText(self.login)

    def logout(self):
        # logs(self.login, "logout")
        self.switchWindow.emit()

    def users(self):
        self.btnadduser.show()
        self.btnadduser.setText('Add user')
        try:
            self.btnadduser.clicked.disconnect()
        except Exception :
            pass
        self.btnadduser.clicked.connect(self.adduser)
        users = pd.read_csv(home_path[:-4] +'/files/users.csv')
        model = pandasModel(users)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.users_click_flag:
            try:
                self.tableView.clicked.disconnect()
            except Exception:
                pass
            self.tableView.clicked.connect(self.modifyUser)
            self.users_click_flag = False
        self.pins_click_flag = True
        self.ref_click_flag = True

    def history(self):
        self.btnadduser.hide()
        logs = pd.read_csv(home_path[:-4] +'/files/history.csv')
        model = pandasModel(logs)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        try:
            self.tableView.clicked.disconnect()
        except Exception:
            pass
        self.users_click_flag = True
        self.pins_click_flag = True
        self.ref_click_flag = True

        
    def modifyUser(self,item):
        row = item.row()
        editDialog = EditDialog(row,self.login)
        editDialog.setWindowTitle('Edit User')
        editDialog.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        editDialog.resize(380,180)
        editDialog.exec_()
        editDialog.close()
        self.users()

    def adduser(self):
        addUserDialog = AddDialog(self.login)
        addUserDialog.setWindowTitle('Add User')
        addUserDialog.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        addUserDialog.resize(380,180)
        addUserDialog.exec_()
        addUserDialog.close()
        self.users()

    def pins(self):
        self.btnadduser.show()
        self.btnadduser.setText('add port')
        try:
            self.btnadduser.clicked.disconnect()
        except Exception :
            pass
        self.btnadduser.clicked.connect(self.addpin)
        pins = pd.read_csv(home_path[:-4] +'/files/settings.csv')
        model = pandasModel(pins)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.pins_click_flag:
            try:
                self.tableView.clicked.disconnect()
            except Exception:
                pass
            self.tableView.clicked.connect(self.modifypin)
            self.pins_click_flag = False
        self.users_click_flag = True
        self.ref_click_flag = True

    def modifypin(self,item):
        row = item.row()
        editPin = PinDialog(row,self.login,is_admin = True)
        editPin.setWindowTitle('Edit Port')
        editPin.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        editPin.resize(380,180)
        editPin.exec_()
        editPin.close()
        self.pins()

    def addpin(self):
        addPin = AddPinDialog(self.login)
        addPin.setWindowTitle('Add Port')
        addPin.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        addPin.resize(380,180)
        addPin.exec_()
        addPin.close()
        self.pins()

    def references(self):
        self.btnadduser.show()
        self.btnadduser.setText('add refrerence')
        try:
            self.btnadduser.clicked.disconnect()
        except Exception :
            pass
        self.btnadduser.clicked.connect(self.addrefrence)
        refereces = pd.read_csv(home_path[:-4] +'/files/references.csv')
        model = pandasModel(refereces)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True) 
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.ref_click_flag:
            try:
                self.tableView.clicked.disconnect()
            except Exception:
                pass
            self.tableView.clicked.connect(self.modifyref)
            self.ref_click_flag = False
        self.users_click_flag = True
        self.pins_click_flag = True

    def modifyref(self,item):
        row = item.row()
        editRef = EditRefDialog(row,self.login)
        editRef.setWindowTitle('Edit Reference')
        editRef.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        editRef.resize(380,180)
        editRef.exec_()
        editRef.close()
        self.references()

    def addrefrence(self):
        addRef = AddRefDialog(self.login)
        addRef.setWindowTitle('Add Reference')
        addRef.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        addRef.resize(380,180)
        addRef.exec_()
        addRef.close()
        self.references()


    def statistics(self):
        self.switchWindow2.emit(self.login)

class User(QMainWindow,USER_UI):
    switchWindow = pyqtSignal()
    switchWindow2 = pyqtSignal(str)
    sendsignal = pyqtSignal(str)
    def __init__(self, login,arg=None,):
        self.last_ref = ''
        super(User, self).__init__(arg)
        QWidget.__init__(self)
        self.setupUi(self)
        self.login = login
        self.loaded = False
        self.handleUI()
        self.handleButtons()
        self.handleHeaders()
        self.attemps = 0

    def handleUI(self):
        self.setWindowTitle('Pick to light System : User')
        self.showMaximized()
        self.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        self.movie = QMovie(home_path[:-4] +'/assets/tenor.gif')
        self.label.setMovie(self.movie)
        self.movie.start()
        self.state.setText(" ")
        pix1 =  QPixmap(home_path[:-4] +'/assets/logo-small.png')
        self.logo1.setPixmap(pix1.scaled(self.logo1.size()))
        pix2 =  QPixmap(home_path[:-4] +'/assets/logo-csmall.png')
        self.logo2.setPixmap(pix2.scaled(self.logo1.size()))
        QCoreApplication.processEvents()

    def handleButtons(self):
        self.btnLogout.clicked.connect(self.logout)
        self.btnscanner.clicked.connect(self.editSettings)
        self.QTxtRef.setEnabled(False)
        self.QTxtRef.textChanged.connect(self.updateStyleSheetRef)
        self.stats.clicked.connect(self.statistics)

    def updateStyleSheetRef(self):
        if len(self.QTxtRef.text())>0:
            self.QTxtRef.setStyleSheet("color: green;")
        else:
            self.QTxtRef.setStyleSheet("color: red;")

    def handleHeaders(self):
        date = datetime.datetime.now()
        self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
        self.usernameLabel.setText(self.login)

    def logout(self):
        # logs(self.login, "logout")
        self.switchWindow.emit()

    def recieveData(self,data):
        if data.startswith('ref'):
            data = data[:4]
            res = pd.read_csv(home_path[:-4] +'/files/references.csv')
            references = res['reference'].tolist()
            if data in references:
                self.last_ref = data
                self.movie.stop()
                # self.label.setPixmap()
                pix =  QPixmap(home_path[:-4] +'/assets/'+data+'.jpg')
                self.label.setPixmap(pix.scaled(self.label.size()))
                self.QTxtRef.setText(data)
                self.sendData(data)
            else:
                QMessageBox.warning(self,"Error","Reference not found!")
        else:
            # logs(self.login,self.last_ref,data)
            self.attemps += 1
            data = data.lower()
            res = pd.read_csv(home_path[:-4] +'/files/references.csv')
            button = res["button"][res['reference'] == self.last_ref].item()
            if button != data :
                pix =  QPixmap(home_path[:-4] +'/assets/nok.png')
                self.state.setPixmap(pix)#.scaled(self.state.size()))
                QCoreApplication.processEvents()
                time.sleep(3)
                self.state.setText("Try again")
                QCoreApplication.processEvents()
            elif button == data:
                pix =  QPixmap(home_path[:-4] +'/assets/ok.png')
                self.state.setPixmap(pix)#.scaled(self.state.size()))
                QCoreApplication.processEvents()
                time.sleep(3)
                self.label.setMovie(self.movie)
                self.movie.start()
                self.state.setText(" ")
                self.QTxtRef.setText("")
                self.attemps = 0
                QCoreApplication.processEvents()
            if self.attemps == 3:
                self.label.setMovie(self.movie)
                self.movie.start()
                self.state.setText(" ")
                self.QTxtRef.setText("")
                self.attemps = 0
                QCoreApplication.processEvents()
    def sendData(self,data):
        try:
            res = pd.read_csv(home_path[:-4] +'/files/references.csv')
            code = res[res['reference'] == data]['code'].item()
            self.sendsignal.emit(str(code))
        except Exception as e:
            pass
        

    def editSettings(self):
        # edit scanner
        res = pd.read_csv(home_path[:-4] +'/files/settings.csv')
        row = list(res[res['purpose'] == 'Scanner'].index)[0]
        editPin = PinDialog(row,self.login,is_admin = False)
        editPin.setWindowTitle('Edit Port')
        editPin.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        editPin.resize(380,180)
        editPin.exec_()
        editPin.close()
        # edit plc
        row = list(res[res['purpose'] == 'CPU'].index)[0]
        editPin = PinDialog(row,self.login,is_admin = False)
        editPin.setWindowTitle('Edit Port')
        editPin.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        editPin.resize(380,180)
        editPin.exec_()
        editPin.close()

    def statistics(self):
        self.switchWindow2.emit(self.login)
        
class Statistics(QMainWindow,STATS_UI):
    switchWindow = pyqtSignal(str)

    def __init__(self, login,arg=None):
        super(Statistics, self).__init__(arg)
        QMainWindow.__init__(self)
        self.loaded = False
        self.date_type = 'day'
        self.login = login
        self.setupUi(self)
        self.handleUI()
        self.handleButtons()
        self.handleHeaders()
        # self.drawPlots()
        
    def handleUI(self):
        self.setWindowTitle('Pick to light System: Statistics')
        self.showMaximized()
        self.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))
        pix1 =  QPixmap(home_path[:-4] +'/assets/logo-s.png')
        self.logo1.setPixmap(pix1.scaled(self.logo1.size()))
        pix2 =  QPixmap(home_path[:-4] +'/assets/logo-c.jpg')
        self.logo2.setPixmap(pix2.scaled(self.logo1.size()))
        hist = pd.read_csv(home_path[:-4] +'/files/history.csv')
        userList = hist['username'].unique()
        refList = hist['reference'].unique()
        self.users.addItems(userList)
        self.products.addItems(refList)
        self.userstime.addItems(userList)
        self.userPlot()
        self.productPlot()
        self.datePlot(self.radioButton1)
        self.usersTimePlot()
        QCoreApplication.processEvents()


    def handleButtons(self):
        self.btnback.clicked.connect(self.back)
        self.users.activated.connect(self.userPlot)
        self.products.activated.connect(self.productPlot)
        self.userstime.activated.connect(self.usersTimePlot)
        self.radioButton1.toggled.connect(lambda: self.datePlot(self.radioButton1))
        self.radioButton2.toggled.connect(lambda: self.datePlot(self.radioButton2))
        self.radioButton3.toggled.connect(lambda: self.datePlot(self.radioButton3))
        self.radioButton4.toggled.connect(lambda: self.datePlot(self.radioButton4))

    def handleHeaders(self):
        date = datetime.datetime.now()
        self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
        self.usernameLabel.setText(self.login)

    def back(self):
        self.switchWindow.emit(self.login)
    
    def userPlot(self):
        user = str(self.users.currentText())
        plotNumberOfScans('username',user)
        self.drawPlots()

    def usersTimePlot(self):
        user = str(self.userstime.currentText())
        plotDate(self.date_type,user=user)
        self.drawPlots()


    def productPlot(self):
        ref = str(self.products.currentText())
        plotNumberOfScans('reference',ref)
        self.drawPlots()

    def datePlot(self,b):
        if b.isChecked():
            self.date_type = b.text()[3:] 
            plotDate(self.date_type)
            self.drawPlots()

    def drawPlots(self):
        try:
            pix1 =  QPixmap(home_path[:-4] +'/assets/username.png')
            pix2 =  QPixmap(home_path[:-4] +'/assets/reference.png')
            pix3 =  QPixmap(home_path[:-4] +'/assets/date.png')
            pix4 =  QPixmap(home_path[:-4] +'/assets/userdate.png')
            self.g1.setPixmap(pix1.scaled(self.g1.size()))
            self.g2.setPixmap(pix2.scaled(self.g2.size()))
            self.g3.setPixmap(pix3.scaled(self.g3.size()))
            self.g4.setPixmap(pix4.scaled(self.g4.size()))
        except Exception as e:
            print('err')
        QCoreApplication.processEvents()


# class Scan(QMainWindow,SCAN_UI):
#     switchWindow = pyqtSignal(str)

#     def __init__(self, text,arg=None,):
#         super(Scan, self).__init__(arg)
#         QWidget.__init__(self)
#         self.setupUi(self)
#         self.login = ""
#         self.reference = ""
#         self.quantity = ""
#         self.loaded = False
#         self.processed = 0
#         self.handleUI()
#         self.handleButtons()
#         self.handleHeaders()

#     def handleUI(self):
#         self.setWindowTitle('Pick to light System : Scan')
#         self.showMaximized()
#         self.setWindowIcon(QIcon(home_path[:-4] +'/assets/logo-scroll.png'))

#     def handleButtons(self):
#         self.btnBack.clicked.connect(self.back)
#         self.btn_I_O.clicked.connect(self.IOmonitor)
#         self.btnStatistic.clicked.connect(self.statistics)
#         self.draw(home_path[:-4] +'/assets/step1.jpg')

#     def handel_progressBar(self,):
#         per = self.processed*100/self.quantity
#         self.progressBar.setValue(per)
#         self.quanLabel.setText('BOX QT ' + str(self.processed) +'/' +str(self.quantity))
#         QApplication.processEvents()

#     def handleHeaders(self):
#         date = datetime.datetime.now()
#         self.dateLabel.setText(date.strftime("%Y/%m/%d, %H:%M"))
#         self.usernameLabel.setText("User: "+self.login)
#         self.refLabel.setText("Ref: " + self.reference)

#     def back(self):
#         self.switchWindow.emit(self.login)

#     def IOmonitor(self):
#         pass


#     def statistics(self):
#         pass

#     def recieveData(self,data):
#         if data == 'step1':
#             self.step1.setStyleSheet('border: 10px solid #64de9d;background-color : #64de9d;')
#             self.draw(home_path[:-4] +'/assets/step2.jpg')
#         elif data == 'step2':
#             self.step2.setStyleSheet('border: 10px solid #64de9d;background-color : #64de9d;')
#             self.draw(home_path[:-4] +'/assets/step3.jpg')
#         elif data == 'step3':
#             self.step3.setStyleSheet('border: 10px solid #64de9d;background-color : #64de9d;')
#             self.draw(home_path[:-4] +'/assets/step4.jpg')
#         elif data == 'step4':
#             self.step4.setStyleSheet('border: 10px solid #64de9d;background-color : #64de9d;')
#             self.processed +=1
#             self.handel_progressBar()
#             #logs(self.login, "Complete "+ str(self.processed) + "/" + str(self.quantity) +" of product :" + str(self.reference))
#             time.sleep(3)
#             self.step1.setStyleSheet('border: 15px solid #e1eefa;background-color : #e1eefa;')
#             self.step2.setStyleSheet('border: 15px solid #e1eefa;background-color : #e1eefa;')
#             self.step3.setStyleSheet('border: 15px solid #e1eefa;background-color : #e1eefa;')
#             self.step4.setStyleSheet('border: 15px solid #e1eefa;background-color : #e1eefa;')
#             self.draw(home_path[:-4] +'/assets/step1.jpg')
#         if self.processed == self.quantity:
#             # logs(self.login, "Finished all products with reference" + self.reference)
#             self.back()


#     def draw(self,name):
#         pix =  QPixmap(name)
#         self.label.setPixmap(pix.scaled(self.label.size()))
