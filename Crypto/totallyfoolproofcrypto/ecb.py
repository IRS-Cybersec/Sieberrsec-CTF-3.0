from pwn import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from string import *
charset = ascii_letters+digits+punctuation
from tqdm import tqdm
HOST = 'localhost'
#r = remote(HOST, 31311)
r = process(['python3.8','server.py'])

def enc(pt: bytes) -> str:
    r.sendlineafter('> ', pt)
    if b'\n' in pt: raise RuntimeError(pt)
    return bytes.fromhex(r.recvline().decode())

smallestlen = len(enc(b'A'))
for i in range(2,16):
    if len(enc(b'A'*i)) != smallestlen: break
# At this point, (i+len(FLAG)) % 16 == 0
# Note that when ls = blockify(enc(pad(b'}', 16) + b'A'*(i+1))), ls[0] == ls[-1].

flag = ''
while '{' not in flag:
    if b'\n' in pad(b'.'+flag.encode(), AES.block_size): #uh-oh
        for c1 in tqdm(charset):
            for c2 in charset:
                guess = c1+c2+flag
                padded = pad(guess.encode(), AES.block_size)
                pt = padded[:16]+b'A'*(i+len(guess))
                ls = group(16,enc(pt))
                if ls[0] in ls[1:]: break
            else: continue
            break
        else:
            print("PANIC: CHARACTERS NOT FOUND")
            exit(1)
    else:
        for c in tqdm(charset):
            guess = c+flag
            padded = pad(guess.encode(), AES.block_size)
            pt = padded[:16]+b'A'*(i+len(guess))
            ls = group(16,enc(pt))
            if ls[0] in ls[1:]: break
        else:
            print("PANIC: CHARACTER NOT FOUND")
            exit(1)
    flag = guess
print("IRS"+flag)
