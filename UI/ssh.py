# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './UI_xml/ssh.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SSH(object):
    def setupUi(self, SSH):
        SSH.setObjectName("SSH")
        SSH.setWindowModality(QtCore.Qt.ApplicationModal)
        SSH.resize(800, 599)
        SSH.setStyleSheet("background-color: rgb(136, 138, 133);")
        self.centralwidget = QtWidgets.QWidget(SSH)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 778, 540))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_2)
        self.tableWidget_2.setStyleSheet("\n"
"background-color: rgb(46, 52, 54);\n"
"color: rgb(255,255,255);")
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(52, 101, 164))
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(52, 101, 164))
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(52, 101, 164))
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(52, 101, 164))
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(52, 101, 164))
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.tableWidget_2.setItem(0, 0, item)
        self.gridLayout_8.addWidget(self.tableWidget_2, 0, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea_2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 37))
        self.frame.setMaximumSize(QtCore.QSize(16777181, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_6 = QtWidgets.QFrame(self.frame)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_9.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        self.horizontalLayout_6.addWidget(self.frame_6)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 1))
        self.frame_2.setMaximumSize(QtCore.QSize(16777193, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_11.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.horizontalLayout_6.addWidget(self.frame_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        SSH.setCentralWidget(self.centralwidget)

        self.retranslateUi(SSH)
        QtCore.QMetaObject.connectSlotsByName(SSH)

    def retranslateUi(self, SSH):
        _translate = QtCore.QCoreApplication.translate
        SSH.setWindowTitle(_translate("SSH", "MainWindow"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("SSH", "PID"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("SSH", "STAT"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("SSH", "TIME"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("SSH", "COMMAND"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("SSH", "ACTIONS"))
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)