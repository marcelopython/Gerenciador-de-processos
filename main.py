import os
import signal

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton, QMessageBox
from aptdaemon import loop

from UI.main import Ui_MainWindow
import sys
import psutil as ps
from os import system
from PyQt5.QtCore import pyqtSignal, QThread
from time import sleep
from hurry.filesize import size, alternative
import asyncio

class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.thread = None
        self.start()

    def man(self):
        self.monitoryCpu()
        self.memory()
        header = ['pid', 'name', 'status', 'username']
        line = 0
        processos = ps.process_iter()
        self.tableWidget.setRowCount(len(ps.pids()))
        for processo in processos:
            lineColumn = 0
            for column in header:
                info = processo.as_dict(attrs=header)[column]
                self.tableWidget.setItem(line, lineColumn, QTableWidgetItem(str(info)))
                lineColumn = lineColumn + 1
            kill = QPushButton('KILL')
            kill.clicked.connect(self.handleButtonClicked)
            self.tableWidget.setCellWidget(line, 4, kill)
            line = line + 1
            self.tableWidget.setColumnWidth(1, 300)
            self.tableWidget.setColumnWidth(3, 100)

    def monitoryCpu(self):
        _translate = QtCore.QCoreApplication.translate
        i = 0
        position = 0
        for cpu in ps.cpu_percent(interval=0.1, percpu=True):
            if i > 0:
                position = position+1
            self.label = QtWidgets.QLabel(self.frame_2)
            self.label.setObjectName(f"processador_label{i}")
            self.gridLayout_3.addWidget(self.label, 0, position, 1, 1)
            self.processado_progressBar = QtWidgets.QProgressBar(self.frame_2)
            self.processado_progressBar.setProperty("value", cpu)
            self.processado_progressBar.setStyleSheet("background-color: rgb(52, 101, 164);\n"
                           "background-color: rgb(238, 238, 236);")
            self.processado_progressBar.setObjectName(f"processador_progressBar{i}")
            position = position+1
            self.gridLayout_3.addWidget(self.processado_progressBar, 0, position, 1, 1)
            self.label.setText(_translate("MainWindow", f" CPU {i} "))
            i = i + 1

    def memory(self):
        memory = ps.virtual_memory()
        _translate = QtCore.QCoreApplication.translate
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName(f"memory_label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        self.processado_progressBar = QtWidgets.QProgressBar(self.frame_3)
        self.label.setText(_translate("MainWindow", f" Em uso {size(memory.used,  system=alternative)} "))

        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName(f"memory_label")
        self.gridLayout_6.addWidget(self.label, 0, 1, 1, 1)
        self.processado_progressBar = QtWidgets.QProgressBar(self.frame_3)
        self.label.setText(_translate("MainWindow", f" Livre {size(memory.available, system=alternative)} "))

    def handleButtonClicked(self):
        linha = self.tableWidget.currentRow()
        pid = self.tableWidget.item(linha, 0).text()
        self.kill_proc_tree(int(pid))


    def kill_proc_tree(self, pid: int) -> None:
        try:
            ps.Process(pid).kill()
        except Exception as e:
            if isinstance(e, ps.AccessDenied):
                self.alert()

    def alert(self):
        msgBox = QMessageBox()
        msgBox.setStyleSheet(self.styleAlert())
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Usuário não permitido')
        msgBox.setWindowTitle("Access Denied")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def styleAlert(self):
        return """
           QMessageBox {background-color: rgb(85, 87, 83); color: white;} QLineEdit{ color: rgb(255, 255, 255)}
                               QPushButton{color: white; font-size: 16px; background-color: rgb(114, 159, 207);border-radius: 10px;
                               padding: 10px; text-align: center;} QPushButton:hover{color: #2b5b84;}
                               """
    def start(self):
        self.thread = ExecuteThread()
        self.thread.start()
        self.thread.finished.connect(self.thread_finished)
        self.thread.sinal.connect(self.man)

    def thread_finished(self):
        pass

class ExecuteThread(QThread):
    sinal = pyqtSignal()
    def run(self):
        while True:
            self.sinal.emit()
            sleep(3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
