#!/usr/local/bin/python3

if eval(__import__('regex').fullmatch(r'[a-oq-z]+\(((?R)|)\)', input('> '))[0]) == 0x1337133713371337:
    print(open('flag.txt', 'r').read())

