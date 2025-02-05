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
        self.pushButton_cypher.clicked.connect(self.cypher_text)
        self.pushButton_get_msg_window.clicked.connect(
            lambda: self.choose_operator(page_index=1))
        self.pushButton_put_msg_window.clicked.connect(
            lambda: self.choose_operator(page_index=0))

    def gen_keys(self):
        self.plainTextEdit_public_key.clear()
        self.plainTextEdit_private_key.clear()
        (self.public_key, self.private_key) = rsa.newkeys(
            int(self.lineEdit_key_len.text()))
        print(type(self.private_key))
        self.plainTextEdit_public_key.appendPlainText(str(self.public_key))
        self.plainTextEdit_private_key.appendPlainText(str(self.private_key))
        # self.public_key = rsa.key.PublicKey(
        #     256656401102891047157919825004431610219, 65537)
        with open('keys.txt', mode='w') as f:
            f.write(f'{self.public_key}\n{self.private_key}')

    def cypher_text(self):
        self.plainTextEdit_result_msg.clear()
        inp_msg = str(self.plainTextEdit_open_text.toPlainText()
                      ).encode('utf8')
        crypto = rsa.encrypt(inp_msg, self.public_key)
        self.plainTextEdit_result_msg.appendPlainText(str(crypto))
        # message = rsa.decrypt(crypto, self.private_key)
        # print(message.decode('utf-8'))
        with open('message.txt', mode='w') as f:
            f.write(f'{crypto}')

    def choose_operator(self, page_index):
        self.stackedWidget.setCurrentIndex(page_index)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
