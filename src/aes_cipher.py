from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image
import hashlib
import os

def derive_key(password: str, length: int = 16) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()[:length]

def encrypt_ecb(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt_ecb(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)

def encrypt_ctr(data: bytes, key: bytes, nonce: bytes = None):
    if nonce is None:
        nonce = get_random_bytes(8)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.encrypt(data), nonce

def decrypt_ctr(data: bytes, key: bytes, nonce: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.decrypt(data)

def process_image_ecb(input_path: str, output_path: str, password: str, encrypt: bool = True):
    img = Image.open(input_path)
    data = img.tobytes()
    key = derive_key(password)

    if encrypt:
        result = encrypt_ecb(data, key)
        
        with open(output_path + ".bin", "wb") as f:
            f.write(result)

        visual = result[:len(data)].ljust(len(data), b"\0")
        out_img = Image.frombytes(img.mode, img.size, visual)
        out_img.save(output_path)
    else:
        with open(input_path + ".bin", "rb") as f:
            encrypted = f.read()
        result = decrypt_ecb(encrypted, key)
        out_img = Image.frombytes(img.mode, img.size, result[:len(data)])
        out_img.save(output_path)

def process_image_ctr(input_path: str, output_path: str, password: str, nonce: bytes = None, encrypt: bool = True):
    img = Image.open(input_path)
    data = img.tobytes()
    key = derive_key(password)

    if encrypt:
        result, used_nonce = encrypt_ctr(data, key, nonce)

        with open(output_path + ".nonce", "wb") as f:
            f.write(used_nonce)
        out_img = Image.frombytes(img.mode, img.size, result)
        out_img.save(output_path)
        return used_nonce
    else:
        with open(input_path + ".nonce", "rb") as f:
            used_nonce = f.read()
        result = decrypt_ctr(data, key, used_nonce)
        out_img = Image.frombytes(img.mode, img.size, result)
        out_img.save(output_path)