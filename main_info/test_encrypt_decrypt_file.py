from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Генерация случайного ключа и IV (Initialization Vector)
key = os.urandom(32)  # 256-битный ключ для AES
iv = os.urandom(16)   # 128-битный IV для AES

# Функция для шифрования файла


def encrypt_file(input_file, output_file, key, iv):
    # Инициализация шифра
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    # Чтение данных из файла
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Добавление padding (дополнение данных до размера, кратного 16 байтам)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Шифрование данных
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Запись зашифрованных данных в файл
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)  # Сохраняем IV и зашифрованные данные

# Функция для расшифрования файла


def decrypt_file(input_file, output_file, key):
    # Чтение зашифрованных данных из файла
    with open(input_file, 'rb') as f:
        data = f.read()

    # Извлечение IV и зашифрованных данных
    iv = data[:16]
    ciphertext = data[16:]

    # Инициализация шифра
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    # Расшифрование данных
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Удаление padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Запись расшифрованных данных в файл
    with open(output_file, 'wb') as f:
        f.write(plaintext)


# Пример использования
if __name__ == "__main__":
    input_file = 'example.txt'          # Исходный файл
    encrypted_file = 'example.enc'     # Зашифрованный файл
    decrypted_file = 'example_dec.txt'  # Расшифрованный файл

    # Шифрование файла
    encrypt_file(input_file, encrypted_file, key, iv)
    print(f"Файл '{input_file}' зашифрован в '{encrypted_file}'.")

    # Расшифрование файла
    decrypt_file(encrypted_file, decrypted_file, key)
    print(f"Файл '{encrypted_file}' расшифрован в '{decrypted_file}'.")
