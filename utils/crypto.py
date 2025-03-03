from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from base64 import b64encode, b64decode

def generate_key():
    return get_random_bytes(16)


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return b64encode(nonce + tag + ciphertext)

def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    # Decode the base64 encoded ciphertext
    decoded_data = b64decode(ciphertext)
    nonce = decoded_data[:12]
    tag = decoded_data[12:28]
    ciphertext = decoded_data[28:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext