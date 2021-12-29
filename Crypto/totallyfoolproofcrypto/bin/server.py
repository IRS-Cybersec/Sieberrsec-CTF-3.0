from Crypto.Util.Padding import pad,unpad
from Crypto.Cipher import AES
import os

with open("flag", 'rb') as f: flag = f.read().strip()
key = os.urandom(16)

while 1:
    pt = input('> ').encode()
    padded = pad(pt+flag, AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB)
    print(cipher.encrypt(padded).hex())

