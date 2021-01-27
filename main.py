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
            kill = QPushButton('Kill')
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
        self.test = ExecuteThread()
        self.test.start()
        self.test.finished.connect(self.thread_finished)
        self.test.my_signal.connect(self.my_event)

    def thread_finished(self):
        pass

    def my_event(self):
        self.process()

class ExecuteThread(QThread):
    my_signal = pyqtSignal()

    def run(self):
        while True:
            self.my_signal.emit()
            sleep(3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()