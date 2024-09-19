#!/usr/local/bin/python
from os import __dict__

value = input("speak to me > ")
code = input("your code > ")

assert all(32 <= ord(x) < 127 for x in code), 'cant read this'

def f():
    pass

f.__code__ = f.__code__.replace(co_names=(), co_code=code.encode())
f()
