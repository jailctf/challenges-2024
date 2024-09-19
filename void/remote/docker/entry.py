#!/usr/local/bin/python
import os

cod = ""

while True:
    try:
        line = input("(EOF to finish)> ")
    except EOFError:
        break
    if line == "EOF":
        break
    cod += line + "\n"

for c in cod:
    if ord(c) >= 128:
        print("only ascii")
        exit()
    if c in "_":
        print("no underscores")
        exit()

with open("/tmp/file.py", "w") as f:
    f.write(cod)

print("Good luck", flush=True)

os.system("/app/embedder /tmp/file.py 2>&1")
