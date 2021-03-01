from os import walk, mkdir
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QPushButton, QLabel, QProgressBar, QLineEdit
from UI.main import Ui_MainWindow
from UI.ssh import Ui_SSH
from UI.Alert import Alert
from sys import argv
from psutil import process_iter, pids, cpu_percent, virtual_memory, Process, AccessDenied
from time import sleep
from hurry.filesize import size, alternative
from paramiko import SSHClient, AutoAddPolicy
from ipaddress import ip_address
from json import JSONDecoder


class Ssh(QMainWindow, Ui_SSH):

    def __init__(self, parent=None):
        super(Ssh, self).__init__(parent)
        self.setupUi(self)
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self._translate = QCoreApplication.translate

    def main(self):
        stdin, stdout, stderr = self.ssh.exec_command('ps x')
        if stderr.channel.recv_exit_status() != 0:
            Alert(message='Falha ao buscar processos ', title='Processos')
            print(stderr.read())
        else:
            self.memory()
            self.process(stdout)

    def process(self, stdout):
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
            self.label = QLabel(self.frame_6)
            self.label.setObjectName(f"memory_label")
            self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)
            self.label.setText(self._translate("SSH", f" Em uso {dataMemory[1][26:38]}"))

            self.label = QLabel(self.frame_6)
            self.label.setObjectName(f"memory_label")
            self.gridLayout_10.addWidget(self.label, 0, 1, 1, 1)
            self.label.setText(self._translate("SSH", f" Livre  {dataMemory[1][69:80]}"))

    def handleButtonClicked(self):
        linha = self.tableWidget_2.currentRow()
        pid = self.tableWidget_2.item(linha, 0).text()
        stdin, stdout, stderr = self.ssh.exec_command('kill -9 ' + pid)
        if stderr.channel.recv_exit_status() != 0:
            Alert(message='Falha ao finalizar o processo ' + pid, title='Processo')

    def startThead(self):
        self.thread = ExecuteThread()
        self.thread.start()
        self.thread.finished.connect(self.thread_finished)
        self.thread.sinal.connect(self.main)

    def thread_finished(self):
        self.thread.terminate()


def startSsh(user=None, hostname=None, password=None):
    try:
        ssh.ssh.connect(hostname=hostname, username=user, password=password)
        ssh.startThead()
        ssh.show()
    except Exception as e:
        Alert(str(e.args), 'Falha ao fazer conexão')


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.thread = None
        self.start()
        self.pushButtonConnect.clicked.connect(self.loginSsh)
        self.pushButtonSaveHost.clicked.connect(self.saveHost)
        self.comboBoxHosts.activated.connect(self.selectHost)
        self.lineEditPass.setEchoMode(QLineEdit.Password)
        self._translate = QCoreApplication.translate
        self.listHost()

    def main(self):
        self.monitoryCpu()
        self.memory()
        self.process()

    def listHost(self):
        item = 0
        for _, _, arquivo in walk('Hosts/'):
            for host in arquivo:
                with open('Hosts/' + host, 'r') as dataHost:
                    read = dataHost.read()
                    if read:
                        result = JSONDecoder().decode(read)
                        self.comboBoxHosts.addItem(result['user'], result['host'])
                item += item

    def selectHost(self, item):
        if item is 0:
            self.lineEditUser.setText('')
            self.lineEditHost.setText('')
            self.lineEditPass.setText('')
            return
        host = self.comboBoxHosts.itemData(item)
        name = self.comboBoxHosts.itemText(item)
        with open(f'Hosts/{name}{host}.json', 'r') as dataHost:
            result = JSONDecoder().decode(dataHost.read())
            self.lineEditUser.setText(result['user'])
            self.lineEditHost.setText(result['host'])

    def saveHost(self):
        if self.dataHost():
            user, hostname, password = self.dataHost()
            host = None
            try:
                host = open(f'Hosts/{user}{hostname}.json', 'w')
            except:
                mkdir('Hosts', 0o777)
                host = open(f'Hosts/{user}{hostname}.json', 'w')
            finally:
                data = {"user": user, "host": hostname}
                host.write(str(data).replace("'", '"'))
                host.close()
                self.comboBoxHosts.addItem(user, hostname)

    def loginSsh(self):
        if self.dataHost():
            user, hostname, password = self.dataHost()
            startSsh(user=user, hostname=hostname, password=password)

    def dataHost(self):
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
        return user, hostname, password

    def process(self):
        header = ['pid', 'name', 'status', 'username']
        line = 0
        processos = process_iter()
        self.tableWidget.setRowCount(len(pids()))
        for processo in processos:
            lineColumn = 0
            for column in header:
                info = processo.as_dict(attrs=header)[column]
                self.tableWidget.setItem(line, lineColumn, QTableWidgetItem(str(info)))
                lineColumn += 1
            kill = QPushButton('KILL')
            kill.clicked.connect(self.handleButtonClicked)
            self.tableWidget.setCellWidget(line, 4, kill)
            line += 1
            self.tableWidget.setColumnWidth(1, 300)
            self.tableWidget.setColumnWidth(3, 100)

    def monitoryCpu(self):
        i = 1
        position = 0
        for cpu in cpu_percent(interval=None, percpu=True):
            if i > 1:
                position = position + 1
            self.label = QLabel(self.frame_2)
            self.label.setObjectName(f"processador_label{i}")
            self.gridLayout_3.addWidget(self.label, 0, position, 1, 1)
            self.processado_progressBar = QProgressBar(self.frame_2)
            self.processado_progressBar.setProperty("value", cpu)
            self.processado_progressBar.setStyleSheet("background-color: rgb(52, 101, 164);\n"
                                                      "background-color: rgb(238, 238, 236);")
            self.processado_progressBar.setObjectName(f"processador_progressBar{i}")
            position += 1
            self.gridLayout_3.addWidget(self.processado_progressBar, 0, position, 1, 1)
            self.label.setText(self._translate("MainWindow", f" CPU {i} "))
            i += 1

    def memory(self):
        memory = virtual_memory()
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(f"memory_label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        self.processado_progressBar = QProgressBar(self.frame_3)
        self.label.setText(self._translate("MainWindow", f" Em uso {size(memory.used, system=alternative)} "))
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(f"memory_label")
        self.gridLayout_6.addWidget(self.label, 0, 1, 1, 1)
        self.processado_progressBar = QProgressBar(self.frame_3)
        self.label.setText(self._translate("MainWindow", f" Livre {size(memory.available, system=alternative)} "))

    def handleButtonClicked(self):
        linha = self.tableWidget.currentRow()
        pid = self.tableWidget.item(linha, 0).text()
        self.killProcTree(int(pid))

    def killProcTree(self, pid: int) -> None:
        try:
            Process(pid).kill()
        except Exception as e:
            if isinstance(e, AccessDenied):
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
    app = QApplication(argv)
    main = Main()
    main.show()
    ssh = Ssh()
    app.exec_()
