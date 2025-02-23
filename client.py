from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from GUI.client import Ui_MainWindow
import socket
import rsa
import json


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
        self.pushButton_let_file_window_2.clicked.connect(
            lambda: self.choose_operator(page_index=2)
        )
        self.pushButton_get_msg_window_2.clicked.connect(
            lambda: self.choose_operator(page_index=1)
        )
        self.pushButton_get_file_window.clicked.connect(
            lambda: self.choose_operator(page_index=3)
        )
        self.pushButton_file_let_page.clicked.connect(
            lambda: self.choose_operator(page_index=2)
        )
        self.pushButton_let_file_window.clicked.connect(
            lambda: self.choose_operator(page_index=2))

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
        crypto = crypto.decode('CP866')
        with open('message.json', 'w') as fh:
            json.dump(crypto, fh)

    def choose_operator(self, page_index):
        self.stackedWidget.setCurrentIndex(page_index)

    def decrypt_msg(self):

        with open('message.json', 'r') as fh:
            inp_encrypt_msg = json.load(fh)
        self.plainTextEdit_get_msg.appendPlainText(inp_encrypt_msg)
        inp_encrypt_msg = self.plainTextEdit_get_msg.toPlainText()
        inp_encrypt_msg = bytes(inp_encrypt_msg.encode('CP866'))

        with open('keys.txt', mode='r') as f1:
            keys = list()
            for el in f1:
                keys.append(el.strip())
        private_key = keys[1].replace(
            'PrivateKey(', '').replace(')', '').replace(',', '').split()
        self.plainTextEdit_public_key.appendPlainText(keys[0])
        self.plainTextEdit_private_key.appendPlainText(keys[1])
        private_key = rsa.key.PrivateKey(int(private_key[0]), int(private_key[1]),
                                         int(private_key[2]), int(private_key[3]), int(private_key[4]))
        message = rsa.decrypt(inp_encrypt_msg, private_key)
        self.plainTextEdit_get_msg_result.appendPlainText(
            message.decode('utf-8'))
        print(message.decode('utf-8'))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
