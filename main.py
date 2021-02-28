from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSignal, QThread
from UI.main import Ui_MainWindow
from UI.ssh import Ui_SSH
from UI.Alert import Alert
import sys
import psutil as ps
from time import sleep
from hurry.filesize import size, alternative
from paramiko import SSHClient, AutoAddPolicy
from ipaddress import ip_address


class Ssh(QMainWindow, Ui_SSH):

    def __init__(self, parent=None):
        super(Ssh, self).__init__(parent)
        self.setupUi(self)
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())

    def main(self):
        stdin, stdout, stderr = self.ssh.exec_command('ps x')
        if stderr.channel.recv_exit_status() != 0:
            Alert(message='Falha ao buscar processos ', title='Processos')
            print(stderr.read())
        else:
            self.memory()
            self.processes(stdout)

    def processes(self, stdout):
        data = stdout.read().decode('utf-8').split('\n')
        self.tableWidget_2.setRowCount(len(data) - 5)
        line = 0
        title = True
        for item in data:
            if title:
                title = False
                continue
            self.tableWidget_2.setItem(line, 0, QTableWidgetItem(str(item[0:5])))
            self.tableWidget_2.setItem(line, 1, QTableWidgetItem(str(item[14:21])))
            self.tableWidget_2.setItem(line, 2, QTableWidgetItem(str(item[21:26])))
            self.tableWidget_2.setItem(line, 3, QTableWidgetItem(str(item[26:])))
            kill = QPushButton('KILL')
            kill.clicked.connect(self.handleButtonClicked)
            self.tableWidget_2.setCellWidget(line, 4, kill)
            self.tableWidget_2.setColumnWidth(0, 50)
            self.tableWidget_2.setColumnWidth(1, 50)
            self.tableWidget_2.setColumnWidth(2, 50)
            self.tableWidget_2.setColumnWidth(3, 500)
            line = line + 1

    def memory(self):
        stdin, stdout, stderr = self.ssh.exec_command('free -h')
        if stderr.channel.recv_exit_status() != 0:
            Alert(message='Falha ao ler estatísticas do uso de memoria', title='Estatística de memoria')
        else:
            dataMemory = stdout.read().decode('utf-8').split('\n')
            _translate = QtCore.QCoreApplication.translate
            self.label = QtWidgets.QLabel(self.frame_6)
            self.label.setObjectName(f"memory_label")
            self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)
            self.label.setText(_translate("SSH", f" Em uso {dataMemory[1][26:38]}"))

            self.label = QtWidgets.QLabel(self.frame_6)
            self.label.setObjectName(f"memory_label")
            self.gridLayout_10.addWidget(self.label, 0, 1, 1, 1)
            self.label.setText(_translate("SSH", f" Livre  {dataMemory[1][69:80]}"))

    def handleButtonClicked(self):
        linha = self.tableWidget_2.currentRow()
        pid = self.tableWidget_2.item(linha, 0).text()
        stdin, stdout, stderr = self.ssh.exec_command('kill -9 ' + pid)
        if stderr.channel.recv_exit_status() != 0:
            Alert(message='Falha ao finalizar o processo ' + pid, title='Processo')
            print(stderr.read())

    def startThead(self):
        self.thread = ExecuteThread()
        self.thread.start()
        self.thread.finished.connect(self.thread_finished)
        self.thread.sinal.connect(self.main)

    def thread_finished(self):
        self.thread.terminate()

    def start(self, host, user, password):
        try:
            ssh.ssh.connect(hostname=host, username=user, password=password)
            ssh.startThead()
            ssh.show()
        except Exception as e:
            Alert(str(e.args[1]), 'Falha ao fazer conexão')


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.thread = None
        self.start()
        self.pushButtonConnect.clicked.connect(self.loginSsh)

    def main(self):
        self.monitoryCpu()
        self.memory()
        self.process()

    def loginSsh(self):
        user = self.lineEditUser.text()
        hostname = self.lineEditHost.text()
        password = self.lineEditPass.text()
        if not user or not hostname or not password:
            Alert(message='Dados incompletos', title="Complete os dados")
            return
        try:
            ip_address(hostname)
        except:
            Alert(message='Host não e válido', title="Host inválido")
            return

        try:
            ssh.start(host=hostname, user=user, password=password)
        except Exception as e:
            Alert(str(e.args), 'erro ')
            print(e)

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

    def monitoryCpu(self):
        _translate = QtCore.QCoreApplication.translate
        i = 0
        position = 0
        for cpu in ps.cpu_percent(interval=None, percpu=True):
            if i > 0:
                position = position + 1
            self.label = QtWidgets.QLabel(self.frame_2)
            self.label.setObjectName(f"processador_label{i}")
            self.gridLayout_3.addWidget(self.label, 0, position, 1, 1)
            self.processado_progressBar = QtWidgets.QProgressBar(self.frame_2)
            self.processado_progressBar.setProperty("value", cpu)
            self.processado_progressBar.setStyleSheet("background-color: rgb(52, 101, 164);\n"
                                                      "background-color: rgb(238, 238, 236);")
            self.processado_progressBar.setObjectName(f"processador_progressBar{i}")
            position = position + 1
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
        self.label.setText(_translate("MainWindow", f" Em uso {size(memory.used, system=alternative)} "))
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName(f"memory_label")
        self.gridLayout_6.addWidget(self.label, 0, 1, 1, 1)
        self.processado_progressBar = QtWidgets.QProgressBar(self.frame_3)
        self.label.setText(_translate("MainWindow", f" Livre {size(memory.available, system=alternative)} "))

    def handleButtonClicked(self):
        linha = self.tableWidget.currentRow()
        pid = self.tableWidget.item(linha, 0).text()
        self.killProcTree(int(pid))

    def killProcTree(self, pid: int) -> None:
        try:
            ps.Process(pid).kill()
        except Exception as e:
            if isinstance(e, ps.AccessDenied):
                Alert(message='Usuário não permitido', title="Acesso negado")

    def start(self) -> None:
        self.thread = ExecuteThread()
        self.thread.start()
        self.thread.finished.connect(self.thread_finished)
        self.thread.sinal.connect(self.main)

    def thread_finished(self):
        self.thread.terminate()


class ExecuteThread(QThread):
    sinal = pyqtSignal()

    def __init__(self, parent=None):
        super(ExecuteThread, self).__init__(parent)

    def run(self):
        while True:
            self.sinal.emit()
            sleep(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    ssh = Ssh()
    app.exec_()
