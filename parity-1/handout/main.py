#!/usr/local/bin/python3
inp = input("> ")

for i, v in enumerate(inp):
    if not (ord(v) < 128 and i % 2 == ord(v) % 2):
        print('bad')
        exit()

eval(inp)
