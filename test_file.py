import json

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

key = os.urandom(32)  # 256-битный ключ для AES
iv = os.urandom(16)
print(key)
with open('message_key.json', 'w') as fh:
    json.dump(key.decode('CP866'), fh)

with open('message_key.json', 'r') as fh:
    inp_encrypt_msg = json.load(fh)
inp_encrypt_msg = bytes(inp_encrypt_msg.encode('CP866'))
print(type(inp_encrypt_msg))

