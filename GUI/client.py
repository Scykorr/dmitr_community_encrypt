from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from GUI.client import Ui_MainWindow
import socket


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.change_size(341, 300)
        self.setupUi(self)
        self.setWindowTitle('Клиент тестирования')
        # self.lineEdit_2.setText('127.0.0.1')
        # self.curr_ip = self.lineEdit_2.text()
        # self.pushButton_2.clicked.connect(lambda: self.choose_operator(page_index=1))
        # self.pushButton.clicked.connect(lambda: self.choose_operator(page_index=2))
        # self.lineEdit.setText('Ivanov Ivan Ivanovich')
        # self.lineEdit_4.setText('standard1.txt')
