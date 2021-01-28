from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton
from UI.main import Ui_MainWindow
import sys
import psutil as ps
from os import system
from PyQt5.QtCore import pyqtSignal, QThread
from time import sleep

class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.thread = None
        self.StartButtonEvent()


    def process(self):
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

    def handleButtonClicked(self):
        linha = self.tableWidget.currentRow()
        pid = self.tableWidget.item(linha, 0).text()
        system(f'kill -9 {pid}')

    def StartButtonEvent(self):
        self.thread = ExecuteThread()
        self.thread.start()
        self.thread.finished.connect(self.thread_finished)
        self.thread.sinal.connect(self.process)

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