#!/usr/local/bin/python3
inp = input("> ")

f = lambda: None

for i, v in enumerate(inp):
    if v == "_":
        continue
    if not (ord(v) < 128 and i % 2 == ord(v) % 2):
        print('bad')
        exit()

eval(inp, {"__builtins__": None, 'f': f})
