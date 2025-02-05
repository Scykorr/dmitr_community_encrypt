from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from GUI.client import Ui_MainWindow
import socket
import rsa


class MainClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.setupUi(self)
        self.setWindowTitle('Клиент')
        self.pushButton_gen_keys.clicked.connect(self.gen_keys)
        self.public_key = ''
        self.private_key = ''

    def gen_keys(self):
        self.plainTextEdit_public_key.clear()
        (self.public_key, self.private_key) = rsa.newkeys(
            int(self.lineEdit_key_len.text()))
        self.plainTextEdit_public_key.appendPlainText(str(self.public_key))
        self.plainTextEdit_private_key.appendPlainText(str(self.private_key))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
