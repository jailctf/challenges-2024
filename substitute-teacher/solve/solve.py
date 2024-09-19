from pwn import *

PROG = """
^ $@#
#0 A#
#1 B#
#2 C#
#3 D#
#4 E#
#5 F#
#6 G#
#7 H#
#8 I#
#9 J#
0$ $A
1$ $B
2$ $C
3$ $D
4$ $E
5$ $F
6$ $G
7$ $H
8$ $I
9$ $J
@
$ 
J ,aaaaaaaaa
I ,aaaaaaaa
H ,aaaaaaa
G ,aaaaaa
F ,aaaaa
E ,aaaa
D ,aaa
C ,aa
B ,a
A ,

a, ,aaaaaaaaaa
,, ,
@, @
@a @p
pa pp
, !:
:aa b:
!b !:b
:a :b
b c
!c !:c
:cc c:
@

c d
# ]}
pp] ]p
p} p]}
@
p q
:d@q] @*
:@] @*
:d@] @~
:@q] @~
~] ]~
*] ]*
~q] q]~
*q] q]*
@
:@ @*
:d@ @~
!@q] !@~
!@] !@*
@
!@* !@
!@ XL
~} Y}
*} R}
~ Y/
* /
R} }
Y/ /YY
/ 
LYYYYYYYYYY YL
XY XLY
@
LYYYYYYYYY} }9
LYYYYYYYY} }8
LYYYYYYY} }7
LYYYYYY} }6
LYYYYY} }5
LYYYY} }4
LYYY} }3
LYY} }2
LY} }1
L} }0
X} 
""".strip("\n")

before = [105, 108, 123, 116, 101]

p = remote("localhost", 5000)  # replace with remote when doing remote obviously

p.recvline()
from os import system
system(p.recvline())
p.sendline(input('copy paste the above sol to pow > ').encode()[:-1])

def try_n(n: int):
    total_before = before + [n]
    befstr = '106^97 256\n' + "\n".join([f"{i+256}^{v} {i+257}" for i, v in enumerate(total_before)])+"\n"
    p.sendline(b'y')
    p.send((befstr+PROG).encode() + b'\n<END>\n')
    p.recvline(timeout=2)
    p.recvuntil(b'flag bytes: ')
    return int(p.recvline())


while True:
    print("if the prog stops or errors then just copy the printed list and set it as before in the solve.py", before, 123123)
    overall = {}
    for n in b'_abcdefghijklmnopqrstuvwxyz{}':
        res = try_n(n)
        if res not in overall:
            overall[res] = []
        overall[res].append(n)
        print(n, res)
    if len(overall) != 2:
        continue
    for k in overall:
        if len(overall[k]) == 1:
            before.append(overall[k][0])
            break
    print(before)
