import os
import random
from Crypto.Util.number import bytes_to_long, getPrime

iv = os.urandom(8)
with open('flag.txt', 'rb') as f:
    flag = bytes_to_long(f.read())

g = 5
p = getPrime(512)
a = random.randrange(2, p - 1)
A = pow(g, a, p)

print("WELCOME TO DIFFIE'S KEY EXCHANGE!!!!!\n")
print(f'g: {g}', f'p: {p}', sep='\n')

priv_key = int(input("\nWhat is your private key?\n"))
B = pow(g, priv_key, p)
shared_secret = pow(B, a, p)
enc = flag * shared_secret

print(f'\nencrypted flag: {enc}')
exit()
