import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, long_to_bytes
from Crypto.Util.Padding import pad


with open('flag.txt', 'rb') as f:
    flag = f.read()


g = 5
p = getPrime(512)
a = random.randrange(2, p - 1)
A = pow(g, a, p)

print("WELCOME TO DIFFIE'S KEY EXCHANGE!!!!!\n")
print(f'g: {g}', f'p: {p}', sep='\n')

B = int(input("\nWhat is your public key?\n"))


if not 1 < B < (p - 1):
    print('Sneakyyyyy....')
    exit()
else:
    shared_secret = pow(B, a, p)
    key = hashlib.md5(long_to_bytes(shared_secret)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    enc = cipher.encrypt(pad(flag, 16))
    print(f'\nencrypted flag: {enc.hex()}')