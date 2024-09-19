from pwn import *
from os import system

p = remote("localhost", 5000)

p.recvline()
system(p.recvline())
r = input('copy paste pow sol from above > ')[:-1].encode()
p.sendline(r)

p.sendline(open('payload.js', 'rb').read())

p.interactive()

