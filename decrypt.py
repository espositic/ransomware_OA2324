import os
import glob
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def generate_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def decrypt_file(file_path: str, key: bytes):
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    original_file_path = file_path.replace('.enc', '')
    with open(original_file_path, 'wb') as f:
        f.write(plaintext)

    os.remove(file_path)


def decrypt_folder(folder_path: str, password: str):
    key = generate_key(password)
    files = glob.glob(os.path.join(folder_path, '*.enc'))
    for file in files:
        if os.path.isfile(file):
            decrypt_file(file, key)


if __name__ == "__main__":
    folders = [
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents'),
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive'),
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'Download')
    ]
    password = ''

    for folder in folders:
        decrypt_folder(folder, password)

    file_path = os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'uhavebeenhacked.txt')


    if os.path.exists(file_path):
        os.remove(file_path)