import os

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
        self.pushButton_gen_symm_key.clicked.connect(self.gen_sym_key)
        self.pushButton_sypher_open_key.clicked.connect(self.sypher_open_key)
        self.pushButton_gen_symm_key_2.clicked.connect(self.gen_sym_key_from_msg)
        self.check_keys()

    def check_keys(self):
        keys_view = list()
        with open('keys.txt', mode='r') as f1:
            for el in f1:
                keys_view.append(el.strip())
        with open('sym_key.json', 'r') as fh:
            sym_key = json.load(fh)
        sym_key = bytes(sym_key.encode('CP866'))
        print(sym_key)
        with open('sym_iv.json', 'r') as fh:
            sym_iv = json.load(fh)
        sym_iv = bytes(sym_iv.encode('CP866'))
        if keys_view:
            self.plainTextEdit_public_key.clear()
            self.plainTextEdit_public_key.appendPlainText(keys_view[0])
            self.plainTextEdit_private_key.clear()
            self.plainTextEdit_private_key.appendPlainText(keys_view[1])
            self.plainTextEdit_public_key_on_get.clear()
            self.plainTextEdit_public_key_on_get.appendPlainText(keys_view[0])
            self.plainTextEdit_open_key_sypher_file.clear()
            self.plainTextEdit_open_key_sypher_file.appendPlainText(keys_view[0])
            self.plainTextEdit_unsypher_symm_key.clear()
            self.plainTextEdit_unsypher_symm_key.appendPlainText(keys_view[1])
            self.plainTextEdit_symm_rand_key.clear()
            self.plainTextEdit_symm_rand_key.appendPlainText(str(sym_key))
            self.plainTextEdit_symm_init_vector.clear()
            self.plainTextEdit_symm_init_vector.appendPlainText(str(sym_iv))

    def gen_sym_key(self):
        self.plainTextEdit_symm_rand_key.clear()
        self.plainTextEdit_symm_init_vector.clear()
        # Генерация случайного ключа и IV (Initialization Vector)
        key = os.urandom(32)  # 256-битный ключ для AES
        iv = os.urandom(16)  # 128-битный IV для AES
        with open('sym_key.json', 'w') as fh:
            json.dump(key.decode('CP866'), fh)
        with open('sym_iv.json', 'w') as fh:
            json.dump(iv.decode('CP866'), fh)
        self.check_keys()
        self.plainTextEdit_symm_rand_key.appendPlainText(str(key))
        self.plainTextEdit_symm_init_vector.appendPlainText(str(iv))

    def gen_keys(self):
        self.plainTextEdit_public_key.clear()
        self.plainTextEdit_private_key.clear()
        (self.public_key, self.private_key) = rsa.newkeys(
            int(self.lineEdit_key_len.text()))
        self.plainTextEdit_public_key.appendPlainText(str(self.public_key))
        self.plainTextEdit_private_key.appendPlainText(str(self.private_key))
        with open('keys.txt', mode='w') as f:
            f.write(f'{self.public_key}\n{self.private_key}')
        self.check_keys()

    def cypher_text(self):
        self.plainTextEdit_result_msg.clear()
        inp_msg = str(self.plainTextEdit_open_text.toPlainText()
                      ).encode('utf8')
        public_key_params = str(
            self.plainTextEdit_public_key_on_get.toPlainText()).replace('PublicKey(', '')
        public_key_params = public_key_params.replace(',', '')
        public_key_params = public_key_params.replace(')', '')
        public_key_params = public_key_params.split()
        public_key = rsa.key.PublicKey(
            int(public_key_params[0]), int(public_key_params[1]))
        crypto = rsa.encrypt(inp_msg, public_key)
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

    def sypher_open_key(self):
        with open('sym_key.json', 'r') as fh:
            sym_key = json.load(fh)
        sym_key = bytes(sym_key.encode('CP866'))
        with open('sym_iv.json', 'r') as fh:
            sym_iv = json.load(fh)
        sym_iv = bytes(sym_iv.encode('CP866'))
        public_key_params = str(
            self.plainTextEdit_open_key_sypher_file.toPlainText()).replace('PublicKey(', '')
        public_key_params = public_key_params.replace(',', '')
        public_key_params = public_key_params.replace(')', '')
        public_key_params = public_key_params.split()
        public_key = rsa.key.PublicKey(
            int(public_key_params[0]), int(public_key_params[1]))
        crypto = rsa.encrypt(sym_key, public_key)
        crypto = crypto.decode('CP866')
        crypto_iv = rsa.encrypt(sym_iv, public_key)
        crypto_iv = crypto_iv.decode('CP866')
        with open('message_key.json', 'w') as fh:
            json.dump(crypto, fh)
        with open('message_iv.json', 'w') as fh:
            json.dump(crypto_iv, fh)

    def gen_sym_key_from_msg(self):
        with open('message_key.json', 'r') as fh:
            sym_key = json.load(fh)
        sym_key = bytes(sym_key.encode('CP866'))
        with open('message_iv.json', 'r') as fh:
            sym_iv = json.load(fh)
        sym_iv = bytes(sym_iv.encode('CP866'))
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
        message_key = rsa.decrypt(sym_key, private_key)
        message_key = bytes(message_key)
        message_iv = rsa.decrypt(sym_iv, private_key)
        message_iv = bytes(message_iv)
        with open('inp_sym_key.json', 'w') as fh:
            json.dump(message_key.decode('CP866'), fh)
        with open('inp_sym_iv.json', 'w') as fh:
            json.dump(message_iv.decode('CP866'), fh)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainClass()
    w.show()

    sys.exit(app.exec_())
