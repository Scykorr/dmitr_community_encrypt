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
        self.pushButton_uncypher.clicked.connect(self.decrypt_msg)

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
        public_key_params = str(
            self.plainTextEdit_public_key_on_get.toPlainText()).replace('PublicKey(', '')
        public_key_params = public_key_params.replace(',', '')
        public_key_params = public_key_params.replace(')', '')
        public_key_params = public_key_params.split()
        print(public_key_params)
        public_key = rsa.key.PublicKey(
            int(public_key_params[0]), int(public_key_params[1]))
        crypto = rsa.encrypt(inp_msg, public_key)
        print(type(crypto))
        self.plainTextEdit_result_msg.appendPlainText(str(crypto))
        with open('message.txt', mode='w') as f:
            f.write(f'{crypto}')

    def choose_operator(self, page_index):
        self.stackedWidget.setCurrentIndex(page_index)

    def decrypt_msg(self):
        inp_encrypt_msg = bytes(
            str(self.plainTextEdit_get_msg.toPlainText()).encode('utf8'))
        inp_encrypt_msg = bytes(
            b'J\x07\xc4\x0c\xca\xe0\xe6\x1c\xbd\x1a\xb6\xbd}\xd7\x9c\x98')
        self.private_key = rsa.key.PrivateKey(277623006974286306300466805308691768327, 65537,
                                              275038969953148404589898004223643669873, 269462156046169262777, 1030285703372457151)
        message = rsa.decrypt(inp_encrypt_msg, self.private_key)
        print(message.decode('utf-8'))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
