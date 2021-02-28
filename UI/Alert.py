from PyQt5.QtWidgets import QMessageBox

class Alert:
    def __init__(self, message='', title=''):
        self.message = message
        self.title = title
        self.alert()

    def alert(self):
        msgBox = QMessageBox()
        msgBox.setStyleSheet(self.styleAlert())
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(self.message)
        msgBox.setWindowTitle(self.title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def styleAlert(self):
        return """
           QMessageBox {background-color: rgb(85, 87, 83); color: white;} QLineEdit{ color: rgb(255, 255, 255)}
                               QPushButton{color: white; font-size: 16px; background-color: rgb(114, 159, 207);border-radius: 10px;
                               padding: 10px; text-align: center;} QPushButton:hover{color: #2b5b84;}
                               """
