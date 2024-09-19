#!/usr/local/bin/python
import os

randombytes = os.urandom(32).hex()
os.system("mv /flag /flag-" + randombytes)

with open("/tmp/file.py", "r") as f:
    cod = f.read()

for c in cod:
    if ord(c) >= 128:
        print("only ascii")
        exit()
    if c in "_":
        print("no underscores")
        exit()

print("Good luck", flush=True)

os.system("/app/embedder /tmp/file.py 2>&1")
