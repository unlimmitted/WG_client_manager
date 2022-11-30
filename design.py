# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(362, 324)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.QR_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.QR_view.setGeometry(QtCore.QRect(10, 10, 231, 221))
        self.QR_view.setObjectName("QR_view")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(250, 10, 101, 101))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 70, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.label.setObjectName("label")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 40, 81, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(250, 110, 101, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 90, 81, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 60, 61, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setGeometry(QtCore.QRect(70, 60, 21, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(10, 40, 81, 22))
        self.comboBox.setObjectName("comboBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 230, 231, 71))
        self.groupBox_3.setObjectName("groupBox_3")
        self.lineEditAddress = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditAddress.setGeometry(QtCore.QRect(10, 20, 101, 20))
        self.lineEditAddress.setObjectName("lineEditAddress")
        self.lineEditLogin = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditLogin.setGeometry(QtCore.QRect(10, 40, 101, 20))
        self.lineEditLogin.setObjectName("lineEditLogin")
        self.connButton = QtWidgets.QPushButton(self.groupBox_3)
        self.connButton.setGeometry(QtCore.QRect(120, 40, 101, 23))
        self.connButton.setObjectName("connButton")
        self.lineEditPassword = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditPassword.setGeometry(QtCore.QRect(120, 20, 101, 20))
        self.lineEditPassword.setObjectName("lineEditPassword")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 362, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WireGuard client\'s"))
        self.groupBox.setTitle(_translate("MainWindow", "Create client"))
        self.pushButton.setText(_translate("MainWindow", "Create"))
        self.label.setText(_translate("MainWindow", "Cleint name"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Clients"))
        self.pushButton_2.setText(_translate("MainWindow", "Delete"))
        self.pushButton_4.setText(_translate("MainWindow", "Show QR"))
        self.pushButton_5.setText(_translate("MainWindow", "I"))
        self.label_2.setText(_translate("MainWindow", "Choose client"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Connection"))
        self.lineEditAddress.setText(_translate("MainWindow", "Address"))
        self.lineEditLogin.setText(_translate("MainWindow", "Login"))
        self.connButton.setText(_translate("MainWindow", "Connect"))
        self.lineEditPassword.setText(_translate("MainWindow", "Password"))
