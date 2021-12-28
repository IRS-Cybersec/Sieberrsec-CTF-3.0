#!/usr/bin/env python3
from aoc import Grid,Point # https://github.com/152334H/aoc
from pwn import *
import pyte # fun module to handle PTYs
from re import findall
from tqdm import tqdm

DOWN = b'\x1b[B'
screen = pyte.Screen(100,30)
stream = pyte.ByteStream(screen)
#r = process('./bin/rockfarming_simulator', env={'TERM': 'linux', 'COLUMNS': '100', 'LINES': '30'}, stdin=PTY)
r = process(['ssh', '-p33251', 'rock_farming_simulator@challs.sieberrsec.tech'], env={'TERM': 'linux', 'COLUMNS': '100', 'LINES': '30'}, stdin=PTY)
def send_raw(b,t=0.1):
    r.send_raw(b)
    stream.feed(r.recvrepeat(timeout=t+0.3))
def dig(): send_raw(b'T\n',1.2)
def wallet() -> int: return int(findall('\d+', screen.display[1])[0])
def display():
    print(*screen.display, sep='\n')
    print("\033[A"*30,end='\r')
def parse(l):
    income,cost = map(int,findall('\d+',l))
    return cost,l.split()[0][0], income
stream.feed(r.recvrepeat(timeout=0.3))
display()
def solve_maze():
    g= Grid([l[3:-1].strip() for l in screen.display[6:-1] if l[3:-1].strip()], forbidden='#')
    start = g.find_unique('*')
    end = g.find_unique('@')
    border = [(start,[])]
    while border:
        nb = []
        for (cur,his) in border:
            if cur == end: break
            for n in g.adj(cur):
                if (not his or n != his[-1]) and g[n] != '#':
                    nb.append((n,his+[cur]))
        else:
            border = nb
            continue
        break
    else: raise RuntimeError('No path found')
    his.append(cur)
    path = [his[i]-his[i-1] for i in range(1,len(his))]
    path = ''.join({Point(-1,0): 'a', Point(1,0): 'd', Point(0,1): 's', Point(0,-1): 'w'}[p] for p in path)
    send_raw(path.encode(), 0.15)

# get the cost of the ponies
send_raw(b'B')
pones = [parse(findall("- .*\.", l)[0][2:]) for l in screen.display[5:10]]
pones.sort()
required_money = pones[-1][0]
send_raw(b'\n\n',0.65)
solve_maze()
display()
print(pones)

# get enough money to buy the most expensive pony
progress = tqdm(total=required_money, unit='$')
prev = 0
while (money:=wallet()) < required_money:
    progress.update(money-prev)
    prev = money
    dig()

# attempt to race condition
send_raw(b'B' + pones[-1][1].encode() + b'\n', 0.65)
solve_maze()
display()
#if wallet() < required_money: raise RuntimeError # 50% chance of winning
send_raw(b'B' + pones[-2][1].encode() + b'\n', 1)
solve_maze()
stream.feed(r.recvrepeat(timeout=2))
send_raw(b'H', 2)
display()
