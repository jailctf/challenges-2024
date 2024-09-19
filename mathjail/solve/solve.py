from pwn import *

L1 = 'n+n//n'
L2 = '((n+n)*(n+n+n+n+n)//n//n)**n*n*n//(n+n+n)//(n+n+n)'
L3 = '(n%n)**((n+n+n)//n%((((n+n)//n)**n-n//n)%n*((((n+n+n)//n)**n%n-(n+n)//n)%n)+(n+n)//n))'
L4 = 'n**(n*n)//(n**(n+n)-n**n-n//n)%n**n'

# io = process(['python3', 'chal.py'])
io = remote('challs3.pyjail.club', 9144)
io.sendlineafter(b': ', L1.encode())
io.sendlineafter(b': ', L2.encode())
io.sendlineafter(b': ', L3.encode())
io.sendlineafter(b': ', L4.encode())
io.interactive()