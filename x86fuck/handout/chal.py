#!/usr/local/bin/python

from unicorn import Uc, UcError, UC_ARCH_X86, UC_HOOK_INTR, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBX

def read_bytes(uc, addr):
    ret = b''
    i = 0
    while (c := uc.mem_read(addr + i, 1)) != b'\x00':
        ret += c
        i += 1
    return ret

def hook_interrupt(uc, intno, user_data):
    if intno == 0x80:
        sysno = uc.reg_read(UC_X86_REG_EAX)
        filename = uc.reg_read(UC_X86_REG_EBX)

        if sysno == 11 and read_bytes(uc, filename) == b'/bin/sh':
            print(open('flag.txt', 'r').read())
            mu.emu_stop()

code = bytes.fromhex(input('Please input your finest shellcode (in hex): '))

if len(code) > 4096:
    print('Too big! Try again.')
    exit(1)

if len(set(code)) > 2:
    print("Too diverse! Try again.")
    exit(1)

mu = Uc(UC_ARCH_X86, UC_MODE_32)
mu.mem_map(0, 4096)
mu.mem_write(0, code)
mu.hook_add(UC_HOOK_INTR, hook_interrupt)

try:
    mu.emu_start(0, len(code))
except UcError as e:
    print(f'Error: {e}')
